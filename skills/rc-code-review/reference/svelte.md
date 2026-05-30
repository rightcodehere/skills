# Svelte / SvelteKit Code Review Guide

Svelte 5 / SvelteKit ：Runes 、Server/Client 、Form Actions、Store 、。

## 

- [Runes: $state / $derived / $effect](#runes-state--derived--effect)
- [Load （Server vs Client）](#load-server-vs-client)
- [Form Actions](#form-actions)
- [Store （→ $state）](#store-)
- [SSR vs CSR ](#ssr-vs-csr-)
- [（$: → Runes）](#)
- [](#)
- [](#)
- [Review Checklist](#review-checklist)

---

## Runes: $state / $derived / $effect

### $state 

```svelte
<!-- ❌ $state  -->
<script lang="ts">
  let config = $state({ timeout: 5000 });  // 
  const API_URL = $state('/api');           //  $state
</script>

<!-- ✅  -->
<script lang="ts">
  const config = { timeout: 5000 };
  const API_URL = '/api';

  // $state 
  let count = $state(0);
  let user = $state<User | null>(null);
</script>
```

### $state.raw 

```svelte
<!-- ❌  -->
<script lang="ts">
  // largeData ，
  let data = $state(hugeApiResponse);
</script>

<!-- ✅ $state.raw  -->
<script lang="ts">
  let data = $state.raw(hugeApiResponse);

  // 
  async function refresh() {
    data = await fetchLatestData();  // ✅ triggers reactivity
  }

  // ❌ 
  // data.items[0].name = 'new';  // will NOT re-render
</script>
```

### $state.snapshot 

```svelte
<!-- ❌  $state  -->
<script lang="ts">
  let state = $state({ x: 0, y: 0 });

  onMount(() => {
    //  Proxy 
    chartLibrary.update(state);  // state is a Proxy!
  });
</script>

<!-- ✅ $state.snapshot  -->
<script lang="ts">
  import { unstate } from 'svelte';

  let state = $state({ x: 0, y: 0 });

  onMount(() => {
    // $state.snapshot produces a plain object (Svelte 5)
    chartLibrary.update($state.snapshot(state));
    // or use unstate() for the same purpose
    chartLibrary.update(unstate(state));
  });
</script>
```

###  $state 

```svelte
<!-- ❌  $state  -->
<script lang="ts">
  let state = $state({ count: 0, name: 'Svelte' });
  let { count, name } = state;  // count and name are plain values!
</script>
<p>{count}</p>  <!-- ❌ will NOT update when state.count changes -->

<!-- ✅  $state  -->
<script lang="ts">
  let state = $state({ count: 0, name: 'Svelte' });
</script>
<p>{state.count}</p>  <!-- ✅ stays reactive -->

<!-- ✅  $state -->
<script lang="ts">
  let count = $state(0);
  let name = $state('Svelte');
</script>
```

---

### $derived 

```svelte
<!-- ❌ #1 ： $effect  -->
<script lang="ts">
  let firstName = $state('John');
  let lastName = $state('Doe');
  let fullName = $state('');

  //  $effect ！
  $effect(() => {
    fullName = `${firstName} ${lastName}`;  // unnecessary effect
  });
</script>

<!-- ✅  $derived  -->
<script lang="ts">
  let firstName = $state('John');
  let lastName = $state('Doe');
  let fullName = $derived(`${firstName} ${lastName}`);
</script>
```

### $derived 

```svelte
<!-- ❌ $derived  -->
<script lang="ts">
  let items = $state<Item[]>([]);
  let count = $derived(() => {
    console.log('recalculating');  // side effect!
    analytics.track('count', items.length);  // side effect!
    return items.length;
  });
</script>

<!-- ✅ $derived  -->
<script lang="ts">
  let items = $state<Item[]>([]);
  let count = $derived(items.length);

  // side effects go in $effect
  $effect(() => {
    analytics.track('count', count);
  });
</script>
```

---

### $effect 

#### $effect vs $derived

```svelte
<!-- ❌ $effect （） -->
<script lang="ts">
  let searchQuery = $state('');
  let results = $state([]);

  $effect(() => {
    results = searchQuery ? items.filter(i => i.name.includes(searchQuery)) : items;
  });
</script>

<!-- ✅  $derived -->
<script lang="ts">
  let searchQuery = $state('');
  let results = $derived(
    searchQuery ? items.filter(i => i.name.includes(searchQuery)) : items
  );
</script>
```

#### 

```svelte
<!-- ❌ $effect  →  -->
<script lang="ts">
  let count = $state(0);

  $effect(() => {
    console.log(count);
    count++;  // modifying dependency inside effect → infinite loop!
  });
</script>

<!-- ✅  $effect  -->
<script lang="ts">
  let count = $state(0);
  let log = $state<string[]>([]);

  $effect(() => {
    // read count, write to a different state
    log = [...log, `count is ${count}`];
  });
</script>
```

#### 

```svelte
<!-- ❌  →  -->
<script lang="ts">
  let roomId = $state('');

  $effect(() => {
    const ws = new WebSocket(`ws://example.com/${roomId}`);
    ws.onmessage = (e) => {
      messages = [...messages, JSON.parse(e.data)];
    };
    // no cleanup! WebSocket leaks when roomId changes
  });
</script>

<!-- ✅  -->
<script lang="ts">
  let roomId = $state('');

  $effect(() => {
    const ws = new WebSocket(`ws://example.com/${roomId}`);
    ws.onmessage = (e) => {
      messages = [...messages, JSON.parse(e.data)];
    };
    return () => ws.close();  // cleanup on re-run
  });
</script>

<!-- ✅  -->
<script lang="ts">
  $effect(() => {
    const id = setInterval(() => {
      console.log('tick');
    }, 1000);
    return () => clearInterval(id);
  });
</script>
```

#### async $effect 

```svelte
<!-- ❌ await  -->
<script lang="ts">
  let userId = $state('1');
  let preference = $state('dark');

  $effect(async () => {
    const user = await fetchUser(userId);   // userId IS tracked
    const theme = preference;               // NOT tracked (read after await)!
    applyTheme(user, theme);
  });
</script>

<!-- ✅  await  -->
<script lang="ts">
  let userId = $state('1');
  let preference = $state('dark');

  $effect(async () => {
    const currentPref = preference;  // read before await
    const user = await fetchUser(userId);
    applyTheme(user, currentPref);
  });
</script>
```

#### untrack 

```svelte
<!-- ❌  -->
<script lang="ts">
  let data = $state<Data | null>(null);
  let debugMode = $state(false);

  $effect(() => {
    if (debugMode) {  // debugMode becomes a dependency!
      console.log('data changed', data);
    }
  });
</script>

<!-- ✅ untrack  -->
<script lang="ts">
  import { untrack } from 'svelte';

  let data = $state<Data | null>(null);
  let debugMode = $state(false);

  $effect(() => {
    if (untrack(() => debugMode)) {  // debugMode is NOT tracked
      console.log('data changed', data);
    }
  });
</script>
```

---

## Load （Server vs Client）

### +page.server.js vs +page.js

```typescript
// ❌  +page.js  secrets
// src/routes/admin/+page.js
export async function load({ fetch }) {
  // universal load runs on both server and client
  const data = await db.query('SELECT * FROM users');  // db not available in browser!
  return { users: data };
}

// ✅  +page.server.js
// src/routes/admin/+page.server.js
import { db } from '$lib/server/db';

export async function load() {
  const users = await db.query('SELECT * FROM users');
  return { users };
}
```

```typescript
// ✅ +page.js （ fetch ）
// src/routes/dashboard/+page.js
export async function load({ fetch, parent }) {
  const [analytics, notifications] = await Promise.all([
    fetch('/api/analytics').then(r => r.json()),
    fetch('/api/notifications').then(r => r.json())
  ]);
  return { analytics, notifications };
}
```

### await parent() 

```typescript
// ❌  await parent → 
// src/routes/blog/[slug]/+page.js
export async function load({ parent, fetch }) {
  const parentData = await parent();  // wait for parent
  const post = await fetch(`/api/posts/${parentData.blogId}`);
  return { post };
}

// ✅ ， parent await
// src/routes/blog/[slug]/+page.js
export async function load({ parent, fetch }) {
  // only await parent if you truly need its data
  const post = await fetch('/api/posts/slug');
  return { post };
}

// ✅  parent ，，
// src/routes/blog/[slug]/+page.js
export async function load({ parent, fetch }) {
  const { blogId } = await parent();  // required: need blogId for post URL
  const post = await fetch(`/api/posts/${blogId}`);
  return { post };
}
```

### 

```typescript
// ❌  server load 
// src/routes/api/+page.server.js
export async function load() {
  return {
    stream: fs.createReadStream('data.csv'),  // not serializable!
    callback: () => console.log('hi'),        // functions not serializable!
    date: new Date(),                         // becomes string via devalue
  };
}

// ✅ 
// src/routes/api/+page.server.js
export async function load() {
  return {
    data: await readFile('data.csv', 'utf-8'),
    timestamp: Date.now(),
  };
}
```

---

## Form Actions

###  POST 

```svelte
<!-- ❌  GET/load  -->
<script lang="ts">
  import { goto } from '$app/navigation';

  async function deleteUser(id: string) {
    await fetch(`/api/users/${id}`, { method: 'DELETE' });
    goto('/users');  // side effect via client navigation
  }
</script>
<button onclick={() => deleteUser(user.id)}>Delete</button>

<!-- ✅  form actions -->
```

```typescript
// src/routes/users/+page.server.js
import { fail, redirect } from '@sveltejs/kit';

export const actions = {
  delete: async ({ request, locals }) => {
    const formData = await request.formData();
    const id = formData.get('id');

    if (!id) return fail(400, { message: 'Missing id' });

    await locals.db.users.delete(id);
    throw redirect(303, '/users');
  }
};
```

```svelte
<!-- form with progressive enhancement -->
<script lang="ts">
  import { enhance } from '$app/forms';
</script>

<form method="POST" action="?/delete" use:enhance>
  <input type="hidden" name="id" value={user.id} />
  <button type="submit">Delete</button>
</form>
```

### fail() 

```typescript
// ❌ fail() 
// src/routes/login/+page.server.js
export const actions = {
  default: async ({ request, locals }) => {
    const formData = await request.formData();
    const user = await locals.db.users.findByEmail(formData.get('email'));

    return fail(401, {
      password: formData.get('password'),  // ❌ exposes password in page data!
      hint: user.passwordHint,             // ❌ leaks internal data!
    });
  }
};

// ✅ 
export const actions = {
  default: async ({ request }) => {
    const formData = await request.formData();
    const email = formData.get('email');

    return fail(401, {
      email,                    // ✅ safe to echo back
      incorrect: true,          // ✅ generic error flag
    });
  }
};
```

### use:enhance 

```svelte
<!-- ❌  use:enhance →  JS  -->
<form method="POST" action="?/create">
  <input name="title" />
  <button type="submit">Create</button>
</form>

<!-- ✅ use:enhance  SPA  + progressive enhancement -->
<script lang="ts">
  import { enhance } from '$app/forms';
</script>

<form method="POST" action="?/create" use:enhance={() => {
  return ({ update }) => {
    update({ reset: false });  // customize behavior
  };
}}>
  <input name="title" />
  <button type="submit">Create</button>
</form>

<!-- ✅  -->
<form
  method="POST"
  action="?/create"
  use:enhance={() => {
    submitting = true;
    return ({ update }) => {
      update();
      submitting = false;
    };
  }}
>
  <button type="submit" disabled={submitting}>
    {submitting ? 'Creating...' : 'Create'}
  </button>
</form>
```

---

## Store （→ $state）

### writable/readable → $state

```typescript
// ❌ Legacy store pattern (Svelte 4)
// src/lib/stores/user.js
import { writable, derived } from 'svelte/store';

export const user = writable(null);
export const isLoggedIn = derived(user, $user => !!$user);

// usage with $ prefix
// $user = { name: 'John' };

// ✅ Svelte 5: shared state in .svelte.js files
// src/lib/stores/user.svelte.js
let currentUser = $state<User | null>(null);

export function getUser() {
  return currentUser;
}

export function setUser(user: User | null) {
  currentUser = user;
}

export function isLoggedIn() {
  return currentUser !== null;
}
```

### $  store 

```svelte
<!-- ❌ $  store  -->
<script lang="ts">
  import { count } from '$lib/stores/count';
  // $count is legacy syntax in Svelte 5
</script>
<p>{$count}</p>

<!-- ✅ Svelte 5 runes  -->
<script lang="ts">
  import { getCount } from '$lib/stores/count.svelte';

  let count = $derived(getCount());
</script>
<p>{count}</p>

<!-- ✅  export  $state  getter -->
<script lang="ts">
  // count.svelte.js exports a reactive reference
  import { counter } from '$lib/stores/count.svelte';
</script>
<p>{counter.value}</p>
```

### .svelte.js / .svelte.ts 

```typescript
// ❌  .js  runes → 
// src/lib/utils.js
let state = $state(0);  // runes only work in .svelte.js files!

// ✅  .svelte.js 
// src/lib/utils.svelte.js
let state = $state(0);

export function getState() {
  return state;
}

export function setState(val: number) {
  state = val;
}
```

---

## SSR vs CSR 

### ssr=false SPA 

```typescript
// ❌  layout  SSR →  CSR
// src/routes/+layout.js
export const ssr = false;  // entire app becomes SPA

// ✅  SSR
// src/routes/admin/dashboard/+page.js
export const ssr = false;  // only this page skips SSR

// ✅ ：
// src/routes/editor/+page.js
export const ssr = false;  // editor needs browser APIs, skip SSR
```

###  SSR 

```svelte
<!-- ❌  API -->
<script lang="ts">
  const height = window.innerHeight;        // ReferenceError during SSR!
  const prefersDark = matchMedia('(prefers-color-scheme: dark)');  // crash!
</script>

<!-- ✅  onMount  browser guard  -->
<script lang="ts">
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';

  let height = $state(0);

  onMount(() => {
    height = window.innerHeight;
  });

  // or conditional check
  const prefersDark = browser
    ? matchMedia('(prefers-color-scheme: dark)').matches
    : false;
</script>
```

### prerender  actions 

```typescript
// ❌ prerender  actions → 
// src/routes/contact/+page.server.js
export const prerender = true;

export const actions = {
  // Error: prerendered pages cannot have server-side form actions
  default: async ({ request }) => { /* ... */ }
};

// ✅ prerender  server actions
// src/routes/about/+page.server.js
export const prerender = true;
// no actions — static page

// ✅  actions  prerender
// src/routes/contact/+page.server.js
export const actions = {
  default: async ({ request }) => {
    // handle form submission
  }
};
```

---

## 

### $: → $derived / $effect

```svelte
<!-- ❌ Svelte 4  -->
<script lang="ts">
  let count = 0;
  let doubled = 0;

  $: doubled = count * 2;              // reactive assignment
  $: if (count > 10) console.log('big');
</script>

<!-- ✅ Svelte 5 runes -->
<script lang="ts">
  let count = $state(0);
  let doubled = $derived(count * 2);   // derived value

  $effect(() => {
    if (count > 10) console.log('big');
  });
</script>
```

### export let → $props()

```svelte
<!-- ❌ Svelte 4 props -->
<script lang="ts">
  export let title: string;
  export let count = 0;
</script>

<!-- ✅ Svelte 5 $props() -->
<script lang="ts">
  let { title, count = 0 }: { title: string; count?: number } = $props();
</script>
```

### on:click → onclick

```svelte
<!-- ❌ Svelte 4  -->
<button on:click={handleClick}>Click</button>
<button on:click={() => count++}>Increment</button>

<!-- ✅ Svelte 5 HTML  -->
<button onclick={handleClick}>Click</button>
<button onclick={() => count++}>Increment</button>
```

### createEventDispatcher →  props

```svelte
<!-- ❌ Svelte 4  dispatch -->
<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  function handleDelete() {
    dispatch('delete', { id: 42 });
  }
</script>

<!-- ✅ Svelte 5  props -->
<script lang="ts">
  let { ondelete }: { ondelete?: (e: { id: number }) => void } = $props();

  function handleDelete() {
    ondelete?.({ id: 42 });
  }
</script>

<!-- parent usage -->
<Child ondelete={(e) => removeItem(e.id)} />
```

### slot → @render children()

```svelte
<!-- ❌ Svelte 4 slot -->
<!-- Card.svelte -->
<div class="card">
  <slot />
</div>

<!-- ✅ Svelte 5 snippets -->
<!-- Card.svelte -->
<script lang="ts">
  let { children } = $props();
</script>
<div class="card">
  {@render children()}
</div>

<!-- with named slots → named snippets -->
<!-- Layout.svelte -->
<script lang="ts">
  let { header, children, footer } = $props();
</script>
<div>
  <header>{@render header?.()}</header>
  <main>{@render children()}</main>
  <footer>{@render footer?.()}</footer>
</div>

<!-- parent usage -->
<Layout>
  {#snippet header()}<h1>Title</h1>{/snippet}
  <p>Body content</p>
  {#snippet footer()}<p>Footer</p>{/snippet}
</Layout>
```

### beforeUpdate / afterUpdate → $effect.pre

```svelte
<!-- ❌ Svelte 4 lifecycle hooks -->
<script lang="ts">
  import { beforeUpdate, afterUpdate } from 'svelte';

  let count = 0;

  beforeUpdate(() => {
    console.log('about to update', count);
  });

  afterUpdate(() => {
    console.log('updated', count);
    document.title = `Count: ${count}`;
  });
</script>

<!-- ✅ Svelte 5 $effect and $effect.pre -->
<script lang="ts">
  let count = $state(0);

  // $effect.pre runs before DOM updates (like beforeUpdate)
  $effect.pre(() => {
    console.log('about to update', count);
  });

  // $effect runs after DOM updates (like afterUpdate)
  $effect(() => {
    console.log('updated', count);
    document.title = `Count: ${count}`;
  });
</script>
```

---

## 

### $state.raw 

```svelte
<!-- ❌  -->
<script lang="ts">
  let searchResults = $state(largeResultArray);  // deep proxy on every item
</script>

<!-- ✅ $state.raw  -->
<script lang="ts">
  let searchResults = $state.raw<SearchResult[]>([]);

  async function search(query: string) {
    searchResults = await fetchResults(query);  // whole-array replacement
  }
</script>
```

### Keyed {#each}

```svelte
<!-- ❌  key  each →  DOM diff -->
{#each items as item}
  <div>{item.name}</div>
{/each}

<!-- ✅  key  each -->
{#each items as item (item.id)}
  <div>{item.name}</div>
{/each}

<!-- ✅  key -->
{#each items as item (item.category, item.id)}
  <div>{item.name}</div>
{/each}
```

### Streaming  load  Promise

```typescript
// ❌  → 
// src/routes/+page.server.js
export async function load({ params }) {
  const posts = await getPosts();       // slow
  const comments = await getComments(); // slow
  const tags = await getTags();         // slow
  return { posts, comments, tags };
}

// ✅ 
export async function load({ params }) {
  return {
    posts: getPosts(),       // return promises directly for streaming
    comments: getComments(),
    tags: getTags(),
  };
}
```

```svelte
<!-- streaming in template with {#await} -->
{#await data.posts}
  <p>Loading posts...</p>
{:then posts}
  <ul>
    {#each posts as post (post.id)}
      <li>{post.title}</li>
    {/each}
  </ul>
{:catch error}
  <p>Failed to load posts: {error.message}</p>
{/await}
```

---

## 

### 

```typescript
// ❌  universal load  secrets
// src/routes/admin/+page.js (universal — runs on client too!)
export async function load() {
  return {
    apiKey: process.env.SECRET_API_KEY,    // exposed to client bundle!
    dbUrl: import.meta.env.DATABASE_URL,    // leaks to browser!
  };
}

// ✅  server load 
// src/routes/admin/+page.server.js (server-only)
export async function load({ locals }) {
  // secrets stay on server
  const data = await fetch(process.env.SECRET_API_KEY + '/admin');
  return { data };  // only derived data is sent to client
}

// ✅  PUBLIC_ 
// .env
// PUBLIC_API_URL=https://api.example.com
// SECRET_API_KEY=xxx  (no PUBLIC_ prefix = server-only)
```

### $lib/server/ 

```typescript
// ❌ 
// src/lib/db.js
import { SECRET_DB_URL } from '$env/static/private';
// any client component importing this gets the secret!

// ✅  $lib/server/  → 
// src/lib/server/db.js
import { SECRET_DB_URL } from '$env/static/private';

export async function query(sql: string) {
  // safe: client cannot import from $lib/server/
}

// usage in server files only
// src/routes/api/users/+server.js
import { query } from '$lib/server/db';
```

### CSRF 

```typescript
// ✅ SvelteKit  CSRF 
// Origin header is checked automatically for POST/PUT/DELETE/PATCH
// No additional CSRF tokens needed for form actions

// ❌  CSRF （）
// src/hooks.server.js
export const handle = sequence(
  // do NOT do this without understanding the implications
  // ({ event, resolve }) => resolve(event, { filterSerializedResponseHeaders: () => true })
);
```

### Cookie 

```typescript
// ❌  Cookie 
// src/hooks.server.js
export async function handle({ event, resolve }) {
  const token = event.cookies.get('session');
  // cookie without httpOnly, secure, sameSite flags
  event.cookies.set('session', token, {
    path: '/',
    // missing: httpOnly, secure, sameSite
  });
}

// ✅  Cookie 
import { dev } from '$app/environment';

event.cookies.set('session', token, {
  path: '/',
  httpOnly: true,          // not accessible via JS
  secure: !dev,            // HTTPS only in production
  sameSite: 'lax',         // CSRF protection
  maxAge: 60 * 60 * 24 * 7 // 1 week, explicit expiry
});
```

---

## Review Checklist

### Runes: $state / $derived / $effect

- [ ] $state ，
- [ ]  $state.raw
- [ ]  $state （）
- [ ]  $state.snapshot / unstate 
- [ ] $derived 
- [ ]  $effect  $derived 
- [ ] $effect （）
- [ ] $effect （、、WebSocket）
- [ ] async $effect  await 
- [ ]  untrack 

### Load 

- [ ]  +page.server.js（ +page.js）
- [ ]  await parent() 
- [ ] （Promise.all  Promise）
- [ ] server load 

### Form Actions

- [ ] （） form actions + POST
- [ ] fail() （、）
- [ ]  use:enhance 

### Store 

- [ ] writable/readable → $state  .svelte.js 
- [ ]  .js  runes
- [ ]  $  store 

### SSR vs CSR 

- [ ]  layout  SSR
- [ ]  API（window、document） onMount  browser guard 
- [ ] prerender  server actions

### Svelte 4 → 5 

- [ ] $: → $derived / $effect
- [ ] export let → $props()
- [ ] on:click → onclick
- [ ] createEventDispatcher →  props
- [ ] slot → @render children()
- [ ] beforeUpdate/afterUpdate → $effect.pre / $effect

### 

- [ ]  $state.raw
- [ ] {#each}  key
- [ ] load  Promise 
- [ ] 

### 

- [ ]  server load 
- [ ]  $lib/server/ 
- [ ]  CSRF 
- [ ] Cookie  httpOnly、secure、sameSite
- [ ] server load 
