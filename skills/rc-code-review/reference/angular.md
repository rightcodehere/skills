# Angular Code Review Guide

> Angular 17+ code review guide covering Signals, Standalone components, RxJS anti-patterns, Zoneless change detection, template best practices, and performance optimization essentials.

## Table of Contents

- [Signals and Change Detection](#signals-and-change-detection)
- [Standalone Components Migration](#standalone-components-migration)
- [RxJS Anti-Patterns](#rxjs-anti-patterns)
- [Zoneless Change Detection](#zoneless-change-detection)
- [Template Best Practices](#template-best-practices)
- [Performance Optimization](#performance-optimization)
- [Review Checklist](#review-checklist)

---

## Signals and Change Detection

### Signal + OnPush Auto-Triggers Change Detection

```typescript
// ❌ Mutable state + OnPush = UI does not update
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `<p>{{ data.name }}</p>`,
})
export class UserProfile {
  data = { name: 'Alice' };
  changeName() { this.data.name = 'Bob'; } // UI will not update!
}

// ✅ Signal + OnPush = Auto change detection
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `<p>{{ name() }}</p>`,
})
export class UserProfile {
  name = signal('Alice');
  changeName() { this.name.set('Bob'); } // Auto-triggers CD
}
```

### @Input() Object Mutation Not Detected by OnPush

```typescript
// ❌ Mutate Input object - reference unchanged, OnPush does not detect
@Input() config!: Config;
updateConfig() { this.config.theme = 'dark'; }

// ✅ Create new reference
updateConfig() { this.config = { ...this.config, theme: 'dark' }; }
```

### computed() for Derived State

```typescript
// ❌ effect for state synchronization - anti-pattern, may trigger extra CD cycles
export class CartComponent {
  total = signal(0);
  discounted = signal(0);

  constructor() {
    effect(() => this.discounted.set(this.total() * 0.9));
  }
}

// ✅ computed for derived state - lazy evaluation, no side effects
export class CartComponent {
  total = signal(0);
  discounted = computed(() => this.total() * 0.9);
}
```

### Signal Reads After await in effect() Not Tracked

```typescript
// ❌ Read Signal after await - dependencies not tracked
effect(async () => {
  const data = await fetchUserData();
  console.log(`Theme: ${theme()}`); // theme() not tracked!
});

// ✅ Sync read before await
effect(async () => {
  const currentTheme = theme(); // Sync read, tracked
  const data = await fetchUserData();
  console.log(`Theme: ${currentTheme}`);
});
```

### effect() Only in Specific Scenarios

```typescript
// ❌ Use effect to sync two Signals - always use computed
effect(() => { this.filtered.set(this.items().filter(i => i.active)); });

// ✅ Legitimate effect scenarios: DOM operations, analytics logging, subscribe to external sources
effect(() => {
  const canvas = this.canvasRef.nativeElement;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = this.color();
  ctx.fillRect(0, 0, this.size(), this.size());
});

// 💡 "There are no situations where effect is good,
//    only situations where it is appropriate."
```

---

## Standalone Components Migration

### Angular 19+ standalone is Default

```typescript
// ❌ Legacy NgModule component
@Component({
  selector: 'old-component',
  standalone: false,
})
export class OldComponent {}

// ✅ Modern Standalone component (Angular 19+ standalone is default)
@Component({
  selector: 'user-profile',
  imports: [ProfilePhoto, RouterLink],
  template: `<profile-photo /><a routerLink="/edit">Edit</a>`,
})
export class UserProfile {}
```

### Review Markers

```typescript
// ⚠️ Migration signals:
// 1. standalone: false
// 2. @NgModule declarations
// 3. Component via NgModule rather than direct import

// ✅ Migration path:
// 1. Remove standalone: false
// 2. Add dependencies to component imports array
// 3. If no more declarations, delete NgModule
```

---

## RxJS Anti-Patterns

### subscribe() Must Use takeUntilDestroyed

```typescript
// ❌ Bare subscribe - memory leak! Continues receiving data after component destruction
@Component({ /* ... */ })
export class UserProfile implements OnInit {
  ngOnInit() {
    this.data$.subscribe(data => this.processData(data));
  }
}

// ✅ takeUntilDestroyed - auto-cancel on component destruction (call in constructor or injection context)
@Component({ /* ... */ })
export class UserProfile {
  constructor() {
    this.data$.pipe(takeUntilDestroyed()).subscribe(data => {
      this.processData(data);
    });
  }
}

// ✅ Use outside constructor - pass DestroyRef
@Component({ /* ... */ })
export class UserProfile {
  private destroyRef = inject(DestroyRef);

  startListening() {
    this.data$.pipe(takeUntilDestroyed(this.destroyRef)).subscribe(/* ... */);
  }
}
```

### toSignal Over AsyncPipe

```typescript
// ❌ AsyncPipe - requires import, pipe syntax in template
@Component({
  imports: [AsyncPipe],
  template: `{{ data$ | async }}`,
})

// ✅ toSignal - auto-unsubscribe, can use anywhere
export class UserProfile {
  data = toSignal(this.data$, { initialValue: null });
  // Use data() directly in template
}
```

### Avoid Repeated toSignal Calls

```typescript
// ❌ toSignal creates new subscription on each call
getData() {
  return toSignal(this.http.get('/api/data'));
}

// ✅ Store result
data = toSignal(this.http.get('/api/data'), { initialValue: null });
```

---

## Zoneless Change Detection

### Plain Property Mutation Not Detected (Angular 21+)

```typescript
// ❌ Plain property assignment does not trigger CD in Zoneless
export class UserService {
  user: User | null = null;
  loadUser() { this.user = fetchResult; } // Does not trigger!
}

// ✅ Signal auto-triggers CD
export class UserService {
  private _user = signal<User | null>(null);
  readonly user = this._user.asReadonly();
  loadUser() { this._user.set(fetchResult); }
}
```

### NgZone API Invalid in Zoneless

```typescript
// ❌ NgZone.onStable never triggers in zoneless
ngZone.onStable.subscribe(() => { /* never triggers */ });

// ✅ Use afterNextRender
afterNextRender({ write: () => { /* execute after CD */ } });
```

### Reactive Forms Mutation Needs markForCheck

```typescript
// ❌ Reactive Forms setValue/patchValue does not auto-schedule CD in zoneless
this.form.patchValue({ name: 'Alice' }); // UI may not update

// ✅ Manually mark or reflect via Signal
this.form.patchValue({ name: 'Alice' });
this.cdr.markForCheck();
```

### Valid CD Triggers in Zoneless

| Trigger | Description |
|---------|-------------|
| `signal.set()` / `.update()` | Signal updates auto-trigger |
| `ChangeDetectorRef.markForCheck()` | Manual marking |
| `ComponentRef.setInput()` | Input binding |
| Template event listener callbacks | User interactions |

---

## Template Best Practices

### Extract Complex Logic to computed Signal

```typescript
// ❌ Complex expressions in template
template: `<div *ngIf="items.filter(i => i.active).length > 0 && user.role === 'admin'">`

// ✅ Extract to computed
filteredItems = computed(() => this.items().filter(i => i.active));
shouldShow = computed(() => this.filteredItems().length > 0 && this.user().role === 'admin');
template: `@if (shouldShow()) { <div>...</div> }`
```

### Native Bindings Over NgClass / NgStyle

```typescript
// ❌ NgClass/NgStyle - extra directive overhead
template: `<div [ngClass]="{active: isActive}" [ngStyle]="{'color': textColor}">`

// ✅ Native class/style bindings - better performance
template: `<div [class.active]="isActive" [style.color]="textColor">`
```

### Mark Template-Only Members protected

```typescript
// ❂ Template-only methods exposed as public
export class UserProfile {
  formatName(name: string) { return name.trim(); }
}

// ✅ Use protected for template-only members
export class UserProfile {
  protected formatName(name: string) { return name.trim(); }
}
```

### Mark Angular-Managed Properties readonly

```typescript
// ❌ input/output/model can be accidentally overwritten
userId = input<string>();
userSaved = output<void>();

// ✅ readonly prevents accidental assignment
readonly userId = input<string>();
readonly userSaved = output<void>();
readonly userName = model<string>();
```

### Naming Convention: Action Names Not Event Names

```typescript
// ❌ Name by event
template: `<button (click)="handleClick()">Save</button>`

// ✅ Name by action
template: `<button (click)="saveUserData()">Save</button>`
```

---

## Performance Optimization

### effect is Last Resort - Prefer computed

```typescript
// ❌ effect for state sync - triggers extra CD, may infinite loop
effect(() => {
  this.filteredItems.set(this.items().filter(i => i.active));
});

// ✅ computed - lazy evaluation, no side effects, no extra CD
filteredItems = computed(() => this.items().filter(i => i.active));
```

### afterRenderEffect Separate Read/Write Phases

```typescript
// ❌ No phase specified = mixedReadWrite = extra DOM reflow
afterRenderEffect(() => {
  const height = el.offsetHeight; // read
  el.style.height = height + 10 + 'px'; // write
});

// ✅ Separate phases reduce reflow
afterRenderEffect({
  earlyRead: () => el.offsetHeight,
  write: (height) => { el.style.height = height() + 10 + 'px'; },
  read: () => verifyLayout(),
});
```

### inject() Over Constructor Injection

```typescript
// ❌ Constructor injection - hard to read with many dependencies
export class UserService {
  constructor(
    private http: HttpClient,
    private router: Router,
    private auth: AuthService,
  ) {}
}

// ✅ inject() - better type inference and readability
export class UserService {
  private http = inject(HttpClient);
  private router = inject(Router);
  private auth = inject(AuthService);
}
```

---

## Review Checklist

### Signals and Change Detection

- [ ] Signal + OnPush for template state (non-mutable objects)
- [ ] `@Input()` objects updated via new reference (non-mutation)
- [ ] Derived state uses `computed()`, not `effect()`
- [ ] Signal reads in `effect()` before `await`
- [ ] `effect()` only for DOM operations, logging, external subscriptions

### Standalone Components

- [ ] No `standalone: false` (Angular 19+)
- [ ] Component dependencies imported via `imports` array
- [ ] No unnecessary `@NgModule`

### RxJS

- [ ] `.subscribe()` paired with `takeUntilDestroyed` or `async` pipe
- [ ] Prefer `toSignal` over `AsyncPipe`
- [ ] No duplicate `toSignal` calls

### Zoneless

- [ ] Template state managed via Signal (non-plain properties)
- [ ] No `NgZone.onStable` / `NgZone.onMicrotaskEmpty`
- [ ] Reactive Forms mutations have `markForCheck()`

### Templates

- [ ] Complex logic extracted to `computed` Signal
- [ ] Use native `[class]`/`[style]` not `NgClass`/`NgStyle`
- [ ] Template-only members marked `protected`
- [ ] `input`/`output`/`model` properties marked `readonly`
- [ ] Event handlers named by action (`saveData` not `handleClick`)

### Performance

- [ ] `effect()` not used for state sync
- [ ] `afterRenderEffect` separates read/write phases
- [ ] `inject()` for dependency injection
