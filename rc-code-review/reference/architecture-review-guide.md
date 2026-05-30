# Architecture Review Guide

，、。

## SOLID 

### S -  (SRP)

**：**
- /？
- ？
- ，？

**：**
```
⚠️  "And"、"Manager"、"Handler"、"Processor" 
⚠️  200-300 
⚠️  5-7 
⚠️ 
```

**：**
- "？？"
- " X ，？ Y ？"

### O -  (OCP)

**：**
- ，？
- （、）？
-  if/else  switch ？

**：**
```
⚠️ switch/if-else 
⚠️ 
⚠️  (instanceof, typeof) 
```

**：**
- " X ，？"
- " switch ？"

### L -  (LSP)

**：**
- ？
- ？
- ？

**：**
```
⚠️  (casting)
⚠️  NotImplementedException
⚠️  return
⚠️ 
```

**：**
- "，？"
- "？"

### I -  (ISP)

**：**
- ？
- ？
- ？

**：**
```
⚠️  5-7 
⚠️  NotImplementedException
⚠️  (IManager, IService)
⚠️ 
```

**：**
- "？"
- "？"

### D -  (DIP)

**：**
- ？
-  new ？
- ？

**：**
```
⚠️  new 
⚠️ /
⚠️ 
⚠️ 
```

**：**
- " mock ？"
- "/API ，？"

---

## 

### 

|  |  |  |
|--------|----------|------|
| ** (Big Ball of Mud)** | ， | 、 |
| ** (God Object)** | ，、 | ， |
| **** | ，goto ， |  |
| ** (Lava Flow)** | ， |  |

### 

|  |  |  |
|--------|----------|------|
| ** (Golden Hammer)** | / |  |
| ** (Gas Factory)** | ， | YAGNI ， |
| ** (Boat Anchor)** | "" | ， |
| **** |  |  |

### 

```markdown
🔴 [blocking] " 2000 ，"
🟡 [important] " 3 ，？"
💡 [suggestion] " switch ，"
```

---

## 

### （）

|  |  |  |
|------|------|------|
| **** ✅ |  | `calculate(price, quantity)` |
| **** ✅ |  | `processOrder(orderDTO)` |
| **** ⚠️ |  |  User  name |
| **** ⚠️ |  | `process(data, isAdmin=true)` |
| **** ❌ |  |  |
| **** ❌ |  |  |

### （）

|  |  |  |
|------|------|------|
| **** |  | ✅  |
| **** |  | ✅  |
| **** |  | ⚠️  |
| **** |  | ⚠️  |
| **** |  | ❌  |
| **** |  | ❌  |

### 

```yaml
:
  CBO ():
    : < 5
    : 5-10
    : > 10

  Ce ():
    : 
    : < 7

  Ca ():
    : 
    : ，

:
  LCOM4 ():
    1:  ✅
    2-3:  ⚠️
    >3:  ❌
```

### 

- "？？"
- "？"
- "？"

---

## 

### Clean Architecture 

```
┌─────────────────────────────────────┐
│         Frameworks & Drivers        │ ← ：Web、DB、UI
├─────────────────────────────────────┤
│         Interface Adapters          │ ← Controllers、Gateways、Presenters
├─────────────────────────────────────┤
│          Application Layer          │ ← Use Cases、Application Services
├─────────────────────────────────────┤
│            Domain Layer             │ ← Entities、Domain Services
└─────────────────────────────────────┘
          ↑  ↑
```

### 

**：**

```typescript
// ❌ ：Domain  Infrastructure
// domain/User.ts
import { MySQLConnection } from '../infrastructure/database';

// ✅ ：Domain ，Infrastructure 
// domain/UserRepository.ts ()
interface UserRepository {
  findById(id: string): Promise<User>;
}

// infrastructure/MySQLUserRepository.ts ()
class MySQLUserRepository implements UserRepository {
  findById(id: string): Promise<User> { /* ... */ }
}
```

### 

**：**
- [ ] Domain （、HTTP、）？
- [ ] Application  API？
- [ ] Controller ？
- [ ] （UI  Repository）？

**：**
- [ ] ？
- [ ] ？
- [ ] ？

### 

```markdown
🔴 [blocking] "Domain ，"
🟡 [important] "Controller ， Service "
💡 [suggestion] ""
```

---

## 

### 

|  |  |  |
|------|----------|------------|
| **Factory** | ， | ， |
| **Strategy** | ， | ， |
| **Observer** | ， |  |
| **Singleton** | ， |  |
| **Decorator** | ， | ， |

### 

```
⚠️ Patternitis（）：

1.  if/else  +  + 
2. 
3. ""
4. 
5. 
```

### 

```markdown
✅ :
- 
- 
- 

❌ :
- 
- 
-  YAGNI 
```

### 

- "？"
- "，？"
- "？"

---

## 

### 

**：**
- [ ] ？
- [ ] （hooks、plugins、events）？
- [ ] （、）？

**：**
- [ ] ？
- [ ] ？
- [ ] ？

**：**
- [ ] （）？
- [ ] （session、）？
- [ ] ？

### 

```typescript
// ✅ ：/
class OrderService {
  private hooks: OrderHooks;

  async createOrder(order: Order) {
    await this.hooks.beforeCreate?.(order);
    const result = await this.save(order);
    await this.hooks.afterCreate?.(result);
    return result;
  }
}

// ❌ ：
class OrderService {
  async createOrder(order: Order) {
    await this.sendEmail(order);        // 
    await this.updateInventory(order);  // 
    await this.notifyWarehouse(order);  // 
    return await this.save(order);
  }
}
```

### 

```markdown
💡 [suggestion] "，？"
🟡 [important] "，？"
📚 [learning] ""
```

---

## 

### 

**/（）：**
```
src/
├── user/
│   ├── User.ts           ()
│   ├── UserService.ts    ()
│   ├── UserRepository.ts ()
│   └── UserController.ts (API)
├── order/
│   ├── Order.ts
│   ├── OrderService.ts
│   └── ...
└── shared/
    ├── utils/
    └── types/
```

**（）：**
```
src/
├── controllers/     ← 
│   ├── UserController.ts
│   └── OrderController.ts
├── services/
├── repositories/
└── models/
```

### 

|  |  |  |
|------|------|------|
|  | PascalCase， | `UserService`, `OrderRepository` |
|  | camelCase， | `createUser`, `findOrderById` |
|  | I  | `IUserService`  `UserService` |
|  | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
|  |  | `_cache`  `#cache` |

### 

```yaml
:
  : < 300 
  : < 50 
  : < 200 
  : < 4 
  : < 4 

:
  - 
  - 
  - 
```

### 

```markdown
🟢 [nit] " 500 "
🟡 [important] ""
💡 [suggestion] " `process` ， `calculateOrderTotal`？"
```

---

## 

###  5 

```markdown
□ ？（）
□ ？
□ /UI/？
□  SOLID ？
□ ？
```

### （）

```markdown
🔴 God Object -  1000 
🔴  - A → B → C → A
🔴 Domain 
🔴 
🔴 
```

### （）

```markdown
🟡  (CBO) > 10
🟡  5 
🟡  4 
🟡  > 10 
🟡 
```

---

## 

|  |  |  |
|------|------|----------|
| **SonarQube** | 、 |  |
| **NDepend** | 、 | .NET |
| **JDepend** |  | Java |
| **Madge** |  | JavaScript/TypeScript |
| **ESLint** | 、 | JavaScript/TypeScript |
| **CodeScene** | 、 |  |

---

## 

- [Clean Architecture - Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SOLID Principles in Code Review - JetBrains](https://blog.jetbrains.com/upsource/2015/08/31/what-to-look-for-in-a-code-review-solid-principles-2/)
- [Software Architecture Anti-Patterns](https://medium.com/@christophnissle/anti-patterns-in-software-architecture-3c8970c9c4f5)
- [Coupling and Cohesion in System Design](https://www.geeksforgeeks.org/system-design/coupling-and-cohesion-in-system-design/)
- [Design Patterns - Refactoring Guru](https://refactoring.guru/design-patterns)
