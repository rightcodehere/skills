# Java Code Review Guide

Java ：Java 17/21 、Spring Boot 3 、（）、JPA 。

## 

- [ Java  (17/21+)](#-java--1721)
- [Stream API & Optional](#stream-api--optional)
- [Spring Boot ](#spring-boot-)
- [JPA  ](#jpa--)
- [](#)
- [Lombok ](#lombok-)
- [](#)
- [](#)
- [Review Checklist](#review-checklist)

---

##  Java  (17/21+)

### Record ()

```java
// ❌  POJO/DTO：
public class UserDto {
    private final String name;
    private final int age;

    public UserDto(String name, int age) {
        this.name = name;
        this.age = age;
    }
    // getters, equals, hashCode, toString...
}

// ✅  Record：、、
public record UserDto(String name, int age) {
    // 
    public UserDto {
        if (age < 0) throw new IllegalArgumentException("Age cannot be negative");
    }
}
```

### Switch 

```java
// ❌  Switch： break，
String type = "";
switch (obj) {
    case Integer i: // Java 16+
        type = String.format("int %d", i);
        break;
    case String s:
        type = String.format("string %s", s);
        break;
    default:
        type = "unknown";
}

// ✅ Switch ：，
String type = switch (obj) {
    case Integer i -> "int %d".formatted(i);
    case String s  -> "string %s".formatted(s);
    case null      -> "null value"; // Java 21  null
    default        -> "unknown";
};
```

###  (Text Blocks)

```java
// ❌  SQL/JSON 
String json = "{\n" +
              "  \"name\": \"Alice\",\n" +
              "  \"age\": 20\n" +
              "}";

// ✅ ：
String json = """
    {
      "name": "Alice",
      "age": 20
    }
    """;
```

---

## Stream API & Optional

###  Stream

```java
// ❌  Stream（ + ）
items.stream().forEach(item -> {
    process(item);
});

// ✅  for-each
for (var item : items) {
    process(item);
}

// ❌  Stream 
List<Dto> result = list.stream()
    .filter(...)
    .map(...)
    .peek(...)
    .sorted(...)
    .collect(...); // 

// ✅ 
var filtered = list.stream().filter(...).toList();
// ...
```

### Optional 

```java
// ❌  Optional （，）
public void process(Optional<String> name) { ... }
public class User {
    private Optional<String> email; // 
}

// ✅ Optional 
public Optional<User> findUser(String id) { ... }

// ❌  Optional  isPresent() + get()
Optional<User> userOpt = findUser(id);
if (userOpt.isPresent()) {
    return userOpt.get().getName();
} else {
    return "Unknown";
}

// ✅  API
return findUser(id)
    .map(User::getName)
    .orElse("Unknown");
```

---

## Spring Boot 

###  (DI)

```java
// ❌  (@Autowired)
// ：（），，
@Service
public class UserService {
    @Autowired
    private UserRepository userRepo;
}

// ✅  (Constructor Injection)
// ：， (Mock)， final
@Service
public class UserService {
    private final UserRepository userRepo;

    public UserService(UserRepository userRepo) {
        this.userRepo = userRepo;
    }
}
// 💡 ： Lombok @RequiredArgsConstructor ，
```

### 

```java
// ❌ 
@Service
public class PaymentService {
    private String apiKey = "sk_live_12345";
}

// ❌  @Value 
@Value("${app.payment.api-key}")
private String apiKey;

// ✅  @ConfigurationProperties 
@ConfigurationProperties(prefix = "app.payment")
public record PaymentProperties(String apiKey, int timeout, String url) {}
```

---

## JPA  

### N+1 

```java
// ❌ FetchType.EAGER  
// Entity 
@Entity
public class User {
    @OneToMany(fetch = FetchType.EAGER) // ！
    private List<Order> orders;
}

// 
List<User> users = userRepo.findAll(); // 1  SQL
for (User user : users) {
    //  Lazy， N  SQL
    System.out.println(user.getOrders().size());
}

// ✅  @EntityGraph  JOIN FETCH
@Query("SELECT u FROM User u JOIN FETCH u.orders")
List<User> findAllWithOrders();
```

### 

```java
// ❌  Controller （）
// ❌  private  @Transactional（AOP ）
@Transactional
private void saveInternal() { ... }

// ✅  Service  @Transactional
// ✅  readOnly = true ()
@Service
public class UserService {
    @Transactional(readOnly = true)
    public User getUser(Long id) { ... }

    @Transactional
    public void createUser(UserDto dto) { ... }
}
```

### Entity 

```java
// ❌  Entity  Lombok @Data
// @Data  equals/hashCode ，
@Entity
@Data
public class User { ... }

// ✅  @Getter, @Setter
// ✅  equals/hashCode ( ID)
@Entity
@Getter
@Setter
public class User {
    @Id
    private Long id;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof User)) return false;
        return id != null && id.equals(((User) o).id);
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
```

---

## 

###  (Java 21+)

```java
// ❌  I/O （）
ExecutorService executor = Executors.newFixedThreadPool(100);

// ✅  I/O （）
// Spring Boot 3.2+ ：spring.threads.virtual.enabled=true
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();

// ，（ DB 、HTTP ） OS 
```

### 

```java
// ❌ SimpleDateFormat 
private static final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");

// ✅  DateTimeFormatter (Java 8+)
private static final DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy-MM-dd");

// ❌ HashMap 
// ✅  ConcurrentHashMap
Map<String, String> cache = new ConcurrentHashMap<>();
```

---

## Lombok 

```java
// ❌  @Builder 
@Builder
public class Order {
    private String id; // 
    private String note; // 
}
//  id: Order.builder().note("hi").build();

// ✅  Builder 
//  build()  (Lombok @Builder.Default )
```

---

## 

### 

```java
// ❌  try-catch 
try {
    userService.create(user);
} catch (Exception e) {
    e.printStackTrace(); // 
    // return null; // ，
}

// ✅  + @ControllerAdvice (Spring Boot 3 ProblemDetail)
public class UserNotFoundException extends RuntimeException { ... }

@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(UserNotFoundException.class)
    public ProblemDetail handleNotFound(UserNotFoundException e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
    }
}
```

---

## 

###  vs 

```java
// ❌ 
@SpringBootTest //  Context，
public class UserServiceTest { ... }

// ✅  Mockito
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock UserRepository repo;
    @InjectMocks UserService service;

    @Test
    void shouldCreateUser() { ... }
}

// ✅  Testcontainers
@Testcontainers
@SpringBootTest
class UserRepositoryTest {
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15");
    // ...
}
```

---

## Review Checklist

### 
- [ ]  Java 17/21 （Switch , Records, ）
- [ ] （Date, Calendar, SimpleDateFormat）
- [ ]  Stream API  Collections ？
- [ ] Optional ，

### Spring Boot
- [ ]  @Autowired 
- [ ]  @ConfigurationProperties
- [ ] Controller ， Service
- [ ]  @ControllerAdvice / ProblemDetail

###  & 
- [ ]  `@Transactional(readOnly = true)`
- [ ]  N+1 （EAGER fetch ）
- [ ] Entity  @Data， equals/hashCode
- [ ] 

### 
- [ ] I/O ？
- [ ] （ConcurrentHashMap vs HashMap）
- [ ] ？ I/O 

### 
- [ ] 
- [ ] （ Slf4j， System.out）
- [ ] 
