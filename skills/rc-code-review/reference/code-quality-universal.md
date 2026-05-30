# Universal Code Quality Anti-Patterns

> ，、、、、、TOCTOU、。 PR 。

## 

- [](#)
- [](#)
- [](#)
- [](#)
- [](#)
- [](#)
- [](#)
- [TOCTOU ](#toctou-)
- [](#)
- [](#)
- [](#)

---

## 

Before accepting new code, search the existing codebase for reusable utilities.

### 

```python
# ❌ —— PathBuilder
def get_config_path(name):
    base = os.environ.get("APP_ROOT", ".")
    return os.path.join(base, "config", name + ".json")

# ✅  PathBuilder
def get_config_path(name):
    return PathBuilder.config(f"{name}.json")
```

```javascript
// ❌  debounce—— lodash  utils/debounce.ts
function debounce(fn, ms) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}

// ✅ 
import { debounce } from "@/utils/debounce";
```

**：**
-  utility ？
- inline ？
-  shared/utils 

---

## 

### 

```python
# ❌ 
def create_user(name, email, role, team, active, avatar_url, timezone):
    ...

# ✅  / dataclass
@dataclass
class CreateUserParams:
    name: str
    email: str
    role: Role = Role.MEMBER
    team: str | None = None
    active: bool = True
    avatar_url: str | None = None
    timezone: str = "UTC"

def create_user(params: CreateUserParams) -> User:
    ...
```

```typescript
// ❌ 6+  positional 
function renderWidget(
  title: string, width: number, height: number,
  theme: string, collapsible: boolean, icon: string
) { ... }

// ✅ Options object pattern
interface WidgetOptions {
  title: string;
  width?: number;
  height?: number;
  theme?: "light" | "dark";
  collapsible?: boolean;
  icon?: string;
}
function renderWidget(options: WidgetOptions) { ... }
```

**：**
-  ≥ 4 ？ options object / dataclass
- ？ enum  strategy pattern
-  `enable_x`, `disable_y` ？

---

## 

### 

```python
# ❌  ORM —— SQLAlchemy
def get_users():
    return session.query(User).filter(User.active == True).all()

# ✅  domain ，
def get_active_users() -> list[UserDTO]:
    rows = user_repo.find_active()
    return [UserDTO.from_row(r) for r in rows]
```

```typescript
// ❌  API response 
<UserCard user={apiResponse.data.results[0]} />

// ✅  domain ，adapter 
interface UserSummary {
  displayName: string;
  avatarUrl: string;
}
<UserCard user={adaptUser(apiResponse)} />
```

**：**
- （ORM, HTTP client, file format）？
- /？
- ？

---

## 

### /

```python
# ❌ Magic strings 
if status == "active":
    ...
if role == "admin":
    ...

# ✅  enum
class Status(StrEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"

if user.status == Status.ACTIVE:
    ...
```

```typescript
// ❌ Raw string event names——
emitter.emit("userCreated", data);
emitter.on("usercreated", handler); // bug: typo

// ✅  branded type
const Events = {
  USER_CREATED: "userCreated",
  USER_SUSPENDED: "userSuspended",
} as const;
emitter.emit(Events.USER_CREATED, data);
```

**：**
-  enum/union type？
- 、action type、status ？
-  case-sensitive ？

---

## 

###  if/else

```python
# ❌ 
label = (
    "Admin" if role == "admin" else
    "Manager" if role == "manager" else
    "Viewer" if role == "viewer" else
    "Unknown"
)

# ✅  match
ROLE_LABELS = {
    "admin": "Admin",
    "manager": "Manager",
    "viewer": "Viewer",
}
label = ROLE_LABELS.get(role, "Unknown")
```

```typescript
// ❌ 
const bg = isHovered
  ? isSelected ? "blue" : "gray"
  : isSelected ? "navy" : "white";

// ✅ （lookup map）
const bgMap: Record<string, string> = {
  "true-true": "blue",
  "true-false": "gray",
  "false-true": "navy",
  "false-false": "white",
};
const bg = bgMap[`${isHovered}-${isSelected}`];
```

```python
# ❌  if 3+ 
def process(order):
    if order is not None:
        if order.items:
            for item in order.items:
                if item.price > 0:
                    ...

# ✅ Early return + guard clauses
def process(order):
    if not order or not order.items:
        return
    for item in order.items:
        if item.price <= 0:
            continue
        ...
```

**：**
-  ≥ 2 ？
- if/else  ≥ 3 ？
-  lookup table、early return  match ？

---

## 

### 

```python
# ❌ ，
def format_user(user):
    return f"{user.first_name} {user.last_name} ({user.email})"

def format_employee(emp):
    return f"{emp.first_name} {emp.last_name} ({emp.work_email})"

# ✅ 
def format_person(first: str, last: str, email: str) -> str:
    return f"{first} {last} ({email})"
```

```typescript
// ❌ Copy-paste handler  URL
async function deletePost(id: string) {
  await fetch(`/api/posts/${id}`, { method: "DELETE" });
  router.push("/posts");
}
async function deleteComment(id: string) {
  await fetch(`/api/comments/${id}`, { method: "DELETE" });
  router.push("/comments");
}

// ✅ 
async function deleteResource(resource: string, id: string) {
  await fetch(`/api/${resource}/${id}`, { method: "DELETE" });
  router.push(`/${resource}`);
}
```

**：**
-  ≥ 2 /URL/？
- ？
-  template method  strategy ？

---

## 

### 

```typescript
// ❌  poll  update——
useEffect(() => {
  const interval = setInterval(() => {
    fetch("/api/status").then(r => r.json()).then(setStatus);
  }, 5000);
  return () => clearInterval(interval);
}, []);

// ✅ 
useEffect(() => {
  const interval = setInterval(() => {
    fetch("/api/status")
      .then(r => r.json())
      .then(data => {
        setStatus(prev => isEqual(prev, data) ? prev : data);
      });
  }, 5000);
  return () => clearInterval(interval);
}, []);
```

```python
# ❌  loop  DB——
for item in items:
    item.status = compute_status(item)
    session.commit()

# ✅ 
for item in items:
    new_status = compute_status(item)
    if item.status != new_status:
        item.status = new_status
        session.commit()
```

**：**
- polling / interval / event handler ？
- wrapper function  same-reference return？
- DB ？

---

## TOCTOU 

### Time-of-Check-to-Time-of-Use

```python
# ❌ ——/
if os.path.exists(path):
    with open(path) as f:
        data = f.read()

# ✅  + 
try:
    with open(path) as f:
        data = f.read()
except FileNotFoundError:
    data = None
```

```python
# ❌  →  
if account.balance >= amount:
    account.balance -= amount

# ✅ 
with account.lock:
    if account.balance < amount:
        raise InsufficientFundsError()
    account.balance -= amount
```

```typescript
// ❌ Check-then-act  async 
if (!fileExists(path)) {
  await writeFile(path, content);
}

// ✅  + catch
try {
  await writeFile(path, content, { flag: "wx" });
} catch (e) {
  if (e.code === "EEXIST") { /* handle */ }
  else throw e;
}
```

**：**
- `if exists → operate`  `try operate → catch`？
- /？
- async  check  act  await？

---

## 

### 

```python
# ❌ 
content = Path("log.txt").read_text()
first_line = content.split("\n")[0]

# ✅ 
first_line = Path("log.txt").read_text().split("\n", 1)[0]
# ：
with open("log.txt") as f:
    first_line = f.readline()
```

```typescript
// ❌  items 
const allItems = await db.query("SELECT * FROM orders");
const pending = allItems.filter(o => o.status === "pending");

// ✅ 
const pending = await db.query(
  "SELECT * FROM orders WHERE status = ?", ["pending"]
);
```

```python
# ❌ 
users = list(User.objects.all())
user = next(u for u in users if u.id == user_id)

# ✅ 
user = User.objects.get(id=user_id)
```

**：**
- /？
- /？
- API  pagination/limit ？

---

## 

### 

```typescript
// ❌  fullName  firstName + lastName
interface User {
  firstName: string;
  lastName: string;
  fullName: string;  // redundant
}

// ✅ fullName 
interface User {
  firstName: string;
  lastName: string;
}
const fullName = `${user.firstName} ${user.lastName}`;
```

```python
# ❌ 
class Order:
    total: float
    item_count: int       # redundant if len(items) gives the same
    items: list[Item]

# ✅  property
class Order:
    items: list[Item]

    @property
    def total(self) -> float:
        return sum(item.price for item in self.items)

    @property
    def item_count(self) -> int:
        return len(self.items)
```

**：**
- ？
-  invalidation ？
- observer/effect ？

---

## 

- [ ] ****:  utility/helper，？
- [ ] ****:  ≤ 3 ？ options object / dataclass？
- [ ] ****: （ORM、HTTP client、file format）？
- [ ] ****:  magic strings  enum/constant/union type？
- [ ] ****:  ≤ 1 ？if/else  ≤ 2 ？
- [ ] **DRY**:  copy-paste-with-variation（≥ 2 ）？
- [ ] ****: polling / interval / event handler  change-detection guard？
- [ ] **TOCTOU**: `if exists → operate`  `try operate → catch`？
- [ ] ****: /？
- [ ] ****: ？
