# TypeScript/JavaScript Code Review Guide

> TypeScript ，、、、strict 、async/await 。

## 

- [](#)
- [](#)
- [](#)
- [Strict ](#strict-)
- [](#)
- [](#)
- [ESLint ](#eslint-)
- [Review Checklist](#review-checklist)

---

## 

###  any

```typescript
// ❌ Using any defeats type safety
function processData(data: any) {
  return data.value;  // ，
}

// ✅ Use proper types
interface DataPayload {
  value: string;
}
function processData(data: DataPayload) {
  return data.value;
}

// ✅  unknown + 
function processUnknown(data: unknown) {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    return (data as { value: string }).value;
  }
  throw new Error('Invalid data');
}
```

### 

```typescript
// ❌ 
function getLength(value: string | string[]) {
  return (value as string[]).length;  //  string 
}

// ✅ 
function getLength(value: string | string[]): number {
  if (Array.isArray(value)) {
    return value.length;
  }
  return value.length;
}

// ✅  in 
interface Dog { bark(): void }
interface Cat { meow(): void }

function speak(animal: Dog | Cat) {
  if ('bark' in animal) {
    animal.bark();
  } else {
    animal.meow();
  }
}
```

###  as const

```typescript
// ❌ 
const config = {
  endpoint: '/api',
  method: 'GET'  //  string
};

// ✅  as const 
const config = {
  endpoint: '/api',
  method: 'GET'
} as const;  // method  'GET'

// ✅ 
function request(method: 'GET' | 'POST', url: string) { ... }
request(config.method, config.endpoint);  // ！
```

---

## 

### 

```typescript
// ❌ 
function getFirstString(arr: string[]): string | undefined {
  return arr[0];
}
function getFirstNumber(arr: number[]): number | undefined {
  return arr[0];
}

// ✅ 
function getFirst<T>(arr: T[]): T | undefined {
  return arr[0];
}
```

### 

```typescript
// ❌ ，
function getProperty<T>(obj: T, key: string) {
  return obj[key];  // Error: 
}

// ✅  keyof 
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: 'Alice', age: 30 };
getProperty(user, 'name');  //  string
getProperty(user, 'age');   //  number
getProperty(user, 'foo');   // Error: 'foo'  keyof User
```

### 

```typescript
// ✅ 
interface ApiResponse<T = unknown> {
  data: T;
  status: number;
  message: string;
}

// 
const response: ApiResponse = { data: null, status: 200, message: 'OK' };
// 
const userResponse: ApiResponse<User> = { ... };
```

### 

```typescript
// ✅ 
interface User {
  id: number;
  name: string;
  email: string;
}

type PartialUser = Partial<User>;         // 
type RequiredUser = Required<User>;       // 
type ReadonlyUser = Readonly<User>;       // 
type UserKeys = keyof User;               // 'id' | 'name' | 'email'
type NameOnly = Pick<User, 'name'>;       // { name: string }
type WithoutId = Omit<User, 'id'>;        // { name: string; email: string }
type UserRecord = Record<string, User>;   // { [key: string]: User }
```

---

## 

### 

```typescript
// ✅ 
type IsString<T> = T extends string ? true : false;

type A = IsString<string>;  // true
type B = IsString<number>;  // false

// ✅ 
type ElementType<T> = T extends (infer U)[] ? U : never;

type Elem = ElementType<string[]>;  // string

// ✅ （ ReturnType）
type MyReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
```

### 

```typescript
// ✅ 
type Nullable<T> = {
  [K in keyof T]: T[K] | null;
};

interface User {
  name: string;
  age: number;
}

type NullableUser = Nullable<User>;
// { name: string | null; age: number | null }

// ✅ 
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type UserGetters = Getters<User>;
// { getName: () => string; getAge: () => number }
```

### 

```typescript
// ✅ 
type EventName = 'click' | 'focus' | 'blur';
type HandlerName = `on${Capitalize<EventName>}`;
// 'onClick' | 'onFocus' | 'onBlur'

// ✅ API 
type ApiRoute = `/api/${string}`;
const route: ApiRoute = '/api/users';  // OK
const badRoute: ApiRoute = '/users';   // Error
```

### Discriminated Unions

```typescript
// ✅ 
type Result<T, E> =
  | { success: true; data: T }
  | { success: false; error: E };

function handleResult(result: Result<User, Error>) {
  if (result.success) {
    console.log(result.data.name);  // TypeScript  data 
  } else {
    console.log(result.error.message);  // TypeScript  error 
  }
}

// ✅ Redux Action 
type Action =
  | { type: 'INCREMENT'; payload: number }
  | { type: 'DECREMENT'; payload: number }
  | { type: 'RESET' };

function reducer(state: number, action: Action): number {
  switch (action.type) {
    case 'INCREMENT':
      return state + action.payload;  // payload 
    case 'DECREMENT':
      return state - action.payload;
    case 'RESET':
      return 0;  //  payload
  }
}
```

---

## Strict 

###  tsconfig.json

```json
{
  "compilerOptions": {
    // ✅  strict 
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "useUnknownInCatchVariables": true,

    // ✅ 
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true
  }
}
```

### noUncheckedIndexedAccess 

```typescript
// tsconfig: "noUncheckedIndexedAccess": true

const arr = [1, 2, 3];
const first = arr[0];  //  number | undefined

// ❌ 
console.log(first.toFixed(2));  // Error:  undefined

// ✅ 
if (first !== undefined) {
  console.log(first.toFixed(2));
}

// ✅ （）
console.log(arr[0]!.toFixed(2));
```

---

## 

### Promise 

```typescript
// ❌ Not handling async errors
async function fetchUser(id: string) {
  const response = await fetch(`/api/users/${id}`);
  return response.json();  // 
}

// ✅ Handle errors properly
async function fetchUser(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to fetch user: ${error.message}`);
    }
    throw error;
  }
}
```

### Promise.all vs Promise.allSettled

```typescript
// ❌ Promise.all 
async function fetchAllUsers(ids: string[]) {
  const users = await Promise.all(ids.map(fetchUser));
  return users;  // 
}

// ✅ Promise.allSettled 
async function fetchAllUsers(ids: string[]) {
  const results = await Promise.allSettled(ids.map(fetchUser));

  const users: User[] = [];
  const errors: Error[] = [];

  for (const result of results) {
    if (result.status === 'fulfilled') {
      users.push(result.value);
    } else {
      errors.push(result.reason);
    }
  }

  return { users, errors };
}
```

### 

```typescript
// ❌ ：
function useSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    fetch(`/api/search?q=${query}`)
      .then(r => r.json())
      .then(setResults);  // ！
  }, [query]);
}

// ✅  AbortController
function useSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    const controller = new AbortController();

    fetch(`/api/search?q=${query}`, { signal: controller.signal })
      .then(r => r.json())
      .then(setResults)
      .catch(e => {
        if (e.name !== 'AbortError') throw e;
      });

    return () => controller.abort();
  }, [query]);
}
```

---

## 

### Readonly  ReadonlyArray

```typescript
// ❌ 
function processUsers(users: User[]) {
  users.sort((a, b) => a.name.localeCompare(b.name));  // ！
  return users;
}

// ✅  readonly 
function processUsers(users: readonly User[]): User[] {
  return [...users].sort((a, b) => a.name.localeCompare(b.name));
}

// ✅ 
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};
```

### 

```typescript
// ✅  as const  readonly 
function createConfig<T extends readonly string[]>(routes: T) {
  return routes;
}

const routes = createConfig(['home', 'about', 'contact'] as const);
//  readonly ['home', 'about', 'contact']
```

---

## ESLint 

###  @typescript-eslint 

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-requiring-type-checking',
    'plugin:@typescript-eslint/strict'
  ],
  rules: {
    // ✅ 
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/no-unsafe-assignment': 'error',
    '@typescript-eslint/no-unsafe-member-access': 'error',
    '@typescript-eslint/no-unsafe-call': 'error',
    '@typescript-eslint/no-unsafe-return': 'error',

    // ✅ 
    '@typescript-eslint/explicit-function-return-type': 'warn',
    '@typescript-eslint/no-floating-promises': 'error',
    '@typescript-eslint/await-thenable': 'error',
    '@typescript-eslint/no-misused-promises': 'error',

    // ✅ 
    '@typescript-eslint/consistent-type-imports': 'error',
    '@typescript-eslint/prefer-nullish-coalescing': 'error',
    '@typescript-eslint/prefer-optional-chain': 'error'
  }
};
```

###  ESLint 

```typescript
// ❌ no-floating-promises: Promise 
async function save() { ... }
save();  // Error:  Promise

// ✅ 
await save();
// 
save().catch(console.error);
// 
void save();

// ❌ no-misused-promises:  async  Promise
const items = [1, 2, 3];
items.forEach(async (item) => {  // Error!
  await processItem(item);
});

// ✅  for...of
for (const item of items) {
  await processItem(item);
}
//  Promise.all
await Promise.all(items.map(processItem));
```

---

## Review Checklist

### 
- [ ]  `any`（ `unknown` + ）
- [ ] 
- [ ] 
- [ ] 
- [ ] （Partial、Pick、Omit ）

### 
- [ ] （extends）
- [ ] 
- [ ] （KISS ）

### Strict 
- [ ] tsconfig.json  strict: true
- [ ]  noUncheckedIndexedAccess
- [ ]  @ts-ignore（ @ts-expect-error）

### 
- [ ] async 
- [ ] Promise rejection 
- [ ]  floating promises（ Promise）
- [ ]  Promise.all  Promise.allSettled
- [ ]  AbortController 

### 
- [ ] 
- [ ]  spread /
- [ ]  readonly 

### ESLint
- [ ]  @typescript-eslint/recommended
- [ ]  ESLint 
- [ ]  consistent-type-imports
