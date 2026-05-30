# C# / .NET Code Review Guide

> C# / .NET 8 ， C# 12 、、EF Core 、ASP.NET Core 、、LINQ 。

## 

- [C# 12 ](#c-12-)
- [](#)
- [EF Core ](#ef-core-)
- [ASP.NET Core ](#aspnet-core-)
- [](#)
- [LINQ ](#linq-)
- [Review Checklist](#review-checklist)

---

## C# 12 

### Primary Constructors（ record ）

```csharp
// ❌ 
public class ProductService
{
    private readonly ProductDbContext _db;
    private readonly ILogger<ProductService> _logger;

    public ProductService(ProductDbContext db, ILogger<ProductService> logger)
    {
        _db = db;
        _logger = logger;
    }
}

// ✅ Primary Constructor——
public class ProductService(ProductDbContext db, ILogger<ProductService> logger)
{
    public async Task<Product?> GetAsync(int id)
        => await db.Products.FindAsync(id);
}

// ⚠️ ：primary constructor ，
// ⚠️ ，
public class OrderService(OrderDbContext db)
{
    private readonly OrderDbContext _db = db; // 
}
```

### Collection Expressions

```csharp
// ❌ 
int[] nums = new int[] { 1, 2, 3 };
List<string> names = new List<string> { "alice", "bob" };

// ✅ 
int[] nums = [1, 2, 3];
List<string> names = ["alice", "bob"];
Span<char> span = ['a', 'b'];

// ✅ 
int[] merged = [..nums, 4, 5];
```

### Default Lambda Parameters

```csharp
// ❌  lambda
var add = (int a, int b) => a + b;
var addDefault = (int a) => a + 1;

// ✅ 
var add = (int a, int b = 1) => a + b;
```

---

## 

### Task.Wait() / .Result / async void 

```csharp
// ❌ Task.Wait() —— （）
public ActionResult<Data> Get(int id)
{
    var data = _service.GetDataAsync(id).Result; // ！
    return Ok(data);
}

// ❌ async void —— ，
public async void HandleEvent()
{
    await _service.ProcessAsync(); // 
}

// ✅ async Task —— 
public async Task<ActionResult<Data>> Get(int id)
{
    var data = await _service.GetDataAsync(id);
    return Ok(data);
}
```

### ConfigureAwait(false) 

```csharp
// ❌  SynchronizationContext
public class LibraryService
{
    public async Task<string> GetDataAsync()
    {
        var response = await _httpClient.GetAsync("/api/data");
        return await response.Content.ReadAsStringAsync();
    }
}

// ✅  ConfigureAwait(false) 
public class LibraryService
{
    public async Task<string> GetDataAsync()
    {
        var response = await _httpClient.GetAsync("/api/data").ConfigureAwait(false);
        return await response.Content.ReadAsStringAsync().ConfigureAwait(false);
    }
}
```

### CancellationToken 

```csharp
// ❌  CancellationToken
public async Task<List<User>> SearchAsync(string query)
{
    return await _db.Users.Where(u => u.Name.Contains(query)).ToListAsync();
}

// ✅  CancellationToken
public async Task<List<User>> SearchAsync(string query, CancellationToken ct = default)
{
    return await _db.Users
        .Where(u => u.Name.Contains(query))
        .ToListAsync(ct);
}
```

### Async Disposal

```csharp
// ❌  dispose 
public class DataClient : IDisposable
{
    public void Dispose()
    {
        _httpClient.Dispose(); // 
    }
}

// ✅ IAsyncDisposable
public class DataClient : IAsyncDisposable
{
    public async ValueTask DisposeAsync()
    {
        await _stream.DisposeAsync();
    }
}

// ✅  await using
await using var client = new DataClient();
```

---

## EF Core 

### N+1 

```csharp
// ❌  N+1—— Blog  Posts
foreach (var blog in await context.Blogs.ToListAsync())
{
    foreach (var post in blog.Posts) // ！
    {
        Console.WriteLine(post.Title);
    }
}

// ✅ Eager Loading + 
await foreach (var blog in context.Blogs
    .Select(b => new { b.Url, b.Posts })
    .AsAsyncEnumerable())
{
    foreach (var post in blog.Posts)
        Console.WriteLine(post.Title);
}
```

### （）

```csharp
// ❌ —— Url 
var urls = await context.Blogs.ToListAsync();

// ✅ 
var urls = await context.Blogs
    .Select(b => b.Url)
    .ToListAsync();
```

### 

```csharp
// ❌ 
var posts = await context.Posts
    .Where(p => p.Title.StartsWith("A"))
    .ToListAsync(); // ！

// ✅ 
var posts = await context.Posts
    .Where(p => p.Title.StartsWith("A"))
    .OrderBy(p => p.Id)
    .Skip((page - 1) * pageSize)
    .Take(pageSize)
    .ToListAsync();
```

### Cartesian Explosion（JOIN ）

```csharp
// ❌  Include 
var blogs = await context.Blogs
    .Include(b => b.Posts)
    .Include(b => b.Tags)
    .ToListAsync(); //  Blog 

// ✅  AsSplitQuery 
var blogs = await context.Blogs
    .Include(b => b.Posts)
    .Include(b => b.Tags)
    .AsSplitQuery()
    .ToListAsync();
```

###  AsNoTracking

```csharp
// ❌ ——
var products = await context.Products.ToListAsync();

// ✅ AsNoTracking—— ~30%， ~40%
var products = await context.Products
    .AsNoTracking()
    .ToListAsync();
```

### 

```csharp
// ✅ ——sargable
var posts1 = await context.Posts
    .Where(p => p.Title.StartsWith("A"))
    .ToListAsync();

// ❌ ——
var posts2 = await context.Posts
    .Where(p => p.Title.EndsWith("A"))
    .ToListAsync();

// ❌ ——
var posts3 = await context.Posts
    .Where(p => p.Title.ToLower() == "foo")
    .ToListAsync();
```

###  vs 

```csharp
// ❌ ——
var products = context.Products.ToList();
context.SaveChanges();

// ✅ 
var products = await context.Products.ToListAsync();
await context.SaveChangesAsync();
```

---

## ASP.NET Core 

### HttpClient 

```csharp
// ❌  HttpClient——socket 
using var client = new HttpClient();
var response = await client.GetAsync("https://api.example.com/data");

// ✅ IHttpClientFactory 
public class MyService
{
    private readonly HttpClient _client;
    public MyService(HttpClient client) => _client = client; // 
}
```

### HttpContext 

```csharp
// ❌  scoped ——
_ = Task.Run(async () =>
{
    await context.SaveChangesAsync(); // ObjectDisposedException!
});

// ✅  scope
_ = Task.Run(async () =>
{
    await using var scope = serviceScopeFactory.CreateAsyncScope();
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    await db.SaveChangesAsync();
});
```

### Request.Form 

```csharp
// ❌  Form——sync over async
var form = HttpContext.Request.Form;

// ✅ 
var form = await HttpContext.Request.ReadFormAsync();
```

### 

```csharp
// ❌ —— 10-100 
try
{
    var user = await _db.Users.FirstAsync(u => u.Id == id);
}
catch (InvalidOperationException)
{
    return NotFound();
}

// ✅ 
var user = await _db.Users.FirstOrDefaultAsync(u => u.Id == id);
if (user is null) return NotFound();
```

###  Body 

```csharp
// ❌ body  header——
await next(context);
context.Response.Headers["X-Custom"] = "value"; // ！

// ✅  OnStarting 
context.Response.OnStarting(() =>
{
    context.Response.Headers["X-Custom"] = "value";
    return Task.CompletedTask;
});
await next(context);
```

---

## 

### Scoped  Singleton

```csharp
// ❌ Scoped  Singleton——
services.AddSingleton<BackgroundWorker>();
services.AddScoped<IUserRepository, UserRepository>();

// BackgroundWorker  Singleton，UserRepository  Scoped
// → UserRepository 

// ✅  Singleton  IServiceProvider  scope
public class BackgroundWorker : BackgroundService
{
    private readonly IServiceScopeFactory _scopeFactory;

    public BackgroundWorker(IServiceScopeFactory scopeFactory)
        => _scopeFactory = scopeFactory;

    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        await using var scope = _scopeFactory.CreateAsyncScope();
        var repo = scope.ServiceProvider.GetRequiredService<IUserRepository>();
    }
}
```

---

## LINQ 

### ToList  LINQ

```csharp
// ❌  ToList ——
var results = context.Posts
    .Where(p => p.Title.StartsWith("A"))
    .ToList()
    .Where(p => SomeClientFilter(p)); // ，

// ✅ 
var results = await context.Posts
    .Where(p => p.Title.StartsWith("A") && SomeDbFilter(p))
    .AsAsyncEnumerable()
    .Where(p => SomeClientFilter(p)) // 
    .ToListAsync();
```

### Count() vs Any()

```csharp
// ❌ Count() 
if (context.Users.Count() > 0) { /* ... */ }

// ✅ Any() ——
if (await context.Users.AnyAsync()) { /* ... */ }
```

###  IEnumerable

```csharp
// ❌ IEnumerable 
public void Process(IEnumerable<int> numbers)
{
    if (numbers.Any()) // 
    {
        foreach (var n in numbers) // （）
        {
            Console.WriteLine(n);
        }
    }
}

// ✅ ，
public void Process(IEnumerable<int> numbers)
{
    var list = numbers.ToList(); // 
    if (list.Any())
    {
        foreach (var n in list)
        {
            Console.WriteLine(n);
        }
    }
}
```

### Select 

```csharp
// ❌ Select ——
var results = users.Select(u =>
{
    _logger.LogInformation($"Processing {u.Name}"); // ！
    return u.Email;
}).ToList();

// ✅  foreach 
foreach (var user in users)
{
    _logger.LogInformation("Processing {Name}", user.Name);
}
var results = users.Select(u => u.Email).ToList();
```

---

## Review Checklist

### C# 12 

- [ ] Primary constructor 
- [ ] （）

### 

- [ ]  `Task.Wait()`、`.Result`、`async void`
- [ ]  `ConfigureAwait(false)`
- [ ] `CancellationToken` 
- [ ]  `IAsyncDisposable` / `await using`
- [ ] 

### EF Core

- [ ]  N+1 （）
- [ ]  `Select()` 
- [ ] ：`ToListAsync()`  `Take()`/`Skip()`
- [ ]  `Include()`  `AsSplitQuery()`
- [ ]  `AsNoTracking()`
- [ ] 
- [ ] 

### ASP.NET Core

- [ ] HttpClient  `IHttpClientFactory` 
- [ ]  scoped 
- [ ]  `ReadFormAsync`  `Request.Form`
- [ ] 
- [ ]  `OnStarting` 

### 

- [ ] Scoped  Singleton
- [ ]  scope

### LINQ

- [ ]  `ToList()`  LINQ
- [ ] `Any()`  `Count() > 0`
- [ ] IEnumerable （）
- [ ] Select 
