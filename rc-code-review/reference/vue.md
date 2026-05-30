# Vue 3 Code Review Guide

> Vue 3 Composition API ，、Props/Emits、Watchers、Composables、Vue 3.5 。

## 

- [](#)
- [Props & Emits](#props--emits)
- [Vue 3.5 ](#vue-35-)
- [Watchers](#watchers)
- [](#)
- [Composables](#composables)
- [](#)
- [Review Checklist](#review-checklist)

---

## 

### ref vs reactive 

```vue
<!-- ✅  ref -->
<script setup lang="ts">
const count = ref(0)
const name = ref('Vue')

// ref  .value 
count.value++
</script>

<!-- ✅ / reactive（）-->
<script setup lang="ts">
const state = reactive({
  user: null,
  loading: false,
  error: null
})

// reactive 
state.loading = true
</script>

<!-- 💡 ： ref， -->
<script setup lang="ts">
const user = ref<User | null>(null)
const loading = ref(false)
const error = ref<Error | null>(null)
</script>
```

###  reactive 

```vue
<!-- ❌  reactive  -->
<script setup lang="ts">
const state = reactive({ count: 0, name: 'Vue' })
const { count, name } = state  // ！
</script>

<!-- ✅  toRefs  -->
<script setup lang="ts">
const state = reactive({ count: 0, name: 'Vue' })
const { count, name } = toRefs(state)  // 
//  ref
const count = ref(0)
const name = ref('Vue')
</script>
```

### computed 

```vue
<!-- ❌ computed  -->
<script setup lang="ts">
const fullName = computed(() => {
  console.log('Computing...')  // ！
  otherRef.value = 'changed'   // ！
  return `${firstName.value} ${lastName.value}`
})
</script>

<!-- ✅ computed  -->
<script setup lang="ts">
const fullName = computed(() => {
  return `${firstName.value} ${lastName.value}`
})
//  watch 
watch(fullName, (name) => {
  console.log('Name changed:', name)
})
</script>
```

### shallowRef 

```vue
<!-- ❌  ref  -->
<script setup lang="ts">
const largeData = ref(hugeNestedObject)  // ，
</script>

<!-- ✅  shallowRef  -->
<script setup lang="ts">
const largeData = shallowRef(hugeNestedObject)

// 
function updateData(newData) {
  largeData.value = newData  // ✅ 
}

// ❌ 
// largeData.value.nested.prop = 'new'

//  triggerRef
import { triggerRef } from 'vue'
largeData.value.nested.prop = 'new'
triggerRef(largeData)
</script>
```

---

## Props & Emits

###  props

```vue
<!-- ❌  props -->
<script setup lang="ts">
const props = defineProps<{ user: User }>()
props.user.name = 'New Name'  //  props！
</script>

<!-- ✅  emit  -->
<script setup lang="ts">
const props = defineProps<{ user: User }>()
const emit = defineEmits<{
  update: [name: string]
}>()
const updateName = (name: string) => emit('update', name)
</script>
```

### defineProps 

```vue
<!-- ❌ defineProps  -->
<script setup lang="ts">
const props = defineProps(['title', 'count'])  // 
</script>

<!-- ✅  + withDefaults -->
<script setup lang="ts">
interface Props {
  title: string
  count?: number
  items?: string[]
}
const props = withDefaults(defineProps<Props>(), {
  count: 0,
  items: () => []  // /
})
</script>
```

### defineEmits 

```vue
<!-- ❌ defineEmits  -->
<script setup lang="ts">
const emit = defineEmits(['update', 'delete'])  // 
emit('update', someValue)  // 
</script>

<!-- ✅  -->
<script setup lang="ts">
const emit = defineEmits<{
  update: [id: number, value: string]
  delete: [id: number]
  'custom-event': [payload: CustomPayload]
}>()

// 
emit('update', 1, 'new value')  // ✅
emit('update', 'wrong')  // ❌ TypeScript 
</script>
```

---

## Vue 3.5 

### Reactive Props Destructure (3.5+)

```vue
<!-- Vue 3.5 ： -->
<script setup lang="ts">
const props = defineProps<{ count: number }>()
//  props.count  toRefs
</script>

<!-- ✅ Vue 3.5+： -->
<script setup lang="ts">
const { count, name = 'default' } = defineProps<{
  count: number
  name?: string
}>()

// count  name ！
//  watch 
watch(() => count, (newCount) => {
  console.log('Count changed:', newCount)
})
</script>

<!-- ✅  -->
<script setup lang="ts">
const {
  title,
  count = 0,
  items = () => []  // （/）
} = defineProps<{
  title: string
  count?: number
  items?: () => string[]
}>()
</script>
```

### defineModel (3.4+)

```vue
<!-- ❌  v-model ： -->
<script setup lang="ts">
const props = defineProps<{ modelValue: string }>()
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

//  computed 
const value = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})
</script>

<!-- ✅ defineModel： v-model  -->
<script setup lang="ts">
//  props  emit
const model = defineModel<string>()

// 
model.value = 'new value'  //  emit
</script>
<template>
  <input v-model="model" />
</template>

<!-- ✅  v-model -->
<script setup lang="ts">
// v-model:title 
const title = defineModel<string>('title')

// 
const count = defineModel<number>('count', {
  default: 0,
  required: false
})
</script>

<!-- ✅  v-model -->
<script setup lang="ts">
const firstName = defineModel<string>('firstName')
const lastName = defineModel<string>('lastName')
</script>
<template>
  <!-- ：<MyInput v-model:first-name="first" v-model:last-name="last" /> -->
</template>

<!-- ✅ v-model  -->
<script setup lang="ts">
const [model, modifiers] = defineModel<string>()

// 
if (modifiers.capitalize) {
  //  .capitalize 
}
</script>
```

### useTemplateRef (3.5+)

```vue
<!-- ：ref  -->
<script setup lang="ts">
const inputRef = ref<HTMLInputElement | null>(null)
</script>
<template>
  <input ref="inputRef" />
</template>

<!-- ✅ useTemplateRef： -->
<script setup lang="ts">
import { useTemplateRef } from 'vue'

const input = useTemplateRef<HTMLInputElement>('my-input')

onMounted(() => {
  input.value?.focus()
})
</script>
<template>
  <input ref="my-input" />
</template>

<!-- ✅  ref -->
<script setup lang="ts">
const refKey = ref('input-a')
const dynamicInput = useTemplateRef<HTMLInputElement>(refKey)
</script>
```

### useId (3.5+)

```vue
<!-- ❌  ID  -->
<script setup lang="ts">
const id = `input-${Math.random()}`  // SSR ！
</script>

<!-- ✅ useId：SSR  ID -->
<script setup lang="ts">
import { useId } from 'vue'

const id = useId()  // ：'v-0'
</script>
<template>
  <label :for="id">Name</label>
  <input :id="id" />
</template>

<!-- ✅  -->
<script setup lang="ts">
const inputId = useId()
const errorId = useId()
</script>
<template>
  <label :for="inputId">Email</label>
  <input
    :id="inputId"
    :aria-describedby="errorId"
  />
  <span :id="errorId" class="error">{{ error }}</span>
</template>
```

### onWatcherCleanup (3.5+)

```vue
<!-- ：watch  -->
<script setup lang="ts">
watch(source, async (value, oldValue, onCleanup) => {
  const controller = new AbortController()
  onCleanup(() => controller.abort())
  // ...
})
</script>

<!-- ✅ onWatcherCleanup： -->
<script setup lang="ts">
import { onWatcherCleanup } from 'vue'

watch(source, async (value) => {
  const controller = new AbortController()
  onWatcherCleanup(() => controller.abort())

  // ，
  if (someCondition) {
    const anotherResource = createResource()
    onWatcherCleanup(() => anotherResource.dispose())
  }

  await fetchData(value, controller.signal)
})
</script>
```

### Deferred Teleport (3.5+)

```vue
<!-- ❌ Teleport  -->
<template>
  <Teleport to="#modal-container">
    <!--  #modal-container  -->
  </Teleport>
</template>

<!-- ✅ defer  -->
<template>
  <Teleport to="#modal-container" defer>
    <!--  -->
    <Modal />
  </Teleport>
</template>
```

---

## Watchers

### watch vs watchEffect

```vue
<script setup lang="ts">
// ✅ watch：，
watch(
  () => props.userId,
  async (userId) => {
    user.value = await fetchUser(userId)
  }
)

// ✅ watchEffect：，
watchEffect(async () => {
  //  props.userId
  user.value = await fetchUser(props.userId)
})

// 💡 ：
// - ？ watch
// - ？ watch
// - ？ watchEffect
</script>
```

### watch 

```vue
<!-- ❌ watch ， -->
<script setup lang="ts">
watch(searchQuery, async (query) => {
  const controller = new AbortController()
  const data = await fetch(`/api/search?q=${query}`, {
    signal: controller.signal
  })
  results.value = await data.json()
  //  query ，！
})
</script>

<!-- ✅  onCleanup  -->
<script setup lang="ts">
watch(searchQuery, async (query, _, onCleanup) => {
  const controller = new AbortController()
  onCleanup(() => controller.abort())  // 

  try {
    const data = await fetch(`/api/search?q=${query}`, {
      signal: controller.signal
    })
    results.value = await data.json()
  } catch (e) {
    if (e.name !== 'AbortError') throw e
  }
})
</script>
```

### watch 

```vue
<script setup lang="ts">
// ✅ immediate：
watch(
  userId,
  async (id) => {
    user.value = await fetchUser(id)
  },
  { immediate: true }
)

// ✅ deep：（，）
watch(
  state,
  (newState) => {
    console.log('State changed deeply')
  },
  { deep: true }
)

// ✅ flush: 'post'：DOM 
watch(
  source,
  () => {
    //  DOM
    // nextTick 
  },
  { flush: 'post' }
)

// ✅ once: true (Vue 3.4+)：
watch(
  source,
  (value) => {
    console.log(':', value)
  },
  { once: true }
)
</script>
```

### 

```vue
<script setup lang="ts">
// ✅  ref
watch(
  [firstName, lastName],
  ([newFirst, newLast], [oldFirst, oldLast]) => {
    console.log(`Name changed from ${oldFirst} ${oldLast} to ${newFirst} ${newLast}`)
  }
)

// ✅  reactive 
watch(
  () => [state.count, state.name],
  ([count, name]) => {
    console.log(`count: ${count}, name: ${name}`)
  }
)
</script>
```

---

## 

### v-for  key

```vue
<!-- ❌ v-for  index  key -->
<template>
  <li v-for="(item, index) in items" :key="index">
    {{ item.name }}
  </li>
</template>

<!-- ✅  key -->
<template>
  <li v-for="item in items" :key="item.id">
    {{ item.name }}
  </li>
</template>

<!-- ✅  key（ ID ）-->
<template>
  <li v-for="(item, index) in items" :key="`${item.name}-${item.type}-${index}`">
    {{ item.name }}
  </li>
</template>
```

### v-if  v-for 

```vue
<!-- ❌ v-if  v-for  -->
<template>
  <li v-for="user in users" v-if="user.active" :key="user.id">
    {{ user.name }}
  </li>
</template>

<!-- ✅  computed  -->
<script setup lang="ts">
const activeUsers = computed(() =>
  users.value.filter(user => user.active)
)
</script>
<template>
  <li v-for="user in activeUsers" :key="user.id">
    {{ user.name }}
  </li>
</template>

<!-- ✅  template  -->
<template>
  <template v-for="user in users" :key="user.id">
    <li v-if="user.active">
      {{ user.name }}
    </li>
  </template>
</template>
```

### 

```vue
<!-- ❌  -->
<template>
  <button @click="items = items.filter(i => i.id !== item.id); count--">
    Delete
  </button>
</template>

<!-- ✅  -->
<script setup lang="ts">
const deleteItem = (id: number) => {
  items.value = items.value.filter(i => i.id !== id)
  count.value--
}
</script>
<template>
  <button @click="deleteItem(item.id)">Delete</button>
</template>

<!-- ✅  -->
<template>
  <!--  -->
  <form @submit.prevent="handleSubmit">...</form>

  <!--  -->
  <button @click.stop="handleClick">...</button>

  <!--  -->
  <button @click.once="handleOnce">...</button>

  <!--  -->
  <input @keyup.enter="submit" @keyup.esc="cancel" />
</template>
```

---

## Composables

### Composable 

```typescript
// ✅  composable 
export function useCounter(initialValue = 0) {
  const count = ref(initialValue)

  const increment = () => count.value++
  const decrement = () => count.value--
  const reset = () => count.value = initialValue

  // 
  return {
    count: readonly(count),  // 
    increment,
    decrement,
    reset
  }
}

// ❌  .value
export function useBadCounter() {
  const count = ref(0)
  return {
    count: count.value  // ❌ ！
  }
}
```

### Props  composable

```vue
<!-- ❌  props  composable  -->
<script setup lang="ts">
const props = defineProps<{ userId: string }>()
const { user } = useUser(props.userId)  // ！
</script>

<!-- ✅  toRef  computed  -->
<script setup lang="ts">
const props = defineProps<{ userId: string }>()
const userIdRef = toRef(props, 'userId')
const { user } = useUser(userIdRef)  // 
//  computed
const { user } = useUser(computed(() => props.userId))

// ✅ Vue 3.5+：
const { userId } = defineProps<{ userId: string }>()
const { user } = useUser(() => userId)  // getter 
</script>
```

###  Composable

```typescript
// ✅  composable 
export function useFetch<T>(url: MaybeRefOrGetter<string>) {
  const data = ref<T | null>(null)
  const error = ref<Error | null>(null)
  const loading = ref(false)

  const execute = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(toValue(url))
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      data.value = await response.json()
    } catch (e) {
      error.value = e as Error
    } finally {
      loading.value = false
    }
  }

  //  URL 
  watchEffect(() => {
    toValue(url)  // 
    execute()
  })

  return {
    data: readonly(data),
    error: readonly(error),
    loading: readonly(loading),
    refetch: execute
  }
}

// 
const { data, loading, error, refetch } = useFetch<User[]>('/api/users')
```

### 

```typescript
// ✅ Composable 
export function useEventListener(
  target: MaybeRefOrGetter<EventTarget>,
  event: string,
  handler: EventListener
) {
  // 
  onMounted(() => {
    toValue(target).addEventListener(event, handler)
  })

  // 
  onUnmounted(() => {
    toValue(target).removeEventListener(event, handler)
  })
}

// ✅  effectScope 
export function useFeature() {
  const scope = effectScope()

  scope.run(() => {
    //  scope 
    const state = ref(0)
    watch(state, () => { /* ... */ })
    watchEffect(() => { /* ... */ })
  })

  // 
  onUnmounted(() => scope.stop())

  return { /* ... */ }
}
```

---

## 

### v-memo

```vue
<!-- ✅ v-memo：， -->
<template>
  <div v-for="item in list" :key="item.id" v-memo="[item.id === selected]">
    <!--  item.id === selected  -->
    <ExpensiveComponent :item="item" :selected="item.id === selected" />
  </div>
</template>

<!-- ✅  v-for  -->
<template>
  <div
    v-for="item in list"
    :key="item.id"
    v-memo="[item.name, item.status]"
  >
    <!--  name  status  -->
  </div>
</template>
```

### defineAsyncComponent

```vue
<script setup lang="ts">
import { defineAsyncComponent } from 'vue'

// ✅ 
const HeavyChart = defineAsyncComponent(() =>
  import('./components/HeavyChart.vue')
)

// ✅ 
const AsyncModal = defineAsyncComponent({
  loader: () => import('./components/Modal.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorDisplay,
  delay: 200,  //  loading（）
  timeout: 3000  // 
})
</script>
```

### KeepAlive

```vue
<template>
  <!-- ✅  -->
  <KeepAlive>
    <component :is="currentTab" />
  </KeepAlive>

  <!-- ✅  -->
  <KeepAlive include="TabA,TabB">
    <component :is="currentTab" />
  </KeepAlive>

  <!-- ✅  -->
  <KeepAlive :max="10">
    <component :is="currentTab" />
  </KeepAlive>
</template>

<script setup lang="ts">
// KeepAlive 
onActivated(() => {
  // （）
  refreshData()
})

onDeactivated(() => {
  // （）
  pauseTimers()
})
</script>
```

### 

```vue
<!-- ✅  -->
<script setup lang="ts">
import { useVirtualList } from '@vueuse/core'

const { list, containerProps, wrapperProps } = useVirtualList(
  items,
  { itemHeight: 50 }
)
</script>
<template>
  <div v-bind="containerProps" style="height: 400px; overflow: auto">
    <div v-bind="wrapperProps">
      <div v-for="item in list" :key="item.data.id" style="height: 50px">
        {{ item.data.name }}
      </div>
    </div>
  </div>
</template>
```

---

## Review Checklist

### 
- [ ] ref ，reactive （ ref）
- [ ]  reactive （ toRefs）
- [ ] props  composable 
- [ ] shallowRef/shallowReactive 
- [ ] computed 

### Props & Emits
- [ ] defineProps  TypeScript 
- [ ]  withDefaults + 
- [ ] defineEmits 
- [ ]  props
- [ ]  defineModel  v-model（Vue 3.4+）

### Vue 3.5 （）
- [ ]  Reactive Props Destructure  props 
- [ ]  useTemplateRef  ref 
- [ ]  useId  SSR  ID
- [ ]  onWatcherCleanup 

### Watchers
- [ ] watch/watchEffect 
- [ ]  watch 
- [ ] flush: 'post'  DOM  watcher
- [ ]  watcher（ computed）
- [ ]  once: true 

### 
- [ ] v-for  key
- [ ] v-if  v-for 
- [ ] 
- [ ] 

### Composables
- [ ]  composables
- [ ] composables （ .value）
- [ ]  composable
- [ ] 
- [ ]  effectScope 

### 
- [ ] 
- [ ]  defineAsyncComponent 
- [ ] 
- [ ] v-memo 
- [ ] KeepAlive 
