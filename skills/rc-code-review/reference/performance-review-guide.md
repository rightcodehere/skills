# Performance Review Guide

，、、、 API 。

## 

- [ (Core Web Vitals)](#-core-web-vitals)
- [JavaScript ](#javascript-)
- [](#)
- [](#)
- [API ](#api-)
- [](#)
- [](#)

---

##  (Core Web Vitals)

### 2024 

|  |  |  |  |
|------|------|--------|------|
| **LCP** | Largest Contentful Paint | ≤ 2.5s |  |
| **INP** | Interaction to Next Paint | ≤ 200ms | （2024  FID）|
| **CLS** | Cumulative Layout Shift | ≤ 0.1 |  |
| **FCP** | First Contentful Paint | ≤ 1.8s |  |
| **TBT** | Total Blocking Time | ≤ 200ms |  |

### LCP 

```javascript
// ❌ LCP  - 
<img src="hero.jpg" loading="lazy" />

// ✅ LCP 
<img src="hero.jpg" fetchpriority="high" />

// ❌ 
<img src="hero.png" />  // PNG 

// ✅  + 
<picture>
  <source srcset="hero.avif" type="image/avif" />
  <source srcset="hero.webp" type="image/webp" />
  <img src="hero.jpg" alt="Hero" />
</picture>
```

**：**
- [ ] LCP  `fetchpriority="high"`？
- [ ]  WebP/AVIF ？
- [ ] ？
- [ ] CDN ？

### FCP 

```html
<!-- ❌  CSS -->
<link rel="stylesheet" href="all-styles.css" />

<!-- ✅  CSS  +  -->
<style>/*  */</style>
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'" />

<!-- ❌  -->
@font-face {
  font-family: 'CustomFont';
  src: url('font.woff2');
}

<!-- ✅  -->
@font-face {
  font-family: 'CustomFont';
  src: url('font.woff2');
  font-display: swap;  /* ， */
}
```

### INP 

```javascript
// ❌ 
button.addEventListener('click', () => {
  //  500ms 
  processLargeData(data);
  updateUI();
});

// ✅ 
button.addEventListener('click', async () => {
  // 
  await scheduler.yield?.() ?? new Promise(r => setTimeout(r, 0));

  // 
  for (const chunk of chunks) {
    processChunk(chunk);
    await scheduler.yield?.();
  }
  updateUI();
});

// ✅  Web Worker 
const worker = new Worker('heavy-computation.js');
worker.postMessage(data);
worker.onmessage = (e) => updateUI(e.data);
```

### CLS 

```css
/* ❌  */
img { width: 100%; }

/* ✅  */
img {
  width: 100%;
  aspect-ratio: 16 / 9;
}

/* ❌  */
.ad-container { }

/* ✅  */
.ad-container {
  min-height: 250px;
}
```

**CLS ：**
- [ ] / width/height  aspect-ratio？
- [ ]  `font-display: swap`？
- [ ] ？
- [ ] ？

---

## JavaScript 

### 

```javascript
// ❌ 
import { HeavyChart } from './charts';
import { PDFExporter } from './pdf';
import { AdminPanel } from './admin';

// ✅ 
const HeavyChart = lazy(() => import('./charts'));
const PDFExporter = lazy(() => import('./pdf'));

// ✅ 
const routes = [
  {
    path: '/dashboard',
    component: lazy(() => import('./pages/Dashboard')),
  },
  {
    path: '/admin',
    component: lazy(() => import('./pages/Admin')),
  },
];
```

### Bundle 

```javascript
// ❌ 
import _ from 'lodash';
import moment from 'moment';

// ✅ 
import debounce from 'lodash/debounce';
import { format } from 'date-fns';

// ❌  Tree Shaking
export default {
  fn1() {},
  fn2() {},  // 
};

// ✅  Tree Shaking
export function fn1() {}
export function fn2() {}
```

**Bundle ：**
- [ ]  import() ？
- [ ] ？
- [ ]  bundle ？（webpack-bundle-analyzer）
- [ ] ？

### 

```javascript
// ❌ 
function List({ items }) {
  return (
    <ul>
      {items.map(item => <li key={item.id}>{item.name}</li>)}
    </ul>
  );  // 10000  = 10000  DOM 
}

// ✅  - 
import { FixedSizeList } from 'react-window';

function VirtualList({ items }) {
  return (
    <FixedSizeList
      height={400}
      itemCount={items.length}
      itemSize={35}
    >
      {({ index, style }) => (
        <div style={style}>{items[index].name}</div>
      )}
    </FixedSizeList>
  );
}
```

**：**
- [ ]  100 ？
- [ ] ？
- [ ] ？

---

## 

### 

#### 1. 

```javascript
// ❌ 
useEffect(() => {
  window.addEventListener('resize', handleResize);
}, []);

// ✅ 
useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

#### 2. 

```javascript
// ❌ 
useEffect(() => {
  setInterval(fetchData, 5000);
}, []);

// ✅ 
useEffect(() => {
  const timer = setInterval(fetchData, 5000);
  return () => clearInterval(timer);
}, []);
```

#### 3. 

```javascript
// ❌ 
function createHandler() {
  const largeData = new Array(1000000).fill('x');

  return function handler() {
    // largeData ，
    console.log(largeData.length);
  };
}

// ✅ 
function createHandler() {
  const largeData = new Array(1000000).fill('x');
  const length = largeData.length;  // 

  return function handler() {
    console.log(length);
  };
}
```

#### 4. 

```javascript
// ❌ WebSocket/EventSource 
useEffect(() => {
  const ws = new WebSocket('wss://...');
  ws.onmessage = handleMessage;
}, []);

// ✅ 
useEffect(() => {
  const ws = new WebSocket('wss://...');
  ws.onmessage = handleMessage;
  return () => ws.close();
}, []);
```

### 

```markdown
- [ ] useEffect ？
- [ ] ？
- [ ] ？
- [ ] WebSocket/SSE ？
- [ ] ？
- [ ] ？
```

### 

|  |  |
|------|------|
| Chrome DevTools Memory |  |
| MemLab (Meta) |  |
| Performance Monitor |  |

---

## 

### N+1 

```python
# ❌ N+1  - 1 + N 
users = User.objects.all()  # 1 
for user in users:
    print(user.profile.bio)  # N （）

# ✅ Eager Loading - 2 
users = User.objects.select_related('profile').all()
for user in users:
    print(user.profile.bio)  # 

# ✅  prefetch_related
posts = Post.objects.prefetch_related('tags').all()
```

```javascript
// TypeORM 
// ❌ N+1 
const users = await userRepository.find();
for (const user of users) {
  const posts = await user.posts;  // 
}

// ✅ Eager Loading
const users = await userRepository.find({
  relations: ['posts'],
});
```

### 

```sql
-- ❌ 
SELECT * FROM orders WHERE status = 'pending';

-- ✅ 
CREATE INDEX idx_orders_status ON orders(status);

-- ❌ ：
SELECT * FROM users WHERE YEAR(created_at) = 2024;

-- ✅ 
SELECT * FROM users
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';

-- ❌ ：LIKE 
SELECT * FROM products WHERE name LIKE '%phone%';

-- ✅ 
SELECT * FROM products WHERE name LIKE 'phone%';
```

### 

```sql
-- ❌ SELECT * 
SELECT * FROM users WHERE id = 1;

-- ✅ 
SELECT id, name, email FROM users WHERE id = 1;

-- ❌  LIMIT
SELECT * FROM logs WHERE type = 'error';

-- ✅ 
SELECT * FROM logs WHERE type = 'error' LIMIT 100 OFFSET 0;

-- ❌ 
for id in user_ids:
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))

-- ✅ 
cursor.execute("SELECT * FROM users WHERE id IN %s", (tuple(user_ids),))
```

### 

```markdown
🔴 :
- [ ]  N+1 ？
- [ ] WHERE ？
- [ ]  SELECT *？
- [ ]  LIMIT？

🟡 :
- [ ]  EXPLAIN ？
- [ ] ？
- [ ] ？
- [ ] ？
```

---

## API 

### 

```javascript
// ❌ 
app.get('/users', async (req, res) => {
  const users = await User.findAll();  //  100000 
  res.json(users);
});

// ✅  + 
app.get('/users', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = Math.min(parseInt(req.query.limit) || 20, 100);  //  100
  const offset = (page - 1) * limit;

  const { rows, count } = await User.findAndCountAll({
    limit,
    offset,
    order: [['id', 'ASC']],
  });

  res.json({
    data: rows,
    pagination: {
      page,
      limit,
      total: count,
      totalPages: Math.ceil(count / limit),
    },
  });
});
```

### 

```javascript
// ✅ Redis 
async function getUser(id) {
  const cacheKey = `user:${id}`;

  // 1. 
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // 2. 
  const user = await db.users.findById(id);

  // 3. （）
  await redis.setex(cacheKey, 3600, JSON.stringify(user));

  return user;
}

// ✅ HTTP 
app.get('/static-data', (req, res) => {
  res.set({
    'Cache-Control': 'public, max-age=86400',  // 24 
    'ETag': 'abc123',
  });
  res.json(data);
});
```

### 

```javascript
// ✅  Gzip/Brotli 
const compression = require('compression');
app.use(compression());

// ✅ 
// : GET /users?fields=id,name,email
app.get('/users', async (req, res) => {
  const fields = req.query.fields?.split(',') || ['id', 'name'];
  const users = await User.findAll({
    attributes: fields,
  });
  res.json(users);
});
```

### 

```javascript
// ✅ 
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 60 * 1000,  // 1 
  max: 100,             //  100 
  message: { error: 'Too many requests, please try again later.' },
});

app.use('/api/', limiter);
```

### API 

```markdown
- [ ] ？
- [ ] ？
- [ ] ？
- [ ] ？
- [ ] ？
- [ ] ？
```

---

## 

### 

|  |  | 10  | 1000  | 100  |  |
|--------|------|-------|---------|----------|------|
| O(1) |  | 1 | 1 | 1 |  |
| O(log n) |  | 3 | 10 | 20 |  |
| O(n) |  | 10 | 1000 | 100  |  |
| O(n log n) |  | 33 | 10000 | 2000  |  |
| O(n²) |  | 100 | 100  | 1  |  |
| O(2ⁿ) |  | 1024 | ∞ | ∞ |  |

### 

```javascript
// ❌ O(n²) - 
function findDuplicates(arr) {
  const duplicates = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) {
        duplicates.push(arr[i]);
      }
    }
  }
  return duplicates;
}

// ✅ O(n) -  Set
function findDuplicates(arr) {
  const seen = new Set();
  const duplicates = new Set();
  for (const item of arr) {
    if (seen.has(item)) {
      duplicates.add(item);
    }
    seen.add(item);
  }
  return [...duplicates];
}
```

```javascript
// ❌ O(n²) -  includes
function removeDuplicates(arr) {
  const result = [];
  for (const item of arr) {
    if (!result.includes(item)) {  // includes  O(n)
      result.push(item);
    }
  }
  return result;
}

// ✅ O(n) -  Set
function removeDuplicates(arr) {
  return [...new Set(arr)];
}
```

```javascript
// ❌ O(n)  - 
const users = [{ id: 1, name: 'A' }, { id: 2, name: 'B' }, ...];

function getUser(id) {
  return users.find(u => u.id === id);  // O(n)
}

// ✅ O(1)  -  Map
const userMap = new Map(users.map(u => [u.id, u]));

function getUser(id) {
  return userMap.get(id);  // O(1)
}
```

### 

```javascript
// ⚠️ O(n)  - 
const doubled = arr.map(x => x * 2);

// ✅ O(1)  - （）
for (let i = 0; i < arr.length; i++) {
  arr[i] *= 2;
}

// ⚠️ 
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);  // O(n) 
}

// ✅  O(1) 
function factorial(n) {
  let result = 1;
  for (let i = 2; i <= n; i++) {
    result *= i;
  }
  return result;
}
```

### 

```markdown
💡 " O(n²)，"
🔴 " Array.includes() ， O(n²)， Set"
🟡 "，"
```

---

## 

### 🔴 （）

**：**
- [ ] LCP ？（）
- [ ]  `transition: all`？
- [ ]  width/height/top/left？
- [ ]  >100 ？

**：**
- [ ]  N+1 ？
- [ ] ？
- [ ]  SELECT * ？

**：**
- [ ]  O(n²) ？
- [ ] useEffect/？

### 🟡 （）

**：**
- [ ] ？
- [ ] ？
- [ ]  WebP/AVIF？
- [ ] ？

**：**
- [ ] ？
- [ ] WHERE ？
- [ ] ？

**API：**
- [ ] ？
- [ ] ？
- [ ] ？

### 🟢 （）

- [ ]  bundle ？
- [ ]  CDN？
- [ ] ？
- [ ] ？

---

## 

### 

|  |  |  |  |
|------|-----|--------|-----|
| LCP | ≤ 2.5s | 2.5-4s | > 4s |
| INP | ≤ 200ms | 200-500ms | > 500ms |
| CLS | ≤ 0.1 | 0.1-0.25 | > 0.25 |
| FCP | ≤ 1.8s | 1.8-3s | > 3s |
| Bundle Size (JS) | < 200KB | 200-500KB | > 500KB |

### 

|  |  |  |  |
|------|-----|--------|-----|
| API  | < 100ms | 100-500ms | > 500ms |
|  | < 50ms | 50-200ms | > 200ms |
|  | < 3s | 3-5s | > 5s |

---

## 

### 

|  |  |
|------|------|
| [Lighthouse](https://developer.chrome.com/docs/lighthouse/) | Core Web Vitals  |
| [WebPageTest](https://www.webpagetest.org/) |  |
| [webpack-bundle-analyzer](https://github.com/webpack-contrib/webpack-bundle-analyzer) | Bundle  |
| [Chrome DevTools Performance](https://developer.chrome.com/docs/devtools/performance/) |  |

### 

|  |  |
|------|------|
| [MemLab](https://github.com/facebookincubator/memlab) |  |
| Chrome Memory Tab |  |

### 

|  |  |
|------|------|
| EXPLAIN |  |
| [pganalyze](https://pganalyze.com/) | PostgreSQL  |
| [New Relic](https://newrelic.com/) / [Datadog](https://www.datadoghq.com/) | APM  |

---

## 

，。 [common-bugs-checklist.md](common-bugs-checklist.md) 。

### 

- [ ]  /  request/render ？
- [ ]  / （loop-invariant）？
- [ ] ？

```typescript
// ❌ loop-invariant 
for (const path of paths) {
  const config = JSON.parse(fs.readFileSync("config.json", "utf-8"));
  processFile(path, config);
}

// ✅ 
const config = JSON.parse(fs.readFileSync("config.json", "utf-8"));
for (const path of paths) processFile(path, config);
```

### 

- [ ]  async  `await`？
- [ ]  `Promise.all` / `asyncio.gather` / `tokio::join!` ？

```typescript
// ❌  await
const a = await fetchA();
const b = await fetchB();

// ✅ 
const [a, b] = await Promise.all([fetchA(), fetchB()]);
```

### 

- [ ]  / import （ I/O、、）？
- [ ] per-request ？
- [ ] ？

### 

> （、、） [common-bugs-checklist.md → Resource Management](common-bugs-checklist.md#resource-management)。 **。

- [ ]  dict / list /  `max-size`  TTL？
- [ ] （、、metrics buffer）？
- [ ]  GC？

```python
# ❌ 
_cache: dict[str, Any] = {}

# ✅  LRU
from functools import lru_cache

@lru_cache(maxsize=256)
def get_cached(key: str) -> Any:
    return expensive_computation(key)
```

---

## 

- [Core Web Vitals - web.dev](https://web.dev/articles/vitals)
- [Optimizing Core Web Vitals - Vercel](https://vercel.com/guides/optimizing-core-web-vitals-in-2024)
- [MemLab - Meta Engineering](https://engineering.fb.com/2022/09/12/open-source/memlab/)
- [Big O Cheat Sheet](https://www.bigocheatsheet.com/)
- [N+1 Query Problem - Stack Overflow](https://stackoverflow.com/questions/97197/what-is-the-n1-selects-problem-in-orm-object-relational-mapping)
- [API Performance Optimization](https://algorithmsin60days.com/blog/optimizing-api-performance/)
