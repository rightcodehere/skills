# Kotlin / Android Code Review Guide

> Kotlin/Android ，、Flow 、Compose 、、、。

## 

- [：](#)
- [Flow ](#flow-)
- [Jetpack Compose ](#jetpack-compose-)
- [](#)
- [](#)
- [：ViewModel  Repository](#viewmodel--repository)
- [](#)
- [Review Checklist](#review-checklist)

---

## ：

###  GlobalScope

```kotlin
// ❌ GlobalScope ，Activity/Fragment 
GlobalScope.launch {
    val data = api.fetchData()
    binding.textView.text = data.title // Crash: view destroyed
}

// ✅  viewModelScope，ViewModel 
class MyViewModel(private val repo: Repository) : ViewModel() {
    fun loadData() {
        viewModelScope.launch {
            val data = repo.fetchData()
            _uiState.value = UiState.Success(data)
        }
    }
}

// ✅  Activity/Fragment  lifecycleScope
class MyActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        lifecycleScope.launch {
            val data = repo.fetchData()
            binding.textView.text = data.title
        }
    }
}
```

### CancellationException 

```kotlin
// ❌ 
viewModelScope.launch {
    try {
        repo.fetchData()
    } catch (e: Exception) {
        // CancellationException ，
        showError(e)
    }
}

// ✅  CancellationException
viewModelScope.launch {
    try {
        repo.fetchData()
    } catch (e: CancellationException) {
        throw e // Must rethrow
    } catch (e: Exception) {
        showError(e)
    }
}

// ✅  catch  ensureActive
viewModelScope.launch {
    try {
        repo.fetchData()
    } catch (e: Exception) {
        ensureActive() // Rethrows if cancelled
        showError(e)
    }
}
```

### CPU-bound 

```kotlin
// ❌ CPU ，
viewModelScope.launch(Dispatchers.Default) {
    for (item in largeList) {
        heavyComputation(item)
    }
}

// ✅  isActive  ensureActive
viewModelScope.launch(Dispatchers.Default) {
    for (item in largeList) {
        ensureActive() // Throws CancellationException if cancelled
        heavyComputation(item)
    }
}

// ✅  yield 
viewModelScope.launch(Dispatchers.Default) {
    for (item in largeList) {
        yield() // Checks cancellation + yields to other coroutines
        heavyComputation(item)
    }
}
```

###  runInterruptible

```kotlin
// ❌  I/O，
viewModelScope.launch(Dispatchers.IO) {
    val result = blockingLibraryCall() // Blocks IO thread
}

// ✅  runInterruptible ，
viewModelScope.launch(Dispatchers.IO) {
    val result = runInterruptible {
        blockingLibraryCall() // Interrupted on cancellation
    }
}
```

### 

```kotlin
// ❌ CPU  IO （，）
viewModelScope.launch(Dispatchers.IO) {
    val bitmap = decodeImage(byteArray) // CPU-bound on IO pool
}

// ✅ CPU  Default，I/O  IO
viewModelScope.launch(Dispatchers.Default) {
    val bitmap = decodeImage(byteArray) // CPU-bound on Default pool
}

// ❌ IO  Default （，）
viewModelScope.launch(Dispatchers.Default) {
    val response = okHttpClient.newCall(request).execute() // I/O on Default pool
}

// ✅ I/O  IO 
viewModelScope.launch(Dispatchers.IO) {
    val response = okHttpClient.newCall(request).execute()
}
```

### launch vs async

```kotlin
// ❌ async ""，
viewModelScope.launch {
    async { analytics.trackEvent("click") } // Overkill
}

// ✅  launch
viewModelScope.launch {
    launch { analytics.trackEvent("click") }
}

// ✅  async
viewModelScope.launch {
    val deferredA = async { api.fetchA() }
    val deferredB = async { api.fetchB() }
    val result = combine(deferredA.await(), deferredB.await())
}
```

###  Job() 

```kotlin
// ❌ Job() 
viewModelScope.launch {
    launch(Job()) { // Detached from parent scope!
        importantWork() // Will NOT be cancelled when viewModelScope cancels
    }
}

// ✅ 
viewModelScope.launch {
    launch { // Child of viewModelScope
        importantWork() // Cancelled when viewModelScope cancels
    }
}

// ✅ ，
class MyManager(private val scope: CoroutineScope) {
    // Independent lifecycle managed by MyManager.shutdown()
    private val managerJob = Job(scope.coroutineContext[Job])
    private val managerScope = scope + managerJob + Dispatchers.IO

    fun shutdown() {
        managerJob.cancel()
    }
}
```

### NonCancellable 

```kotlin
// ❌  withContext(NonCancellable) ，
viewModelScope.launch {
    withContext(NonCancellable) { // Entire block is uncancellable!
        val data = repo.fetchData() // Cannot be cancelled
        db.saveData(data) // Cannot be cancelled
        analytics.track("saved")
    }
}

// ✅ NonCancellable 
viewModelScope.launch {
    try {
        val data = repo.fetchData()
        db.saveData(data)
    } catch (e: CancellationException) {
        throw e
    } finally {
        withContext(NonCancellable) {
            db.cleanup() // Only cleanup is uncancellable
        }
    }
}
```

---

## Flow 

### 

```kotlin
// ❌  collect  flow {} （）
val userFlow = flow {
    emit(api.fetchUser()) // Called once per collector!
}

// Two collectors = two network requests
lifecycleScope.launch { userFlow.collect { } }
lifecycleScope.launch { userFlow.collect { } }

// ✅  StateFlow/SharedFlow（）
class MyViewModel(private val repo: Repository) : ViewModel() {
    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            _uiState.value = UiState.Success(repo.fetchUser())
        }
    }
}
// Multiple collectors share the same StateFlow
```

###  flow {} 

```kotlin
// ❌  flow builder  withContext，
val dataFlow = flow {
    withContext(Dispatchers.IO) { // IllegalStateException!
        emit(api.fetchData())
    }
}

// ✅  flowOn 
val dataFlow = flow {
    emit(api.fetchData()) // Runs on IO via flowOn
}.flowOn(Dispatchers.IO)

// ✅  channelFlow / callbackFlow 
val dataFlow = channelFlow {
    withContext(Dispatchers.IO) {
        send(api.fetchData()) // send() is safe in channelFlow
    }
}
```

### collect 

```kotlin
// ❌  Activity/Fragment  collect 
lifecycleScope.launch {
    viewModel.uiState.collect { state ->
        binding.textView.text = state.title // Crash if view destroyed
    }
}

// ✅  Fragment  viewLifecycleOwner.lifecycleScope + repeatOnLifecycle
viewLifecycleOwner.lifecycleScope.launch {
    viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.uiState.collect { state ->
            binding.textView.text = state.title
        }
    }
}

// ✅  Compose  collectAsStateWithLifecycle
@Composable
fun MyScreen(viewModel: MyViewModel) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    // ...
}
```

### ： catch 

```kotlin
// ❌  collect  try-catch 
viewModelScope.launch {
    try {
        dataFlow.collect { data ->
            processData(data)
        }
    } catch (e: Exception) {
        // This also catches exceptions from processData, not just upstream
        showError(e)
    }
}

// ✅  catch 
viewModelScope.launch {
    dataFlow
        .catch { e -> showError(e) } // Only catches upstream exceptions
        .collect { data ->
            processData(data) // Exceptions here propagate normally
        }
}
```

### StateFlow vs SharedFlow 

```kotlin
// ❌  SharedFlow  StateFlow，
private val _state = MutableSharedFlow<UiState>()
val state: SharedFlow<UiState> = _state

// ✅ UI  StateFlow：、
class MyViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()
}

// ✅ （） SharedFlow + replay(0)
class MyViewModel : ViewModel() {
    private val _navigationEvent = MutableSharedFlow<NavTarget>(extraBufferCapacity = 1)
    val navigationEvent: SharedFlow<NavTarget> = _navigationEvent.asSharedFlow()

    fun navigate(target: NavTarget) {
        _navigationEvent.tryEmit(target)
    }
}

// ✅ Channel （）
private val _navigationEvent = Channel<NavTarget>(Channel.BUFFERED)
val navigationEvent = _navigationEvent.receiveAsFlow()
```

---

## Jetpack Compose 

### 

```kotlin
// ❌ ，Compose 
data class UserProfile(
    val name: String,
    val friends: List<String>, // Unstable! List is not @Stable
)

@Composable
fun ProfileCard(profile: UserProfile) { // Recomposes even if profile didn't change
    Text(profile.name)
}

// ✅  @Immutable 
@Immutable
data class UserProfile(
    val name: String,
    val friends: ImmutableList<String>, // kotlinx.collections.immutable
)

// ✅ 
@Composable
fun ProfileCard(
    name: String, // Stable: String is primitive
    friendCount: Int, // Stable: Int is primitive
) {
    Text(name)
    Text("$friendCount friends")
}
```

### Lambda 

```kotlin
// ❌  Lambda，
@Composable
fun MyScreen(viewModel: MyViewModel) {
    LazyColumn {
        items(items, key = { it.id }) { item ->
            ItemRow(
                item = item,
                onClick = { viewModel.handleClick(item.id) } // New lambda each recomposition!
            )
        }
    }
}

// ✅  remember  Lambda， ViewModel 
@Composable
fun MyScreen(viewModel: MyViewModel) {
    LazyColumn {
        items(items, key = { it.id }) { item ->
            ItemRow(
                item = item,
                onClick = remember(item.id) { { viewModel.handleClick(item.id) } }
            )
        }
    }
}
```

###  derivedStateOf 

```kotlin
// ❌ 
@Composable
fun ScrollToTopButton(lazyListState: LazyListState) {
    val showButton = lazyListState.firstVisibleItemIndex > 0 // Recomposes on every scroll
    if (showButton) {
        Button(onClick = { /* scroll to top */ }) {
            Text("Top")
        }
    }
}

// ✅  derivedStateOf 
@Composable
fun ScrollToTopButton(lazyListState: LazyListState) {
    val showButton by remember {
        derivedStateOf { lazyListState.firstVisibleItemIndex > 0 }
    }
    if (showButton) {
        Button(onClick = { /* scroll to top */ }) {
            Text("Top")
        }
    }
}
```

###  Composable 

```kotlin
// ❌  Composable ，
@Composable
fun MyScreen(userId: String, viewModel: MyViewModel) {
    viewModel.loadUser(userId) // Called on every recomposition!
    val user by viewModel.user.collectAsStateWithLifecycle()
    Text(user?.name ?: "Loading...")
}

// ✅  LaunchedEffect  key 
@Composable
fun MyScreen(userId: String, viewModel: MyViewModel) {
    LaunchedEffect(userId) {
        viewModel.loadUser(userId) // Only when userId changes
    }
    val user by viewModel.user.collectAsStateWithLifecycle()
    Text(user?.name ?: "Loading...")
}

// ✅  remember { ... }
@Composable
fun MyScreen(viewModel: MyViewModel) {
    val initialData = remember { viewModel.getInitialData() }
}
```

### 

```kotlin
// ❌  Composable ，
@Composable
fun ToggleButton() {
    var isChecked by remember { mutableStateOf(false) }
    Switch(
        checked = isChecked,
        onCheckedChange = { isChecked = it }
    )
}

// ✅ ：
@Composable
fun ToggleButton(
    isChecked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier,
) {
    Switch(
        checked = isChecked,
        onCheckedChange = onCheckedChange,
        modifier = modifier,
    )
}

// ✅ 
@Composable
fun ParentScreen() {
    var enabled by rememberSaveable { mutableStateOf(false) }
    ToggleButton(
        isChecked = enabled,
        onCheckedChange = { enabled = it },
    )
}
```

---

## 

###  !!

```kotlin
// ❌ ： null  NPE
val user = getUser()!!
val name = user.name!!

// ✅  + 
val name = getUser()?.name ?: "Unknown"

// ✅ requireNotNull 
val user = requireNotNull(getUser()) { "User must not be null at this point" }

// ✅ 
fun process(user: User?) {
    val nonNullUser = user ?: return
    nonNullUser.doSomething()
}
```

### lateinit vs nullable vs lazy

```kotlin
// ❌ lateinit  null （）
lateinit var optionalConfig: Config // Might never be set

// ✅ lateinit 
class MyActivity : AppCompatActivity() {
    lateinit var binding: ActivityMainBinding // Set in onCreate

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
    }
}

// ✅ nullable + lateinit 
// lateinit: 
// nullable: ， null 
// lazy: 

class MyViewModel(private val repo: Repository) : ViewModel() {
    // lazy: ，
    val expensiveObject by lazy { ExpensiveObject(repo) }

    // nullable: 
    var cachedData: Data? = null
        private set
}
```

### Java ：

```kotlin
// ❌ Java （ null），Kotlin 
// Java:
// public User getUser() { return null; }
val name: String = javaService.getUser().name // NPE!

// ✅  Java 
val user: User? = javaService.getUser()
val name = user?.name ?: "Unknown"

// ✅  Kotlin  Java API，
class SafeUserService(private val delegate: JavaUserService) {
    fun getUser(): User? = delegate.getUser() // Explicitly nullable
}
```

---

## 

###  Context/View

```kotlin
// ❌  Activity Context，Activity 
class MyActivity : AppCompatActivity() {
    fun loadData() {
        // Leaking Activity via coroutine
        GlobalScope.launch {
            val data = repo.fetchData()
            // 'this' (Activity) is captured
            binding.textView.text = data // Activity leaked!
        }
    }
}

// ✅  viewModelScope + 
class MyViewModel(private val repo: Repository) : ViewModel() {
    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    fun loadData() {
        viewModelScope.launch {
            val data = repo.fetchData()
            _uiState.value = UiState.Success(data) // No Activity reference
        }
    }
}
```

### 

```kotlin
// ❌ 
class MyFragment : Fragment() {
    private val sensorListener = object : SensorEventListener {
        override fun onSensorChanged(event: SensorEvent) { }
        override fun onAccuracyChanged(sensor: Sensor, accuracy: Int) { }
    }

    override fun onResume() {
        super.onResume()
        sensorManager.registerListener(sensorListener, sensor, SensorManager.SENSOR_DELAY_UI)
        // Never unregistered!
    }
}

// ✅  onPause/onDestroyView 
override fun onResume() {
    super.onResume()
    sensorManager.registerListener(sensorListener, sensor, SensorManager.SENSOR_DELAY_UI)
}

override fun onPause() {
    super.onPause()
    sensorManager.unregisterListener(sensorListener)
}
```

###  CoroutineScope

```kotlin
// ❌  CoroutineScope 
class MyManager(private val scope: CoroutineScope) {
    private val job = SupervisorJob()
    private val managerScope = scope + job + Dispatchers.IO

    fun start() {
        managerScope.launch {
            while (isActive) {
                pollServer()
                delay(5000)
            }
        }
    }
    // Never cancelled! job lives forever.
}

// ✅  Job
class MyManager(private val scope: CoroutineScope) {
    private val job = SupervisorJob()
    private val managerScope = scope + job + Dispatchers.IO

    fun start() {
        managerScope.launch {
            while (isActive) {
                pollServer()
                delay(5000)
            }
        }
    }

    fun shutdown() {
        job.cancel()
    }
}

// ✅ ViewModel  closeableScope（Kotlin 2.1+）
class MyViewModel : ViewModel() {
    private val scope = viewModelScope + Dispatchers.IO
    // Automatically cancelled when ViewModel is cleared
}
```

---

## ：ViewModel  Repository

### ViewModel 

```kotlin
// ❌  MutableStateFlow，
class MyViewModel : ViewModel() {
    val uiState = MutableStateFlow<UiState>(UiState.Loading) // Mutable!

    fun load() {
        viewModelScope.launch {
            uiState.value = UiState.Success(repo.fetchData())
        }
    }
}

// ✅ ，
class MyViewModel(private val repo: Repository) : ViewModel() {
    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    fun load() {
        viewModelScope.launch {
            _uiState.value = UiState.Success(repo.fetchData())
        }
    }
}
```

###  Repository

```kotlin
// ❌ ViewModel 
class UserViewModel(private val api: Api) : ViewModel() {
    private val _users = MutableStateFlow<List<User>>(emptyList())
    val users: StateFlow<List<User>> = _users.asStateFlow()

    fun loadUsers() {
        viewModelScope.launch {
            val raw = api.getUsers()
            val filtered = raw.filter { it.isActive }
            val sorted = filtered.sortedBy { it.name.lowercase() }
            val enriched = sorted.map { user ->
                user.copy(displayName = "${user.firstName} ${user.lastName}")
            }
            _users.value = enriched
        }
    }
}

// ✅ ViewModel ， Repository
class UserRepository(private val api: Api) {
    suspend fun getActiveUsersSorted(): List<User> {
        return api.getUsers()
            .filter { it.isActive }
            .sortedBy { it.name.lowercase() }
            .map { it.copy(displayName = "${it.firstName} ${it.lastName}") }
    }
}

class UserViewModel(private val repo: UserRepository) : ViewModel() {
    private val _users = MutableStateFlow<List<User>>(emptyList())
    val users: StateFlow<List<User>> = _users.asStateFlow()

    fun loadUsers() {
        viewModelScope.launch {
            _users.value = repo.getActiveUsersSorted()
        }
    }
}
```

### （Offline-First）

```kotlin
// ❌ ViewModel ，，
class MyViewModel(private val api: Api) : ViewModel() {
    fun load() {
        viewModelScope.launch {
            _uiState.value = UiState.Success(api.fetchData())
        }
    }
}

// ✅ Repository ，
class MyRepository(
    private val api: Api,
    private val dao: DataDao,
) {
    val data: Flow<List<Data>> = dao.getAll()
        .map { entities -> entities.map { it.toDomain() } }

    suspend fun refresh() {
        val remote = api.fetchData()
        dao.replaceAll(remote.map { it.toEntity() })
    }
}

class MyViewModel(private val repo: MyRepository) : ViewModel() {
    val uiState = repo.data.map { UiState.Success(it) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), UiState.Loading)

    fun refresh() {
        viewModelScope.launch { repo.refresh() }
    }
}
```

### Use Case 

```kotlin
// ❌ Repository ，
class OrderRepository {
    suspend fun validateAndSubmitOrder(order: Order) { }
    suspend fun calculateOrderTotalWithDiscounts(order: Order): Money { }
    suspend fun checkInventoryAndReserve(items: List<Item>) { }
}

// ✅  Use Case ，Repository 
class SubmitOrderUseCase(
    private val orderRepo: OrderRepository,
    private val inventoryRepo: InventoryRepository,
    private val paymentRepo: PaymentRepository,
) {
    suspend operator fun invoke(order: Order): Result<OrderConfirmation> {
        val validated = order.validate()
        inventoryRepo.reserve(validated.items)
        val total = CalculateOrderTotalUseCase().invoke(validated)
        return paymentRepo.charge(total).map { confirmation ->
            orderRepo.save(validated.copy(status = OrderStatus.CONFIRMED))
            confirmation
        }
    }
}

class OrderRepository {
    suspend fun save(order: Order) { }
    suspend fun getById(id: String): Order? { }
    fun observeOrders(): Flow<List<Order>> { }
}
```

---

## 

### UI ：

```kotlin
// ❌  nullable ，
data class UiState(
    val isLoading: Boolean = false,
    val data: List<Item>? = null,
    val error: String? = null,
)
// Invalid: isLoading=true AND error != null
// Invalid: data != null AND error != null

// ✅ ，
sealed interface UiState {
    data object Loading : UiState
    data class Success(val data: List<Item>) : UiState
    data class Error(val message: String, val cause: Throwable? = null) : UiState
}

class MyViewModel(private val repo: Repository) : ViewModel() {
    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()
}

// ✅ Compose  exhaustive when
@Composable
fun MyScreen(viewModel: MyViewModel) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    when (state) {
        is UiState.Loading -> CircularProgressIndicator()
        is UiState.Success -> DataList((state as UiState.Success).data)
        is UiState.Error -> ErrorMessage((state as UiState.Error).message)
    }
}
```

### 

```kotlin
// ❌ ，
sealed class NavEvent {
    object ToDetail : NavEvent()
    object ToSettings : NavEvent()
}
// How to pass orderId to ToDetail?

// ✅ 
sealed interface NavEvent {
    data class ToDetail(val orderId: String) : NavEvent
    data class ToSettings(val tab: SettingsTab) : NavEvent
    data class ToProfile(val userId: String, val mode: ProfileMode) : NavEvent
}

// ✅ 
navController.handleNavEvent { event ->
    when (event) {
        is NavEvent.ToDetail -> navController.navigate(DetailRoute(event.orderId))
        is NavEvent.ToSettings -> navController.navigate(SettingsRoute(event.tab))
        is NavEvent.ToProfile -> navController.navigate(ProfileRoute(event.userId, event.mode))
    }
}
```

### 

```kotlin
// ❌  Result?  nullable ，
suspend fun fetchUser(id: String): User? {
    return try {
        api.getUser(id)
    } catch (e: Exception) {
        null // What went wrong?
    }
}

// ✅ 
sealed interface NetworkResult<out T> {
    data class Success<T>(val data: T) : NetworkResult<T>
    data class Error(val code: Int, val message: String) : NetworkResult<Nothing>
    data class Exception(val cause: Throwable) : NetworkResult<Nothing>
}

suspend fun fetchUser(id: String): NetworkResult<User> {
    return try {
        val response = api.getUser(id)
        if (response.isSuccessful) {
            NetworkResult.Success(response.body()!!)
        } else {
            NetworkResult.Error(response.code(), response.message())
        }
    } catch (e: Exception) {
        NetworkResult.Exception(e)
    }
}

// ✅  ViewModel  UI 
fun loadUser(id: String) {
    viewModelScope.launch {
        when (val result = repo.fetchUser(id)) {
            is NetworkResult.Success -> _uiState.value = UiState.Success(result.data)
            is NetworkResult.Error -> _uiState.value = UiState.Error("Server error: ${result.code}")
            is NetworkResult.Exception -> _uiState.value = UiState.Error(result.cause.message ?: "Unknown")
        }
    }
}
```

---

## Review Checklist

### 

- [ ]  `GlobalScope`， `viewModelScope` / `lifecycleScope`
- [ ] `CancellationException` ，
- [ ] CPU  `Dispatchers.Default`，I/O  `Dispatchers.IO`
- [ ]  CPU  `ensureActive()`  `yield()`
- [ ]  `runInterruptible` 
- [ ]  `Job()` 
- [ ] `NonCancellable`  `finally` 
- [ ]  `launch`， `async`

### Flow

- [ ] （`flow {}`）（`StateFlow`/`SharedFlow`）
- [ ]  `flow {}` builder  `withContext`， `flowOn` 
- [ ] `collect`  `repeatOnLifecycle`  `collectAsStateWithLifecycle` 
- [ ]  `.catch`  `try-catch`  `collect`
- [ ] UI  `StateFlow`， `SharedFlow`  `Channel`

### Compose

- [ ] Composable ，
- [ ] Lambda  `remember` ，
- [ ]  `derivedStateOf` 
- [ ]  `LaunchedEffect` / `SideEffect`，
- [ ] （state hoisting），Composable 

### 

- [ ]  `!!`， `?.`  `?:`
- [ ] `lateinit` 
- [ ] Java 
- [ ] `lazy` 

### 

- [ ]  `Context` / `View` 
- [ ]  `onPause` / `onDestroyView` 
- [ ]  `CoroutineScope` 
- [ ]  `Activity` / `Fragment` 

### 

- [ ] ViewModel  `MutableStateFlow` / `MutableLiveData`，
- [ ]  Repository / Use Case，ViewModel 
- [ ]  offline-first：Repository 
- [ ]  Use Case 

### 

- [ ] UI ，
- [ ] 
- [ ] ，
- [ ] `when` （exhaustive check）
