# NestJS Code Review Guide

> NestJS ，、、Guard/Interceptor/Pipe、DTO 、、。

## 

- [](#)
- [](#)
- [Guard / Interceptor / Pipe](#guard--interceptor--pipe)
- [ (DTO)](#-dto)
- [](#)
- [](#)
- [](#)
- [Review Checklist](#review-checklist)

---

## 

### ：Controller → Service → Repository

```typescript
// ❌ ORM  Controller， Service 
@Controller('users')
export class UsersController {
  constructor(private readonly prisma: PrismaService) {}

  @Get()
  findAll() {
    return this.prisma.user.findMany();
  }
}

// ✅ Controller → Service → Repository
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get()
  findAll() {
    return this.usersService.findAll();
  }
}

@Injectable()
export class UsersService {
  constructor(private readonly usersRepo: UsersRepository) {}

  findAll() {
    return this.usersRepo.findAll();
  }
}
```

### Repository 

```typescript
// ❌ Repository  Repository—— Service
@Injectable()
export class OrdersRepository {
  constructor(private readonly usersRepository: UsersRepository) {}
}

// ✅  Repository  Service 
@Injectable()
export class OrdersService {
  constructor(
    private readonly ordersRepo: OrdersRepository,
    private readonly usersRepo: UsersRepository,
  ) {}
}
```

### God Service： 8 

```typescript
// ❌ 9  Service
@Injectable()
export class OrdersService {
  constructor(
    private readonly ordersRepo: OrdersRepository,
    private readonly usersRepo: UsersRepository,
    private readonly productsRepo: ProductsRepository,
    private readonly paymentsService: PaymentsService,
    private readonly mailerService: MailerService,
    private readonly inventoryService: InventoryService,
    private readonly discountService: DiscountService,
    private readonly taxService: TaxService,
    private readonly auditService: AuditService,
  ) {}
}

// ✅  Use-Case Service（）
@Injectable()
export class CreateOrderService {
  constructor(
    private readonly ordersRepo: OrdersRepository,
    private readonly paymentsService: PaymentsService,
  ) {}

  async execute(dto: CreateOrderDto) { /* ... */ }
}
```

### Symbol Token 

```typescript
// ❌ ——
@Injectable()
export class UsersService {
  constructor(private readonly repo: TypeOrmUserRepository) {}
}

// ✅  + Symbol Token——
export const USER_REPOSITORY = Symbol('USER_REPOSITORY');

export interface UserRepository {
  findAll(): Promise<User[]>;
  findById(id: string): Promise<User | null>;
}

// module:
{
  provide: USER_REPOSITORY,
  useClass: TypeOrmUserRepository,
}

// service:
@Injectable()
export class UsersService {
  constructor(@Inject(USER_REPOSITORY) private readonly repo: UserRepository) {}
}
```

---

## 

### 

```
src/
  common/         ← （Guards、Filters、Interceptors、Decorators）
  core/           ← （Config、Database、Queue ）
  integrations/   ← （Mailer、Storage、Stripe、SMS）
  modules/        ← 
    [feature]/
      dtos/
      repositories/
      services/
        internal/     ←  Service
        use-cases/    ←  = 
      types/
      [feature].controller.ts
      [feature].module.ts
```

### Domain 

```typescript
// ❌ Domain Entity  NestJS——
import { Injectable } from '@nestjs/common';

@Injectable()
export class User {
  constructor(private readonly email: string) {}
}

// ✅ Domain ，
export class User {
  private constructor(private readonly email: string) {}

  static create(email: string): User {
    return new User(email);
  }
}
```

### 

- `common/`  ****——""，
- `integrations/` ； SendGrid → AWS SES 
-  **Use-Case Service**（） 15  `XxxService`

---

## Guard / Interceptor / Pipe

###  Guard 

```typescript
// ❌ Guard  + 
@Injectable()
export class OrderOwnershipGuard implements CanActivate {
  constructor(private readonly prisma: PrismaService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const req = context.switchToHttp().getRequest();
    const order = await this.prisma.order.findUnique({
      where: { id: req.params.id },
    });
    if (order.userId !== req.user.id) {
      return false; //  +  Guard 
    }
    return true;
  }
}

// ✅ Guard （/）
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private readonly reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<string[]>('roles', [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!requiredRoles) return true;
    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some((role) => user.roles?.includes(role));
  }
}
```

### Interceptor 

```typescript
// ❌ Interceptor 
@Injectable()
export class PricingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler) {
    // ——！
    return next.handle().pipe(map(data => applyDiscount(data)));
  }
}

// ✅ Interceptor 、、、
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler) {
    const now = Date.now();
    const req = context.switchToHttp().getRequest();
    return next.handle().pipe(
      tap(() => console.log(`${req.method} ${req.url} - ${Date.now() - now}ms`)),
    );
  }
}
```

###  ValidationPipe  whitelist

```typescript
// ❌  whitelist——
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
}

// ✅  ValidationPipe + whitelist 
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    }),
  );
  await app.listen(3000);
}
```

---

##  (DTO)

### @ValidateNested()  @Type()

```typescript
// ❌  @ValidateNested——！
export class CreateOrderDto {
  @ValidateNested()
  shipping: AddressDto;
}

// ✅ @ValidateNested + @Type 
import { Type } from 'class-transformer';

export class CreateOrderDto {
  @ValidateNested()
  @Type(() => AddressDto)
  shipping: AddressDto;

  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => OrderItemDto)
  items: OrderItemDto[];
}
```

###  any Body

```typescript
// ❌  DTO——、、 Swagger 
@Post()
create(@Body() body: any) {
  return this.service.create(body);
}

// ✅  DTO
export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(2)
  @MaxLength(100)
  name: string;
}

@Post()
create(@Body() dto: CreateUserDto) {
  return this.service.create(dto);
}
```

### Create  Update  DTO

```typescript
// ❌ PATCH —— API 
@Patch(':id')
update(@Body() dto: CreateUserDto) { /* all fields required */ }

// ✅ Update  PartialType
export class UpdateUserDto extends PartialType(CreateUserDto) {}

@Patch(':id')
update(@Body() dto: UpdateUserDto) { /* all fields optional */ }
```

### 

```typescript
// ❌  @IsOptional
export class UpdateOrderDto {
  @ValidateNested()
  @Type(() => AddressDto)
  shipping?: AddressDto; // undefined 
}

// ✅ @IsOptional + @ValidateNested + @Type
export class UpdateOrderDto {
  @IsOptional()
  @ValidateNested()
  @Type(() => AddressDto)
  shipping?: AddressDto;
}
```

---

## 

### 

```typescript
// ❌ catch { return null }——，""""
async findOne(id: string) {
  try {
    return await this.repo.findById(id);
  } catch (e) {
    return null;
  }
}

// ✅ 
async findOne(id: string): Promise<User> {
  const user = await this.repo.findById(id);
  if (!user) {
    throw new NotFoundException(`User ${id} not found`);
  }
  return user;
}
```

### 

```typescript
// ❌  HTTP 
throw new HttpException('Bad request', 400);

// ✅ 
throw new BadRequestException('Invalid email format');
throw new NotFoundException('User not found');
throw new ConflictException('Email already taken');
throw new ForbiddenException('Insufficient permissions');
throw new UnauthorizedException('Invalid credentials');
```

### 

```typescript
// ✅ ——
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly logger = new Logger(AllExceptionsFilter.name);

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    const request = ctx.getRequest();

    const status =
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;

    this.logger.error(`${request.method} ${request.url} - ${status}`, exception instanceof Error ? exception.stack : '');

    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
    });
  }
}
```

---

## 

### 

```typescript
// ❌ Module A ↔ Module B
@Module({ imports: [UsersModule] })
export class OrdersModule {}

@Module({ imports: [OrdersModule] })
export class UsersModule {}

// ✅ 
@Module({
  providers: [SharedService],
  exports: [SharedService],
})
export class SharedModule {}

@Module({ imports: [SharedModule] })
export class OrdersModule {}

@Module({ imports: [SharedModule] })
export class UsersModule {}
```

### forwardRef 

```typescript
// ⚠️ forwardRef ——
@Module({
  imports: [forwardRef(() => UsersModule)],
})
export class OrdersModule {}

// ✅ ：
// 1. 
// 2. （EventEmitter）
// 3.  Service
```

---

## 

### Use-Case  NestJS 

```typescript
// ✅  NestFactory—— new
describe('CreateUserHandler', () => {
  let handler: CreateUserHandler;
  let repo: InMemoryUserRepository;

  beforeEach(() => {
    repo = new InMemoryUserRepository();
    handler = new CreateUserHandler(repo);
  });

  it('creates a user', async () => {
    const id = await handler.execute(
      new CreateUserCommand('user@example.com', 'Alice'),
    );
    expect(id).toBeDefined();
  });

  it('rejects duplicate email', async () => {
    await handler.execute(new CreateUserCommand('user@example.com', 'Alice'));
    await expect(
      handler.execute(new CreateUserCommand('user@example.com', 'Bob')),
    ).rejects.toThrow('already exists');
  });
});
```

### E2E  Pipes

```typescript
describe('UsersController (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    //  main.ts 
    app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
    await app.init();
  });

  it('/POST users - valid', () => {
    return request(app.getHttpServer())
      .post('/users')
      .send({ email: 'test@test.com', name: 'Test' })
      .expect(201);
  });

  it('/POST users - extra fields rejected', () => {
    return request(app.getHttpServer())
      .post('/users')
      .send({ email: 'test@test.com', name: 'Test', role: 'admin' })
      .expect(400);
  });
});
```

---

## Review Checklist

### 

- [ ] ORM/Prisma  Controller
- [ ]  Controller 
- [ ] Repository 
- [ ] Service  ≤ 8（ Use-Case）

### 

- [ ]  + Symbol Token 
- [ ]  `forwardRef()`（，）
- [ ] Scoped  Singleton 

### 

- [ ]  `@ValidateNested()`  `@Type()`
- [ ]  `ValidationPipe({ whitelist: true, forbidNonWhitelisted: true })` 
- [ ]  `@Body() body: any`—— DTO
- [ ] Create  Update  DTO（`PartialType`）
- [ ]  `{ each: true }`
- [ ]  `@IsOptional()` + `@ValidateNested()` + `@Type()`

### Guard / Interceptor / Pipe

- [ ] Guard ，
- [ ] Interceptor （、、）
- [ ]  Service 

### 

- [ ]  `catch { return null }`——
- [ ]  NestJS 
- [ ]  `common/filters/` 

### 

- [ ] 
- [ ] Domain Entity （`@Injectable` ）
- [ ]  `integrations/` 

### 

- [ ] Use-Case Service  NestJS 
- [ ] E2E  Pipes/Guards
- [ ] Domain Entity 
