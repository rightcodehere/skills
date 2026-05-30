# Go 

 Go 、Effective Go 。

## 

### 
- [ ] （、）
- [ ] goroutine （）
- [ ] context 
- [ ] （/）
- [ ]  `gofmt` 

### 
- [ ] （Go < 1.22）
- [ ] nil 
- [ ] map 
- [ ] defer 
- [ ] （shadowing）

---

## 1. 

### 1.1 

```go
// ❌ ：
result, _ := SomeFunction()

// ✅ ：
result, err := SomeFunction()
if err != nil {
    return fmt.Errorf("some function failed: %w", err)
}
```

### 1.2 

```go
// ❌ ：
if err != nil {
    return err
}

// ❌ ： %v 
if err != nil {
    return fmt.Errorf("failed: %v", err)
}

// ✅ ： %w 
if err != nil {
    return fmt.Errorf("failed to process user %d: %w", userID, err)
}
```

### 1.3  errors.Is  errors.As

```go
// ❌ ：（）
if err == sql.ErrNoRows {
    // ...
}

// ✅ ： errors.Is（）
if errors.Is(err, sql.ErrNoRows) {
    return nil, ErrNotFound
}

// ✅ ： errors.As 
var pathErr *os.PathError
if errors.As(err, &pathErr) {
    log.Printf("path error: %s", pathErr.Path)
}
```

### 1.4 

```go
// ✅ ： sentinel 
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
)

// ✅ ：
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on %s: %s", e.Field, e.Message)
}
```

### 1.5 

```go
// ❌ ：（）
if err != nil {
    log.Printf("error: %v", err)
    return err
}

// ✅ ：，
if err != nil {
    return fmt.Errorf("operation failed: %w", err)
}

// ✅ ：（）
if err != nil {
    log.Printf("non-critical error: %v", err)
    // 
}
```

---

## 2.  Goroutine

### 2.1  Goroutine 

```go
// ❌ ：goroutine 
func bad() {
    ch := make(chan int)
    go func() {
        val := <-ch // ，
        fmt.Println(val)
    }()
    // ，goroutine 
}

// ✅ ： context  done channel
func good(ctx context.Context) {
    ch := make(chan int)
    go func() {
        select {
        case val := <-ch:
            fmt.Println(val)
        case <-ctx.Done():
            return // 
        }
    }()
}
```

### 2.2 Channel 

```go
// ❌ ： nil channel （）
var ch chan int
ch <- 1 // 

// ❌ ： channel （panic）
close(ch)
ch <- 1 // panic!

// ✅ ： channel
func producer(ch chan<- int) {
    defer close(ch) // 
    for i := 0; i < 10; i++ {
        ch <- i
    }
}

// ✅ ：
for val := range ch {
    process(val)
}
// 
val, ok := <-ch
if !ok {
    // channel 
}
```

### 2.3  sync.WaitGroup

```go
// ❌ ：Add  goroutine 
var wg sync.WaitGroup
for i := 0; i < 10; i++ {
    go func() {
        wg.Add(1) // ！
        defer wg.Done()
        work()
    }()
}
wg.Wait()

// ✅ ：Add  goroutine 
var wg sync.WaitGroup
for i := 0; i < 10; i++ {
    wg.Add(1)
    go func() {
        defer wg.Done()
        work()
    }()
}
wg.Wait()
```

### 2.4 （Go < 1.22）

```go
// ❌ （Go < 1.22）：
for _, item := range items {
    go func() {
        process(item) //  goroutine  item
    }()
}

// ✅ ：
for _, item := range items {
    go func(it Item) {
        process(it)
    }(item)
}

// ✅ Go 1.22+：，
```

### 2.5 Worker Pool 

```go
// ✅ ：
func processWithWorkerPool(ctx context.Context, items []Item, workers int) error {
    jobs := make(chan Item, len(items))
    results := make(chan error, len(items))

    //  worker
    for w := 0; w < workers; w++ {
        go func() {
            for item := range jobs {
                results <- process(item)
            }
        }()
    }

    // 
    for _, item := range items {
        jobs <- item
    }
    close(jobs)

    // 
    for range items {
        if err := <-results; err != nil {
            return err
        }
    }
    return nil
}
```

---

## 3. Context 

### 3.1 Context 

```go
// ❌ ：context 
func Process(data []byte, ctx context.Context) error

// ❌ ：context  struct 
type Service struct {
    ctx context.Context // ！
}

// ✅ ：context ， ctx
func Process(ctx context.Context, data []byte) error
```

### 3.2  Context

```go
// ❌ ： context
func middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        ctx := context.Background() //  context！
        process(ctx)
        next.ServeHTTP(w, r)
    })
}

// ✅ ：
func middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        ctx := r.Context()
        ctx = context.WithValue(ctx, key, value)
        process(ctx)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

### 3.3  cancel 

```go
// ❌ ： cancel
ctx, cancel := context.WithTimeout(parentCtx, 5*time.Second)
//  cancel() ，

// ✅ ： defer 
ctx, cancel := context.WithTimeout(parentCtx, 5*time.Second)
defer cancel() // 
```

### 3.4  Context 

```go
// ✅ ： context
func LongRunningTask(ctx context.Context) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err() //  context.Canceled  context.DeadlineExceeded
        default:
            // 
            if err := doChunk(); err != nil {
                return err
            }
        }
    }
}
```

### 3.5 

```go
// ✅  ctx.Err() 
if err := ctx.Err(); err != nil {
    switch {
    case errors.Is(err, context.Canceled):
        log.Println("operation was canceled")
    case errors.Is(err, context.DeadlineExceeded):
        log.Println("operation timed out")
    }
    return err
}
```

---

## 4. 

### 4.1 ，

```go
// ❌ ：
func SaveUser(db *sql.DB, user User) error

// ✅ ：（、）
type UserStore interface {
    Save(ctx context.Context, user User) error
}

func SaveUser(store UserStore, user User) error

// ❌ ：
func NewUserService() UserServiceInterface

// ✅ ：
func NewUserService(store UserStore) *UserService
```

### 4.2 

```go
// ❌ ：
// package database
type Database interface {
    Query(ctx context.Context, query string) ([]Row, error)
    // ... 20 
}

// ✅ ：
// package userservice
type UserQuerier interface {
    QueryUsers(ctx context.Context, filter Filter) ([]User, error)
}
```

### 4.3 

```go
// ❌ ：
type Repository interface {
    GetUser(id int) (*User, error)
    CreateUser(u *User) error
    UpdateUser(u *User) error
    DeleteUser(id int) error
    GetOrder(id int) (*Order, error)
    CreateOrder(o *Order) error
    // ... 
}

// ✅ ：
type UserReader interface {
    GetUser(ctx context.Context, id int) (*User, error)
}

type UserWriter interface {
    CreateUser(ctx context.Context, u *User) error
    UpdateUser(ctx context.Context, u *User) error
}

// 
type UserRepository interface {
    UserReader
    UserWriter
}
```

### 4.4 

```go
// ❌ ： interface{}
func Process(data interface{}) interface{}

// ✅ ：（Go 1.18+）
func Process[T any](data T) T

// ✅ ：
type Processor interface {
    Process() Result
}
```

---

## 5. 

### 5.1 

```go
// ✅ 
func (u *User) SetName(name string) {
    u.Name = name
}

// ✅  sync.Mutex 
type SafeCounter struct {
    mu    sync.Mutex
    count int
}

func (c *SafeCounter) Inc() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

// ✅ （）
type LargeStruct struct {
    Data [1024]byte
    // ...
}

func (l *LargeStruct) Process() { /* ... */ }
```

### 5.2 

```go
// ✅ 
type Point struct {
    X, Y float64
}

func (p Point) Distance(other Point) float64 {
    return math.Sqrt(math.Pow(p.X-other.X, 2) + math.Pow(p.Y-other.Y, 2))
}

// ✅ 
type Counter int

func (c Counter) String() string {
    return fmt.Sprintf("%d", c)
}

// ✅  map、func、chan（）
type StringSet map[string]struct{}

func (s StringSet) Contains(key string) bool {
    _, ok := s[key]
    return ok
}
```

### 5.3 

```go
// ❌ ：
func (u User) GetName() string   // 
func (u *User) SetName(n string) // 

// ✅ ：，
func (u *User) GetName() string { return u.Name }
func (u *User) SetName(n string) { u.Name = n }
```

---

## 6. 

### 6.1  Slice

```go
// ❌ ：
var result []int
for i := 0; i < 10000; i++ {
    result = append(result, i) // 
}

// ✅ ：
result := make([]int, 0, 10000)
for i := 0; i < 10000; i++ {
    result = append(result, i)
}

// ✅ 
result := make([]int, 10000)
for i := 0; i < 10000; i++ {
    result[i] = i
}
```

### 6.2 

```go
// ❌ 
func NewUser() *User {
    return &User{} // 
}

// ✅ （）
func NewUser() User {
    return User{} // 
}

// 
// go build -gcflags '-m -m' ./...
```

### 6.3  sync.Pool 

```go
// ✅ ：/ sync.Pool
var bufferPool = sync.Pool{
    New: func() interface{} {
        return new(bytes.Buffer)
    },
}

func ProcessData(data []byte) string {
    buf := bufferPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufferPool.Put(buf)
    }()

    buf.Write(data)
    return buf.String()
}
```

### 6.4 

```go
// ❌ ： + 
var result string
for _, s := range strings {
    result += s // 
}

// ✅ ： strings.Builder
var builder strings.Builder
for _, s := range strings {
    builder.WriteString(s)
}
result := builder.String()

// ✅  strings.Join
result := strings.Join(strings, "")
```

### 6.5  interface{} 

```go
// ❌  interface{}
func process(data interface{}) {
    switch v := data.(type) { // 
    case int:
        // ...
    }
}

// ✅ 
func process[T int | int64 | float64](data T) {
    // ，
}
```

---

## 7. 

### 7.1 

```go
// ✅ ：
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 1, 2, 3},
        {"with zero", 0, 5, 5},
        {"negative numbers", -1, -2, -3},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

### 7.2 

```go
// ✅ ：
func TestParallel(t *testing.T) {
    tests := []struct {
        name  string
        input string
    }{
        {"test1", "input1"},
        {"test2", "input2"},
    }

    for _, tt := range tests {
        tt := tt // Go < 1.22 
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // 
            result := Process(tt.input)
            // assertions...
        })
    }
}
```

### 7.3  Mock

```go
// ✅ 
type EmailSender interface {
    Send(to, subject, body string) error
}

// 
type SMTPSender struct { /* ... */ }

//  Mock
type MockEmailSender struct {
    SendFunc func(to, subject, body string) error
}

func (m *MockEmailSender) Send(to, subject, body string) error {
    return m.SendFunc(to, subject, body)
}

func TestUserRegistration(t *testing.T) {
    mock := &MockEmailSender{
        SendFunc: func(to, subject, body string) error {
            if to != "test@example.com" {
                t.Errorf("unexpected recipient: %s", to)
            }
            return nil
        },
    }

    service := NewUserService(mock)
    // test...
}
```

### 7.4 

```go
// ✅  t.Helper() 
func assertEqual(t *testing.T, got, want interface{}) {
    t.Helper() // 
    if got != want {
        t.Errorf("got %v, want %v", got, want)
    }
}

// ✅  t.Cleanup() 
func TestWithTempFile(t *testing.T) {
    f, err := os.CreateTemp("", "test")
    if err != nil {
        t.Fatal(err)
    }
    t.Cleanup(func() {
        os.Remove(f.Name())
    })
    // test...
}
```

---

## 8. 

### 8.1 Nil Slice vs Empty Slice

```go
var nilSlice []int     // nil, len=0, cap=0
emptySlice := []int{}  // not nil, len=0, cap=0
made := make([]int, 0) // not nil, len=0, cap=0

// ✅ JSON 
json.Marshal(nilSlice)   // null
json.Marshal(emptySlice) // []

// ✅ ： JSON 
if slice == nil {
    slice = []int{}
}
```

### 8.2 Map 

```go
// ❌ ： map
var m map[string]int
m["key"] = 1 // panic: assignment to entry in nil map

// ✅ ： make 
m := make(map[string]int)
m["key"] = 1

// ✅ 
m := map[string]int{}
```

### 8.3 Defer 

```go
// ❌ ：defer 
func processFiles(files []string) error {
    for _, file := range files {
        f, err := os.Open(file)
        if err != nil {
            return err
        }
        defer f.Close() // ！
        // process...
    }
    return nil
}

// ✅ ：
func processFiles(files []string) error {
    for _, file := range files {
        if err := processFile(file); err != nil {
            return err
        }
    }
    return nil
}

func processFile(file string) error {
    f, err := os.Open(file)
    if err != nil {
        return err
    }
    defer f.Close()
    // process...
    return nil
}
```

### 8.4 Slice 

```go
// ❌ ：
original := []int{1, 2, 3, 4, 5}
slice := original[1:3] // [2, 3]
slice[0] = 100         //  original！
// original  [1, 100, 3, 4, 5]

// ✅ ：
slice := make([]int, 2)
copy(slice, original[1:3])
slice[0] = 100 //  original
```

### 8.5 

```go
// ❌ ：
func getPrefix(s string) string {
    return s[:10] //  s 
}

// ✅ ：（Go 1.18+）
func getPrefix(s string) string {
    return strings.Clone(s[:10])
}

// ✅ Go 1.18 
func getPrefix(s string) string {
    return string([]byte(s[:10]))
}
```

### 8.6 Interface Nil 

```go
// ❌ ：interface  nil 
type MyError struct{}
func (e *MyError) Error() string { return "error" }

func returnsError() error {
    var e *MyError = nil
    return e //  error  nil！
}

func main() {
    err := returnsError()
    if err != nil { // true! interface{type: *MyError, value: nil}
        fmt.Println("error:", err)
    }
}

// ✅ ： nil
func returnsError() error {
    var e *MyError = nil
    if e == nil {
        return nil //  nil
    }
    return e
}
```

### 8.7 Time 

```go
// ❌ ： ==  time.Time
if t1 == t2 { // 
    // ...
}

// ✅ ： Equal 
if t1.Equal(t2) {
    // ...
}

// ✅ 
if t1.Before(t2) || t1.After(t2) {
    // ...
}
```

---

## 9. 

### 9.1 

```go
// ❌ 
package common   // 
package utils    // 
package helpers  // 
package models   // 

// ✅ ：
package user     // 
package order    // 
package postgres // PostgreSQL 
```

### 9.2 

```go
// ❌ 
// package a imports package b
// package b imports package a

// ✅ 1：
// package types ()
// package a imports types
// package b imports types

// ✅ 2：
// package a 
// package b 
```

### 9.3 

```go
// ✅ 
type UserService struct {
    db *sql.DB // 
}

func (s *UserService) GetUser(id int) (*User, error) // 
func (s *UserService) validate(u *User) error         // 

// ✅ 
// internal/database/... 
```

---

## 10. 

### 10.1 

```bash
# （）
gofmt -w .
goimports -w .

# 
go vet ./...

# 
go test -race ./...

# 
go build -gcflags '-m -m' ./...
```

### 10.2  Linter

```bash
# golangci-lint（ linter）
golangci-lint run

# 
# - errcheck: 
# - gosec: 
# - ineffassign: 
# - staticcheck: 
# - unused: 
```

### 10.3 Benchmark 

```go
// ✅ 
func BenchmarkProcess(b *testing.B) {
    data := prepareData()
    b.ResetTimer() // 

    for i := 0; i < b.N; i++ {
        Process(data)
    }
}

//  benchmark
// go test -bench=. -benchmem ./...
```

---

## 

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
- [Go Common Mistakes](https://go.dev/wiki/CommonMistakes)
- [100 Go Mistakes](https://100go.co/)
- [Go Proverbs](https://go-proverbs.github.io/)
- [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md)
