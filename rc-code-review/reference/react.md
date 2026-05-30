# React Code Review Guide

React ：Hooks 、、、 React 19/RSC 。

## 

- [ Hooks ](#-hooks-)
- [useEffect ](#useeffect-)
- [useMemo / useCallback](#usememo--usecallback)
- [](#)
- [Error Boundaries & Suspense](#error-boundaries--suspense)
- [Server Components (RSC)](#server-components-rsc)
- [React 19 Actions & Forms](#react-19-actions--forms)
- [Suspense & Streaming SSR](#suspense--streaming-ssr)
- [TanStack Query v5](#tanstack-query-v5)
- [Review Checklists](#review-checklists)

---

##  Hooks 

```tsx
// ❌  Hooks —  Hooks 
function BadComponent({ isLoggedIn }) {
  if (isLoggedIn) {
    const [user, setUser] = useState(null);  // Error!
  }
  return <div>...</div>;
}

// ✅ Hooks 
function GoodComponent({ isLoggedIn }) {
  const [user, setUser] = useState(null);
  if (!isLoggedIn) return <LoginPrompt />;
  return <div>{user?.name}</div>;
}
```

---

## useEffect 

```tsx
// ❌ 
function BadEffect({ userId }) {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, []);  //  userId ！
}

// ✅ 
function GoodEffect({ userId }) {
  const [user, setUser] = useState(null);
  useEffect(() => {
    let cancelled = false;
    fetchUser(userId).then(data => {
      if (!cancelled) setUser(data);
    });
    return () => { cancelled = true; };  // 
  }, [userId]);
}

// ❌ useEffect （）
function BadDerived({ items }) {
  const [filteredItems, setFilteredItems] = useState([]);
  useEffect(() => {
    setFilteredItems(items.filter(i => i.active));
  }, [items]);  //  effect + 
  return <List items={filteredItems} />;
}

// ✅ ， useMemo
function GoodDerived({ items }) {
  const filteredItems = useMemo(
    () => items.filter(i => i.active),
    [items]
  );
  return <List items={filteredItems} />;
}

// ❌ useEffect 
function BadEventEffect() {
  const [query, setQuery] = useState('');
  useEffect(() => {
    if (query) {
      analytics.track('search', { query });  // 
    }
  }, [query]);
}

// ✅ 
function GoodEvent() {
  const [query, setQuery] = useState('');
  const handleSearch = (q: string) => {
    setQuery(q);
    analytics.track('search', { query: q });
  };
}
```

---

## useMemo / useCallback

```tsx
// ❌  —  useMemo
function OverOptimized() {
  const config = useMemo(() => ({ timeout: 5000 }), []);  // 
  const handleClick = useCallback(() => {
    console.log('clicked');
  }, []);  //  memo ，
}

// ✅ 
function ProperlyOptimized() {
  const config = { timeout: 5000 };  // 
  const handleClick = () => console.log('clicked');
}

// ❌ useCallback 
function BadCallback({ data }) {
  // data ，useCallback 
  const process = useCallback(() => {
    return data.map(transform);
  }, [data]);
}

// ✅ useMemo + useCallback  React.memo 
const MemoizedChild = React.memo(function Child({ onClick, items }) {
  return <div onClick={onClick}>{items.length}</div>;
});

function Parent({ rawItems }) {
  const items = useMemo(() => processItems(rawItems), [rawItems]);
  const handleClick = useCallback(() => {
    console.log(items.length);
  }, [items]);
  return <MemoizedChild onClick={handleClick} items={items} />;
}
```

---

## 

```tsx
// ❌  — 
function BadParent() {
  function ChildComponent() {  // ！
    return <div>child</div>;
  }
  return <ChildComponent />;
}

// ✅ 
function ChildComponent() {
  return <div>child</div>;
}
function GoodParent() {
  return <ChildComponent />;
}

// ❌ Props 
function BadProps() {
  return (
    <MemoizedComponent
      style={{ color: 'red' }}  // 
      onClick={() => {}}         // 
    />
  );
}

// ✅ 
const style = { color: 'red' };
function GoodProps() {
  const handleClick = useCallback(() => {}, []);
  return <MemoizedComponent style={style} onClick={handleClick} />;
}
```

---

## Error Boundaries & Suspense

```tsx
// ❌ 
function BadApp() {
  return (
    <Suspense fallback={<Loading />}>
      <DataComponent />  {/*  */}
    </Suspense>
  );
}

// ✅ Error Boundary  Suspense
function GoodApp() {
  return (
    <ErrorBoundary fallback={<ErrorUI />}>
      <Suspense fallback={<Loading />}>
        <DataComponent />
      </Suspense>
    </ErrorBoundary>
  );
}
```

---

## Server Components (RSC)

```tsx
// ❌  Server Component 
// app/page.tsx (Server Component by default)
function BadServerComponent() {
  const [count, setCount] = useState(0);  // Error! No hooks in RSC
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}

// ✅  Client Component
// app/counter.tsx
'use client';
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}

// app/page.tsx (Server Component)
async function GoodServerComponent() {
  const data = await fetchData();  //  await
  return (
    <div>
      <h1>{data.title}</h1>
      <Counter />  {/*  */}
    </div>
  );
}

// ❌ 'use client'  — 
// layout.tsx
'use client';  // 
export default function Layout({ children }) { ... }

// ✅  'use client'
// 
```

---

## React 19 Actions & Forms

React 19  Actions  Hooks，。

### useActionState

```tsx
// ❌ ：
function OldForm() {
  const [isPending, setIsPending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState(null);

  const handleSubmit = async (formData: FormData) => {
    setIsPending(true);
    setError(null);
    try {
      const result = await submitForm(formData);
      setData(result);
    } catch (e) {
      setError(e.message);
    } finally {
      setIsPending(false);
    }
  };
}

// ✅ React 19: useActionState 
import { useActionState } from 'react';

function NewForm() {
  const [state, formAction, isPending] = useActionState(
    async (prevState, formData: FormData) => {
      try {
        const result = await submitForm(formData);
        return { success: true, data: result };
      } catch (e) {
        return { success: false, error: e.message };
      }
    },
    { success: false, data: null, error: null }
  );

  return (
    <form action={formAction}>
      <input name="email" />
      <button disabled={isPending}>
        {isPending ? 'Submitting...' : 'Submit'}
      </button>
      {state.error && <p className="error">{state.error}</p>}
    </form>
  );
}
```

### useFormStatus

```tsx
// ❌ Props 
function BadSubmitButton({ isSubmitting }) {
  return <button disabled={isSubmitting}>Submit</button>;
}

// ✅ useFormStatus  <form> （ props）
import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending, data, method, action } = useFormStatus();
  // ： <form> 
  return (
    <button disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  );
}

// ❌ useFormStatus  form ——
function BadForm() {
  const { pending } = useFormStatus();  // ！
  return (
    <form action={action}>
      <button disabled={pending}>Submit</button>
    </form>
  );
}

// ✅ useFormStatus  form 
function GoodForm() {
  return (
    <form action={action}>
      <SubmitButton />  {/* useFormStatus  */}
    </form>
  );
}
```

### useOptimistic

```tsx
// ❌  UI
function SlowLike({ postId, likes }) {
  const [likeCount, setLikeCount] = useState(likes);
  const [isPending, setIsPending] = useState(false);

  const handleLike = async () => {
    setIsPending(true);
    const newCount = await likePost(postId);  // ...
    setLikeCount(newCount);
    setIsPending(false);
  };
}

// ✅ useOptimistic ，
import { useOptimistic } from 'react';

function FastLike({ postId, likes }) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    likes,
    (currentLikes, increment: number) => currentLikes + increment
  );

  const handleLike = async () => {
    addOptimisticLike(1);  //  UI
    try {
      await likePost(postId);  // 
    } catch {
      // React  likes 
    }
  };

  return <button onClick={handleLike}>{optimisticLikes} likes</button>;
}
```

### Server Actions (Next.js 15+)

```tsx
// ❌  API
'use client';
function ClientForm() {
  const handleSubmit = async (formData: FormData) => {
    const res = await fetch('/api/submit', {
      method: 'POST',
      body: formData,
    });
    // ...
  };
}

// ✅ Server Action + useActionState
// actions.ts
'use server';
export async function createPost(prevState: any, formData: FormData) {
  const title = formData.get('title');
  await db.posts.create({ title });
  revalidatePath('/posts');
  return { success: true };
}

// form.tsx
'use client';
import { createPost } from './actions';

function PostForm() {
  const [state, formAction, isPending] = useActionState(createPost, null);
  return (
    <form action={formAction}>
      <input name="title" />
      <SubmitButton />
    </form>
  );
}
```

---

## Suspense & Streaming SSR

Suspense  Streaming  React 18+ ， 2025  Next.js 15 。

###  Suspense

```tsx
// ❌ 
function OldComponent() {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchData().then(setData).finally(() => setIsLoading(false));
  }, []);

  if (isLoading) return <Spinner />;
  return <DataView data={data} />;
}

// ✅ Suspense 
function NewComponent() {
  return (
    <Suspense fallback={<Spinner />}>
      <DataView />  {/*  use()  Suspense  */}
    </Suspense>
  );
}
```

###  Suspense 

```tsx
// ❌ ——
function BadLayout() {
  return (
    <Suspense fallback={<FullPageSpinner />}>
      <Header />
      <MainContent />  {/*  */}
      <Sidebar />      {/*  */}
    </Suspense>
  );
}

// ✅ ——
function GoodLayout() {
  return (
    <>
      <Header />  {/*  */}
      <div className="flex">
        <Suspense fallback={<ContentSkeleton />}>
          <MainContent />  {/*  */}
        </Suspense>
        <Suspense fallback={<SidebarSkeleton />}>
          <Sidebar />      {/*  */}
        </Suspense>
      </div>
    </>
  );
}
```

### Next.js 15 Streaming

```tsx
// app/page.tsx -  Streaming
export default async function Page() {
  //  await 
  const data = await fetchSlowData();
  return <div>{data}</div>;
}

// app/loading.tsx -  Suspense 
export default function Loading() {
  return <Skeleton />;
}
```

### use() Hook (React 19)

```tsx
// ✅  Promise
import { use } from 'react';

function Comments({ commentsPromise }) {
  const comments = use(commentsPromise);  //  Suspense
  return (
    <ul>
      {comments.map(c => <li key={c.id}>{c.text}</li>)}
    </ul>
  );
}

//  Promise，
function Post({ postId }) {
  const commentsPromise = fetchComments(postId);  //  await
  return (
    <article>
      <PostContent id={postId} />
      <Suspense fallback={<CommentsSkeleton />}>
        <Comments commentsPromise={commentsPromise} />
      </Suspense>
    </article>
  );
}
```

---

## TanStack Query v5

TanStack Query  React ，v5 。

### 

```tsx
// ❌ 
const queryClient = new QueryClient();  // 

// ✅ 
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,  // 5 
      gcTime: 1000 * 60 * 30,    // 30 （v5 ）
      retry: 3,
      refetchOnWindowFocus: false,  // 
    },
  },
});
```

### queryOptions (v5 )

```tsx
// ❌  queryKey  queryFn
function Component1() {
  const { data } = useQuery({
    queryKey: ['users', userId],
    queryFn: () => fetchUser(userId),
  });
}

function prefetchUser(queryClient, userId) {
  queryClient.prefetchQuery({
    queryKey: ['users', userId],  // ！
    queryFn: () => fetchUser(userId),  // ！
  });
}

// ✅ queryOptions ，
import { queryOptions } from '@tanstack/react-query';

const userQueryOptions = (userId: string) =>
  queryOptions({
    queryKey: ['users', userId],
    queryFn: () => fetchUser(userId),
  });

function Component1({ userId }) {
  const { data } = useQuery(userQueryOptions(userId));
}

function prefetchUser(queryClient, userId) {
  queryClient.prefetchQuery(userQueryOptions(userId));
}

// getQueryData 
const user = queryClient.getQueryData(userQueryOptions(userId).queryKey);
```

### 

```tsx
// ❌ staleTime  0 
useQuery({
  queryKey: ['data'],
  queryFn: fetchData,
  // staleTime  0， refetch
});

// ✅  staleTime
useQuery({
  queryKey: ['data'],
  queryFn: fetchData,
  staleTime: 1000 * 60,  // 1 
});

// ❌  queryFn 
function BadQuery({ filters }) {
  useQuery({
    queryKey: ['items'],  // queryKey  filters！
    queryFn: () => fetchItems(filters),  // filters 
  });
}

// ✅ queryKey 
function GoodQuery({ filters }) {
  useQuery({
    queryKey: ['items', filters],  // filters  queryKey 
    queryFn: () => fetchItems(filters),
  });
}
```

### useSuspenseQuery

> ****：useSuspenseQuery  useQuery ，。

#### useSuspenseQuery 

|  | useQuery | useSuspenseQuery |
|------|----------|------------------|
| `enabled`  | ✅  | ❌  |
| `placeholderData` | ✅  | ❌  |
| `data`  | `T \| undefined` | `T`（）|
|  | `error`  |  Error Boundary |
|  | `isLoading`  |  Suspense |

####  enabled 

```tsx
// ❌  useQuery + enabled 
function BadSuspenseQuery({ userId }) {
  const { data } = useSuspenseQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    enabled: !!userId,  // useSuspenseQuery  enabled！
  });
}

// ✅ 
function GoodSuspenseQuery({ userId }) {
  // useSuspenseQuery  data  T  T | undefined
  const { data } = useSuspenseQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });
  return <UserProfile user={data} />;
}

function Parent({ userId }) {
  if (!userId) return <NoUserSelected />;
  return (
    <Suspense fallback={<UserSkeleton />}>
      <GoodSuspenseQuery userId={userId} />
    </Suspense>
  );
}
```

#### 

```tsx
// ❌ useSuspenseQuery  error 
function BadErrorHandling() {
  const { data, error } = useSuspenseQuery({...});
  if (error) return <Error />;  // error  null！
}

// ✅  Error Boundary 
function GoodErrorHandling() {
  return (
    <ErrorBoundary fallback={<ErrorMessage />}>
      <Suspense fallback={<Loading />}>
        <DataComponent />
      </Suspense>
    </ErrorBoundary>
  );
}

function DataComponent() {
  //  Error Boundary
  const { data } = useSuspenseQuery({
    queryKey: ['data'],
    queryFn: fetchData,
  });
  return <Display data={data} />;
}
```

####  useSuspenseQuery

```tsx
// ✅ ：
// 1. （）
// 2. 
// 3.  React 19  Suspense 
// 4.  +  hydration

// ❌ ：
// 1. （）
// 2.  placeholderData 
// 3.  loading/error 
// 4. 

// ✅  useSuspenseQueries
function MultipleQueries({ userId }) {
  const [userQuery, postsQuery] = useSuspenseQueries({
    queries: [
      { queryKey: ['user', userId], queryFn: () => fetchUser(userId) },
      { queryKey: ['posts', userId], queryFn: () => fetchPosts(userId) },
    ],
  });
  // ，
  return <Profile user={userQuery.data} posts={postsQuery.data} />;
}
```

###  (v5 )

```tsx
// ❌ （）
const mutation = useMutation({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    await queryClient.cancelQueries({ queryKey: ['todos'] });
    const previousTodos = queryClient.getQueryData(['todos']);
    queryClient.setQueryData(['todos'], (old) => [...old, newTodo]);
    return { previousTodos };
  },
  onError: (err, newTodo, context) => {
    queryClient.setQueryData(['todos'], context.previousTodos);
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});

// ✅ v5 ： variables  UI
function TodoList() {
  const { data: todos } = useQuery(todosQueryOptions);
  const { mutate, variables, isPending } = useMutation({
    mutationFn: addTodo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });

  return (
    <ul>
      {todos?.map(todo => <TodoItem key={todo.id} todo={todo} />)}
      {/*  todo */}
      {isPending && <TodoItem todo={variables} isOptimistic />}
    </ul>
  );
}
```

### v5 

```tsx
// v4: isLoading 
// v5: isPending ，isLoading = isPending && isFetching

const { data, isPending, isFetching, isLoading } = useQuery({...});

// isPending: （）
// isFetching: （）
// isLoading: isPending && isFetching（）

// ❌ v4 
if (isLoading) return <Spinner />;  // v5 

// ✅ 
if (isPending) return <Spinner />;  // 
// 
if (isLoading) return <Spinner />;  // 
```

---

## Review Checklists

### Hooks 

- [ ] Hooks / Hook 
- [ ] / Hooks
- [ ] useEffect 
- [ ] useEffect （//）
- [ ]  useEffect 

### （）

- [ ] useMemo/useCallback 
- [ ] React.memo  props 
- [ ] 
- [ ]  JSX /（ memo ）
- [ ] （react-window/react-virtual）

### 

- [ ] ， 200 
- [ ] （Custom Hooks）
- [ ] Props ， TypeScript
- [ ]  Props Drilling（ Context ）

### 

- [ ] （）
- [ ]  useReducer
- [ ]  Context 
- [ ] （ > ）

### 

- [ ]  Error Boundary
- [ ] Suspense  Error Boundary 
- [ ] 

### Server Components (RSC)

- [ ] 'use client' 
- [ ] Server Component  Hooks/
- [ ] 
- [ ]  Server Component 

### React 19 Forms

- [ ]  useActionState  useState
- [ ] useFormStatus  form 
- [ ] useOptimistic （）
- [ ] Server Action  'use server'

### Suspense & Streaming

- [ ]  Suspense 
- [ ]  Suspense  Error Boundary
- [ ]  fallback（ > Spinner）
- [ ]  layout  await 

### TanStack Query

- [ ] queryKey 
- [ ]  staleTime（ 0）
- [ ] useSuspenseQuery  enabled
- [ ] Mutation  invalidate 
- [ ]  isPending vs isLoading 

### 

- [ ]  @testing-library/react
- [ ]  screen 
- [ ]  userEvent  fireEvent
- [ ]  *ByRole 
- [ ] 
