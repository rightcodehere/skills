# Rust Code Review Guide

> Rust 。，——、API 、、。

## 

- [](#)
- [Unsafe ](#unsafe-)
- [](#)
- [](#)
- [spawn vs await](#spawn-vs-await)
- [](#)
- [](#)
- [Trait ](#trait-)
- [Review Checklist](#rust-review-checklist)

---

## 

###  clone()

```rust
// ❌ clone() "Rust "——
fn bad_process(data: &Data) -> Result<()> {
    let owned = data.clone();  //  clone？
    expensive_operation(owned)
}

// ✅ ：clone ？？
fn good_process(data: &Data) -> Result<()> {
    expensive_operation(data)  // 
}

// ✅  clone，
fn justified_clone(data: &Data) -> Result<()> {
    // Clone needed: data will be moved to spawned task
    let owned = data.clone();
    tokio::spawn(async move {
        process(owned).await
    });
    Ok(())
}
```

### Arc<Mutex<T>> 

```rust
// ❌ Arc<Mutex<T>> 
struct BadService {
    cache: Arc<Mutex<HashMap<String, Data>>>,  // ？
}

// ✅ ，
struct GoodService {
    cache: HashMap<String, Data>,  // 
}

// ✅ ，
use dashmap::DashMap;

struct ConcurrentService {
    cache: DashMap<String, Data>,  // 
}
```

### Cow (Copy-on-Write) 

```rust
use std::borrow::Cow;

// ❌ 
fn bad_process_name(name: &str) -> String {
    if name.is_empty() {
        "Unknown".to_string()  // 
    } else {
        name.to_string()  // 
    }
}

// ✅  Cow 
fn good_process_name(name: &str) -> Cow<'_, str> {
    if name.is_empty() {
        Cow::Borrowed("Unknown")  // ，
    } else {
        Cow::Borrowed(name)  // 
    }
}

// ✅ 
fn normalize_name(name: &str) -> Cow<'_, str> {
    if name.chars().any(|c| c.is_uppercase()) {
        Cow::Owned(name.to_lowercase())  // ，
    } else {
        Cow::Borrowed(name)  // ，
    }
}
```

---

## Unsafe （！）

### 

```rust
// ❌ unsafe ——
unsafe fn bad_transmute<T, U>(t: T) -> U {
    std::mem::transmute(t)
}

// ✅  unsafe ：？？
/// Transmutes `T` to `U`.
///
/// # Safety
///
/// - `T` and `U` must have the same size and alignment
/// - `T` must be a valid bit pattern for `U`
/// - The caller ensures no references to `t` exist after this call
unsafe fn documented_transmute<T, U>(t: T) -> U {
    // SAFETY: Caller guarantees size/alignment match and bit validity
    std::mem::transmute(t)
}
```

### Unsafe 

```rust
// ❌  unsafe 
fn bad_get_unchecked(slice: &[u8], index: usize) -> u8 {
    unsafe { *slice.get_unchecked(index) }
}

// ✅  unsafe  SAFETY 
fn good_get_unchecked(slice: &[u8], index: usize) -> u8 {
    debug_assert!(index < slice.len(), "index out of bounds");
    // SAFETY: We verified index < slice.len() via debug_assert.
    // In release builds, callers must ensure valid index.
    unsafe { *slice.get_unchecked(index) }
}

// ✅  unsafe  API
pub fn checked_get(slice: &[u8], index: usize) -> Option<u8> {
    if index < slice.len() {
        // SAFETY: bounds check performed above
        Some(unsafe { *slice.get_unchecked(index) })
    } else {
        None
    }
}
```

###  unsafe 

```rust
// ✅ FFI 
extern "C" {
    fn external_function(ptr: *const u8, len: usize) -> i32;
}

pub fn safe_wrapper(data: &[u8]) -> Result<i32, Error> {
    // SAFETY: data.as_ptr() is valid for data.len() bytes,
    // and external_function only reads from the buffer.
    let result = unsafe {
        external_function(data.as_ptr(), data.len())
    };
    if result < 0 {
        Err(Error::from_code(result))
    } else {
        Ok(result)
    }
}

// ✅  unsafe
pub fn fast_copy(src: &[u8], dst: &mut [u8]) {
    assert_eq!(src.len(), dst.len(), "slices must be equal length");
    // SAFETY: src and dst are valid slices of equal length,
    // and dst is mutable so no aliasing.
    unsafe {
        std::ptr::copy_nonoverlapping(
            src.as_ptr(),
            dst.as_mut_ptr(),
            src.len()
        );
    }
}
```

---

## 

### 

```rust
// ❌  async ——
async fn bad_async() {
    let data = std::fs::read_to_string("file.txt").unwrap();  // ！
    std::thread::sleep(Duration::from_secs(1));  // ！
}

// ✅  API
async fn good_async() -> Result<String> {
    let data = tokio::fs::read_to_string("file.txt").await?;
    tokio::time::sleep(Duration::from_secs(1)).await;
    Ok(data)
}

// ✅ ， spawn_blocking
async fn with_blocking() -> Result<Data> {
    let result = tokio::task::spawn_blocking(|| {
        // 
        expensive_cpu_computation()
    }).await?;
    Ok(result)
}
```

### Mutex  .await

```rust
// ❌  .await  std::sync::Mutex——
async fn bad_lock(mutex: &std::sync::Mutex<Data>) {
    let guard = mutex.lock().unwrap();
    async_operation().await;  // ！
    process(&guard);
}

// ✅ 1：
async fn good_lock_scoped(mutex: &std::sync::Mutex<Data>) {
    let data = {
        let guard = mutex.lock().unwrap();
        guard.clone()  // 
    };
    async_operation().await;
    process(&data);
}

// ✅ 2： tokio::sync::Mutex（ await）
async fn good_lock_tokio(mutex: &tokio::sync::Mutex<Data>) {
    let guard = mutex.lock().await;
    async_operation().await;  // OK: tokio Mutex  await
    process(&guard);
}

// 💡 ：
// - std::sync::Mutex：、、 await
// - tokio::sync::Mutex： await、
```

###  trait 

```rust
// ❌ async trait （）
#[async_trait]
trait BadRepository {
    async fn find(&self, id: i64) -> Option<Entity>;  //  Box
}

// ✅ Rust 1.75+： async trait 
trait Repository {
    async fn find(&self, id: i64) -> Option<Entity>;

    //  Future  allocation
    fn find_many(&self, ids: &[i64]) -> impl Future<Output = Vec<Entity>> + Send;
}

// ✅  dyn 
trait DynRepository: Send + Sync {
    fn find(&self, id: i64) -> Pin<Box<dyn Future<Output = Option<Entity>> + Send + '_>>;
}
```

---

## 

### 

```rust
//  Future  .await  drop ，？
//  Future： await 
//  Future：

// ❌ 
async fn cancel_unsafe(conn: &mut Connection) -> Result<()> {
    let data = receive_data().await;  // ...
    conn.send_ack().await;  // ...，
    Ok(())
}

// ✅ 
async fn cancel_safe(conn: &mut Connection) -> Result<()> {
    // 
    let transaction = conn.begin_transaction().await?;
    let data = receive_data().await;
    transaction.commit_with_ack(data).await?;  // 
    Ok(())
}
```

### select! 

```rust
use tokio::select;

// ❌  select!  Future
async fn bad_select(stream: &mut TcpStream) {
    let mut buffer = vec![0u8; 1024];
    loop {
        select! {
            //  timeout ，read 
            // ！
            result = stream.read(&mut buffer) => {
                handle_data(&buffer[..result?]);
            }
            _ = tokio::time::sleep(Duration::from_secs(5)) => {
                println!("Timeout");
            }
        }
    }
}

// ✅  API
async fn good_select(stream: &mut TcpStream) {
    let mut buffer = vec![0u8; 1024];
    loop {
        select! {
            // tokio::io::AsyncReadExt::read 
            // ，
            result = stream.read(&mut buffer) => {
                match result {
                    Ok(0) => break,  // EOF
                    Ok(n) => handle_data(&buffer[..n]),
                    Err(e) => return Err(e),
                }
            }
            _ = tokio::time::sleep(Duration::from_secs(5)) => {
                println!("Timeout, retrying...");
            }
        }
    }
}

// ✅  tokio::pin!  Future 
async fn pinned_select() {
    let sleep = tokio::time::sleep(Duration::from_secs(10));
    tokio::pin!(sleep);

    loop {
        select! {
            _ = &mut sleep => {
                println!("Timer elapsed");
                break;
            }
            data = receive_data() => {
                process(data).await;
                // sleep ，
            }
        }
    }
}
```

### 

```rust
/// Reads a complete message from the stream.
///
/// # Cancel Safety
///
/// This method is **not** cancel safe. If cancelled while reading,
/// partial data may be lost and the stream state becomes undefined.
/// Use `read_message_cancel_safe` if cancellation is expected.
async fn read_message(stream: &mut TcpStream) -> Result<Message> {
    let len = stream.read_u32().await?;
    let mut buffer = vec![0u8; len as usize];
    stream.read_exact(&mut buffer).await?;
    Ok(Message::from_bytes(&buffer))
}

/// Reads a message with cancel safety.
///
/// # Cancel Safety
///
/// This method is cancel safe. If cancelled, any partial data
/// is preserved in the internal buffer for the next call.
async fn read_message_cancel_safe(reader: &mut BufferedReader) -> Result<Message> {
    reader.read_message_buffered().await
}
```

---

## spawn vs await

###  spawn

```rust
// ❌  spawn——，
async fn bad_unnecessary_spawn() {
    let handle = tokio::spawn(async {
        simple_operation().await
    });
    handle.await.unwrap();  //  await？
}

// ✅  await 
async fn good_direct_await() {
    simple_operation().await;
}

// ✅ spawn 
async fn good_parallel_spawn() {
    let task1 = tokio::spawn(fetch_from_service_a());
    let task2 = tokio::spawn(fetch_from_service_b());

    // 
    let (result1, result2) = tokio::try_join!(task1, task2)?;
}

// ✅ spawn （fire-and-forget）
async fn good_background_spawn() {
    // ，
    tokio::spawn(async {
        cleanup_old_sessions().await;
        log_metrics().await;
    });

    // 
    handle_request().await;
}
```

### spawn  'static 

```rust
// ❌ spawn  Future  'static
async fn bad_spawn_borrow(data: &Data) {
    tokio::spawn(async {
        process(data).await;  // Error: `data`  'static
    });
}

// ✅ 1：
async fn good_spawn_clone(data: &Data) {
    let owned = data.clone();
    tokio::spawn(async move {
        process(&owned).await;
    });
}

// ✅ 2： Arc 
async fn good_spawn_arc(data: Arc<Data>) {
    let data = Arc::clone(&data);
    tokio::spawn(async move {
        process(&data).await;
    });
}

// ✅ 3：（tokio-scoped  async-scoped）
async fn good_scoped_spawn(data: &Data) {
    //  async-scoped crate
    async_scoped::scope(|s| async {
        s.spawn(async {
            process(data).await;  // 
        });
    }).await;
}
```

### JoinHandle 

```rust
// ❌  spawn 
async fn bad_ignore_spawn_error() {
    let handle = tokio::spawn(async {
        risky_operation().await
    });
    let _ = handle.await;  //  panic 
}

// ✅  JoinHandle 
async fn good_handle_spawn_error() -> Result<()> {
    let handle = tokio::spawn(async {
        risky_operation().await
    });

    match handle.await {
        Ok(Ok(result)) => {
            // 
            process_result(result);
            Ok(())
        }
        Ok(Err(e)) => {
            // 
            Err(e.into())
        }
        Err(join_err) => {
            //  panic 
            if join_err.is_panic() {
                error!("Task panicked: {:?}", join_err);
            }
            Err(anyhow!("Task failed: {}", join_err))
        }
    }
}
```

###  vs spawn

```rust
// ✅  join!（）
async fn structured_concurrency() -> Result<(A, B, C)> {
    // 
    // ，
    tokio::try_join!(
        fetch_a(),
        fetch_b(),
        fetch_c()
    )
}

// ✅  spawn 
struct TaskManager {
    handles: Vec<JoinHandle<()>>,
}

impl TaskManager {
    async fn shutdown(self) {
        // ：
        for handle in self.handles {
            if let Err(e) = handle.await {
                error!("Task failed during shutdown: {}", e);
            }
        }
    }

    async fn abort_all(self) {
        // ：
        for handle in self.handles {
            handle.abort();
        }
    }
}
```

---

## 

###  vs 

```rust
// ❌  anyhow—— match 
pub fn parse_config(s: &str) -> anyhow::Result<Config> { ... }

// ✅  thiserror， anyhow
#[derive(Debug, thiserror::Error)]
pub enum ConfigError {
    #[error("invalid syntax at line {line}: {message}")]
    Syntax { line: usize, message: String },
    #[error("missing required field: {0}")]
    MissingField(String),
    #[error(transparent)]
    Io(#[from] std::io::Error),
}

pub fn parse_config(s: &str) -> Result<Config, ConfigError> { ... }
```

### 

```rust
// ❌ 
fn bad_error() -> Result<()> {
    operation().map_err(|_| anyhow!("failed"))?;  // 
    Ok(())
}

// ✅  context 
fn good_error() -> Result<()> {
    operation().context("failed to perform operation")?;
    Ok(())
}

// ✅  with_context 
fn good_error_lazy() -> Result<()> {
    operation()
        .with_context(|| format!("failed to process file: {}", filename))?;
    Ok(())
}
```

### 

```rust
// ✅  #[source] 
#[derive(Debug, thiserror::Error)]
pub enum ServiceError {
    #[error("database error")]
    Database(#[source] sqlx::Error),

    #[error("network error: {message}")]
    Network {
        message: String,
        #[source]
        source: reqwest::Error,
    },

    #[error("validation failed: {0}")]
    Validation(String),
}

// ✅  From
impl From<sqlx::Error> for ServiceError {
    fn from(err: sqlx::Error) -> Self {
        ServiceError::Database(err)
    }
}
```

---

## 

###  collect()

```rust
// ❌  collect——
fn bad_sum(items: &[i32]) -> i32 {
    items.iter()
        .filter(|x| **x > 0)
        .collect::<Vec<_>>()  // ！
        .iter()
        .sum()
}

// ✅ 
fn good_sum(items: &[i32]) -> i32 {
    items.iter().filter(|x| **x > 0).copied().sum()
}
```

### 

```rust
// ❌ 
fn bad_concat(items: &[&str]) -> String {
    let mut s = String::new();
    for item in items {
        s = s + item;  // ！
    }
    s
}

// ✅  join
fn good_concat(items: &[&str]) -> String {
    items.join("")
}

// ✅  with_capacity 
fn good_concat_capacity(items: &[&str]) -> String {
    let total_len: usize = items.iter().map(|s| s.len()).sum();
    let mut result = String::with_capacity(total_len);
    for item in items {
        result.push_str(item);
    }
    result
}

// ✅  write! 
use std::fmt::Write;

fn good_concat_write(items: &[&str]) -> String {
    let mut result = String::new();
    for item in items {
        write!(result, "{}", item).unwrap();
    }
    result
}
```

### 

```rust
// ❌  Vec 
fn bad_check_any(items: &[Item]) -> bool {
    let filtered: Vec<_> = items.iter()
        .filter(|i| i.is_valid())
        .collect();
    !filtered.is_empty()
}

// ✅ 
fn good_check_any(items: &[Item]) -> bool {
    items.iter().any(|i| i.is_valid())
}

// ❌ String::from 
fn bad_static() -> String {
    String::from("error message")  // 
}

// ✅  &'static str
fn good_static() -> &'static str {
    "error message"  // 
}
```

---

## Trait 

### 

```rust
// ❌ —— Java， Interface 
trait Processor { fn process(&self); }
trait Handler { fn handle(&self); }
trait Manager { fn manage(&self); }  // Trait 

// ✅  trait
// 、
struct DataProcessor {
    config: Config,
}

impl DataProcessor {
    fn process(&self, data: &Data) -> Result<Output> {
        // 
    }
}
```

### Trait  vs 

```rust
// ❌  trait （）
fn bad_process(handler: &dyn Handler) {
    handler.handle();  // 
}

// ✅ （，）
fn good_process<H: Handler>(handler: &H) {
    handler.handle();  // 
}

// ✅ trait ：
fn store_handlers(handlers: Vec<Box<dyn Handler>>) {
    //  handlers
}

// ✅  impl Trait 
fn create_handler() -> impl Handler {
    ConcreteHandler::new()
}
```

---

## Rust Review Checklist

### 

****
- [ ] 
- [ ] 
- [ ] 

**API **
- [ ]  API 
- [ ] 
- [ ] 

### 

- [ ] clone() ，
- [ ] Arc<Mutex<T>> ？
- [ ] RefCell 
- [ ] 
- [ ]  Cow 

### Unsafe （）

- [ ]  unsafe  SAFETY 
- [ ] unsafe fn  # Safety 
- [ ] ，
- [ ] 
- [ ] unsafe 
- [ ]  safe 

### /

- [ ]  async （std::fs、thread::sleep）
- [ ]  .await  std::sync 
- [ ] spawn  'static
- [ ] 
- [ ] Channel 

### 

- [ ] select!  Future 
- [ ]  async 
- [ ] 
- [ ]  tokio::pin!  Future

### spawn vs await

- [ ] spawn 
- [ ]  await， spawn
- [ ] spawn  JoinHandle 
- [ ] 
- [ ]  join!/try_join! 

### 

- [ ] ：thiserror 
- [ ] ：anyhow + context
- [ ]  unwrap/expect
- [ ] 
- [ ] must_use 
- [ ]  #[source] 

### 

- [ ]  collect()
- [ ] 
- [ ]  with_capacity  write!
- [ ] impl Trait vs Box<dyn Trait> 
- [ ] 
- [ ]  Cow 

### 

- [ ] cargo clippy 
- [ ] cargo fmt 
- [ ] 
- [ ] 
- [ ]  API 
