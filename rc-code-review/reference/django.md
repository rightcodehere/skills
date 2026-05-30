# Django / DRF Code Review Guide

> Django / DRF ，、N+1 、Serializer 、ViewSet 、。

## 

- [](#)
- [N+1 ](#n1-)
- [Serializer ](#serializer-)
- [ViewSet ](#viewset-)
- [](#)
- [](#)
- [Review Checklist](#review-checklist)

---

## 

### XSS 

```python
from django.utils.safestring import mark_safe
from django.template import engines

# ❌ mark_safe ，
def user_profile(request):
    user_bio = request.user.bio  # 
    return HttpResponse(mark_safe(f"<p>{user_bio}</p>"))

# ❌  autoescape
# {% autoescape off %}{{ user_bio }}{% endautoescape %}

# ✅  Django 
# template: <p>{{ user_bio }}</p>

# ✅  mark_safe ，
from django.utils.html import escape

def render_bio(bio: str) -> str:
    return mark_safe(f"<p>{escape(bio)}</p>")
```

### CSRF 

```python
from django.views.decorators.csrf import csrf_exempt

# ❌  CSRF 
@csrf_exempt
def process_payment(request):
    # 
    amount = request.POST["amount"]
    charge(amount)

# ✅  CSRF 
from django.middleware.csrf import CsrfViewMiddleware

# settings.py —  CSRF 
MIDDLEWARE = [
    # ...
    "django.middleware.csrf.CsrfViewMiddleware",
    # ...
]

# ✅ API  token  CSRF
# settings.py
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}

# ✅  AJAX  CSRF token
# JavaScript: fetch("/api/endpoint/", {
#   headers: {"X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value}
# })
```

### Cookie 

```python
# settings.py

# ❌  cookie 
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False

# ✅  cookie 
SESSION_COOKIE_SECURE = True    # HTTPS only
SESSION_COOKIE_HTTPONLY = True   # JavaScript 
SESSION_COOKIE_SAMESITE = "Lax"  #  CSRF
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"
```

### SQL 

```python
from django.db import connection

# ❌  SQL — SQL 
def search_users(keyword):
    query = f"SELECT * FROM auth_user WHERE username LIKE '%{keyword}%'"
    with connection.cursor() as cursor:
        cursor.execute(query)

# ❌ extra() 
User.objects.extra(
    where=[f"username = '{keyword}'"]
)

# ✅  ORM 
def search_users(keyword):
    return User.objects.filter(username__icontains=keyword)

# ✅  SQL 
def search_users(keyword):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM auth_user WHERE username LIKE %s",
            [f"%{keyword}%"],
        )

# ✅  raw() 
User.objects.raw(
    "SELECT * FROM auth_user WHERE username LIKE %s",
    [f"%{keyword}%"],
)
```

### 

```python
# settings.py

# ❌ 
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5 MB — 
MEDIA_ROOT = "/var/www/uploads"         # web 
ALLOWED_UPLOAD_TYPES = None             # 

# ✅ 
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440   # 2.5 MB in-memory
MEDIA_ROOT = "/srv/media/"              # web 

# ✅ 
import mimetypes
from pathlib import Path

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}

def validate_upload(file):
    ext = Path(file.name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"File type {ext} is not allowed.")
    mime, _ = mimetypes.guess_type(file.name)
    if mime not in {"image/jpeg", "image/png", "application/pdf"}:
        raise ValidationError("Invalid MIME type.")
```

---

## N+1 

### select_related（ForeignKey / OneToOne）

```python
# ❌ N+1: 
books = Book.objects.all()
for book in books:
    print(book.publisher.name)  #  N 

# ✅ select_related  JOIN 
books = Book.objects.select_related("publisher")
for book in books:
    print(book.publisher.name)  # 

# ✅ 
books = Book.objects.select_related("publisher", "publisher__country")

# ✅ （）
books = Book.objects.select_related("publisher").only(
    "title", "publisher__name"
)
```

### prefetch_related（M2M /  ForeignKey）

```python
# ❌ N+1: 
authors = Author.objects.all()
for author in authors:
    print(author.books.all())  #  N 

# ✅ prefetch_related  + Python 
authors = Author.objects.prefetch_related("books")
for author in authors:
    print(list(author.books.all()))  # 

# ✅  prefetch
authors = Author.objects.prefetch_related(
    "books",
    "books__publisher",
)

# ✅ Prefetch 
from django.db.models import Prefetch

authors = Author.objects.prefetch_related(
    Prefetch(
        "books",
        queryset=Book.objects.filter(published=True).only("title", "author_id"),
        to_attr="published_books",
    )
)
for author in authors:
    print(author.published_books)  # ， to_attr 
```

### QuerySet 

```python
# ❌  QuerySet
qs = Book.objects.all()
count = len(qs)             #  1: SELECT COUNT(*)
titles = [b.title for b in qs]  #  2: SELECT * — ！

# ✅  count() 
qs = Book.objects.all()
count = qs.count()          # SELECT COUNT(*) — 
titles = [b.title for b in qs]  # SELECT * — 

# ✅ ， list
books = list(Book.objects.all())  # 
count = len(books)
titles = [b.title for b in books]
```

### 

```python
# ❌ 
qs = Book.objects.all()[:10]   # ：
first = list(qs)               #  1
second = list(qs)              #  2 — ！

# ✅  list
books = list(Book.objects.all()[:10])  # 
first = books
second = list(books)  #  Python list，
```

### len() vs count()

```python
# ❌ len() 
total = len(Book.objects.all())  # SELECT * FROM book — 

# ✅ count() 
total = Book.objects.count()  # SELECT COUNT(*) — 

# ✅  QuerySet ， len
books = list(Book.objects.filter(published=True))
total = len(books)  # ，
```

### if qs vs qs.exists()

```python
# ❌ if qs 
qs = Book.objects.filter(author_id=author_id)
if qs:  # SELECT * FROM book WHERE ... — 
    return qs[0]

# ✅ exists() 
if Book.objects.filter(author_id=author_id).exists():
    return Book.objects.filter(author_id=author_id).first()

# ✅  get/first 
book = Book.objects.filter(author_id=author_id).first()
if book is not None:
    return book
```

---

## Serializer 

### 

```python
from rest_framework import serializers

# ❌ __all__ ，
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"  #  hash、is_superuser 

# ✅ 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

# ✅  exclude 
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ["internal_notes", "admin_flags"]

# ✅  write_only
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
```

### 

```python
from rest_framework import serializers

# ❌ ，
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["quantity", "price", "discount"]

# ✅ 
class OrderSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1, max_value=100)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    discount = serializers.DecimalField(
        max_digits=5, decimal_places=2, min_value=0, max_value=1, required=False
    )

    class Meta:
        model = Order
        fields = ["quantity", "price", "discount"]

# ✅ 
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["quantity", "price", "discount"]

    def validate(self, attrs):
        if attrs.get("discount", 0) > 0.5 and attrs.get("quantity", 0) < 10:
            raise serializers.ValidationError(
                "Bulk discount requires minimum 10 items."
            )
        return attrs

# ✅ 
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["start_date", "end_date", "room"]

    def validate_start_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Start date cannot be in the past.")
        return value

    def validate(self, attrs):
        if attrs["end_date"] <= attrs["start_date"]:
            raise serializers.ValidationError("End date must be after start date.")
        return attrs
```

### 

```python
from rest_framework import serializers

# ❌  Serializer  create/update
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)  # 

    class Meta:
        model = Article
        fields = ["id", "title", "tags"]

# ✅  1:  + PrimaryKeyRelatedField 
class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        source="tags",
    )

    class Meta:
        model = Article
        fields = ["id", "title", "tags", "tag_ids"]

# ✅  2:  create() 
class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Article
        fields = ["id", "title", "tags"]

    def create(self, validated_data):
        tags_data = validated_data.pop("tags")
        article = Article.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            article.tags.add(tag)
        return article

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", None)
        instance = super().update(instance, validated_data)
        if tags_data is not None:
            instance.tags.clear()
            for tag_data in tags_data:
                tag, _ = Tag.objects.get_or_create(**tag_data)
                instance.tags.add(tag)
        return instance
```

### read_only_fields 

```python
from rest_framework import serializers

# ❌ 
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "body", "author", "created_at", "updated_at"]
        # created_at, updated_at, author 

# ✅ 
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "body", "author", "created_at", "updated_at"]
        read_only_fields = ["author", "created_at", "updated_at"]

# ✅ （）
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

---

## ViewSet 

### 

```python
from rest_framework import viewsets

# ❌ ModelViewSet  CRUD，
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    #  destroy, update, create — 

# ✅  ReadOnlyModelViewSet
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    #  list  retrieve

# ✅  Mixin
from rest_framework import mixins

class TagViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
```

### 

```python
from rest_framework import viewsets

# ❌ 
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

# ✅ get_queryset 
class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.filter(
            owner=self.request.user
        ).select_related("owner")

# ✅ ，
class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        qs = Document.objects.select_related("owner")
        if self.request.user.is_staff:
            return qs
        return qs.filter(owner=self.request.user)

# ✅ perform_create 
class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

### 

```python
from rest_framework import permissions, viewsets

# ❌ 
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# ✅ 
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ 
from rest_framework.decorators import action

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

# ✅ 
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
```

### 

```python
# settings.py

# ❌ 
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
}

# ✅ 
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
    },
}

# ✅ 
from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = StandardPagination
```

---

## 

###  ORM 

```python
import asyncio
from asgiref.sync import sync_to_async
from django.http import JsonResponse

# ❌  async  ORM — 
async def user_list(request):
    users = User.objects.all()  # Synchronous ORM call in async context!
    data = [{"id": u.id, "name": u.username} for u in users]
    return JsonResponse(data, safe=False)

# ✅  async ORM（Django 4.1+）
async def user_list(request):
    users = User.objects.all()
    data = []
    async for user in users:  # async iteration
        data.append({"id": user.id, "name": user.username})
    return JsonResponse(data, safe=False)

# ✅  aget / afilter / acreate
async def user_detail(request, pk):
    user = await User.objects.aget(pk=pk)
    return JsonResponse({"id": user.id, "name": user.username})

# ✅  sync_to_async
@sync_to_async
def get_user_with_profile(pk):
    return User.objects.select_related("profile").get(pk=pk)

async def user_profile(request, pk):
    user = await get_user_with_profile(pk)
    return JsonResponse({
        "id": user.id,
        "name": user.username,
        "bio": user.profile.bio,
    })
```

###  await

```python
from django.http import JsonResponse

# ❌  await — coroutine ，
async def user_detail(request, pk):
    user = User.objects.aget(pk=pk)  # Missing await!
    # user  coroutine ， User 
    return JsonResponse({"name": user.username})  # RuntimeError

# ✅  await  ORM 
async def user_detail(request, pk):
    user = await User.objects.aget(pk=pk)
    return JsonResponse({"name": user.username})

# ✅ aget_or_404 
from django.shortcuts import aget_object_or_404

async def user_detail(request, pk):
    user = await aget_object_or_404(User, pk=pk)
    return JsonResponse({"name": user.username})
```

### 

```python
from django.db import transaction
from asgiref.sync import sync_to_async

# ❌ transaction.atomic() ， async 
async def create_order(request):
    async with transaction.atomic():  # Error! Not async-compatible
        order = await Order.objects.acreate(total=100)
        await OrderItem.objects.acreate(order=order, product_id=1)
    return JsonResponse({"order_id": order.id})

# ✅  sync_to_async 
@sync_to_async
def _create_order_with_items():
    with transaction.atomic():
        order = Order.objects.create(total=100)
        OrderItem.objects.create(order=order, product_id=1)
        return order.id

async def create_order(request):
    order_id = await _create_order_with_items()
    return JsonResponse({"order_id": order_id})

# ✅  sync_to_async 
@sync_to_async
def _bulk_create_products(items):
    with transaction.atomic():
        products = Product.objects.bulk_create([Product(**i) for i in items])
        return [p.id for p in products]

async def import_products(request):
    ids = await _bulk_create_products(request.data)
    return JsonResponse({"ids": ids})
```

### 

```python
# ❌  async 
class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):  # sync — blocks async views
        start = time.time()
        response = self.get_response(request)
        elapsed = time.time() - start
        response["X-Elapsed"] = str(elapsed)
        return response

# ✅ 
import time

class TimingMiddleware:
    async_capable = True
    sync_capable = True

    def __init__(self, get_response):
        self.get_response = get_response

    async def __acall__(self, request):
        start = time.time()
        response = await self.get_response(request)
        elapsed = time.time() - start
        response["X-Elapsed"] = str(elapsed)
        return response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        elapsed = time.time() - start
        response["X-Elapsed"] = str(elapsed)
        return response

# ✅  Django  async 
from django.utils.decorators import sync_and_async_middleware
```

### async for 

```python
from django.http import JsonResponse

# ❌  QuerySet  async 
async def export_users(request):
    users = User.objects.all()
    data = []  # 
    for user in users:
        data.append({"id": user.id, "name": user.username})
    return JsonResponse(data, safe=False)

# ✅  async for 
async def export_users(request):
    data = []
    async for user in User.objects.all():
        data.append({"id": user.id, "name": user.username})
    return JsonResponse(data, safe=False)

# ✅  aiterator() + 
async def export_large_dataset(request):
    data = []
    async for user in User.objects.all().aiterator(chunk_size=500):
        data.append({"id": user.id, "name": user.username})
    return JsonResponse(data, safe=False)

# ✅  values() 
async def lightweight_export(request):
    data = []
    async for row in User.objects.values("id", "username"):
        data.append(row)
    return JsonResponse(data, safe=False)
```

---

## 

### 

```python
# settings.py — 

# ❌ 
DEBUG = True
SECRET_KEY = "django-insecure-..."
ALLOWED_HOSTS = ["*"]
SECURE_SSL_REDIRECT = False

# ✅ 

# ---  ---
DEBUG = False
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]  # 
ALLOWED_HOSTS = ["example.com", "www.example.com"]

# --- HTTPS ---
SECURE_SSL_REDIRECT = True          # HTTP  HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ---  ---
SECURE_HSTS_SECONDS = 31536000      # 1 year HSTS
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True   # X-Content-Type-Options: nosniff
SECURE_BROWSER_XSS_FILTER = True     # X-XSS-Protection: 1; mode=block
X_FRAME_OPTIONS = "DENY"             #  clickjacking
REFERRER_POLICY = "strict-origin-when-cross-origin"

# ---  ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
]

# --- Session ---
SESSION_COOKIE_AGE = 3600 * 8  # 8 hours
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
```

### 

```python
# settings.py

# ❌ 
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mydb",
        "USER": "admin",
        "PASSWORD": "hunter2",  # 
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# ✅ 
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "mydb"),
        "USER": os.environ.get("DB_USER", "mydb_user"),
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "OPTIONS": {
            "sslmode": "require",  #  SSL 
        },
        "CONN_MAX_AGE": 60,  # 
    }
}
```

### CORS 

```python
# settings.py (using django-cors-headers)

# ❌ 
CORS_ALLOW_ALL_ORIGINS = True

# ✅ 
CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://app.example.com",
]

# ✅  CORS 
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ORIGINS", "").split(",")
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "x-csrftoken",
]
```

### 

```python
# settings.py

# ❌ （）
LOGGING = {}

# ✅ 
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/django/app.log",
            "maxBytes": 10 * 1024 * 1024,  # 10 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
        "myapp": {
            "handlers": ["file"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        },
    },
}
```

---

## Review Checklist

### 

- [ ]  `mark_safe` 
- [ ] CSRF ， `@csrf_exempt`
- [ ] Session  CSRF cookie  `Secure`, `HttpOnly`, `SameSite`
- [ ] SQL （ORM  `raw()`），
- [ ] 
- [ ] `SECRET_KEY` ，
- [ ] `DEBUG = False` 

### HTTPS 

- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SECURE_HSTS_SECONDS` （≥ 31536000）
- [ ] `SECURE_CONTENT_TYPE_NOSNIFF = True`
- [ ] `X_FRAME_OPTIONS`  `DENY`  `SAMEORIGIN`
- [ ] `ALLOWED_HOSTS`  `"*"`
- [ ]  SSL

### N+1 

- [ ] ForeignKey  `select_related`
- [ ] M2M /  `prefetch_related`
- [ ] 
- [ ]  `count()`  `len(queryset)` 
- [ ]  `exists()`  `if queryset` 
- [ ]  `only()` / `defer()`  `values()` 
- [ ]  QuerySet 

### Serializer

- [ ]  `fields = "__all__"` 
- [ ]  `write_only=True`
- [ ] 
- [ ]  `create()` / `update()`  `read_only=True`
- [ ]  `read_only_fields` 
- [ ] Serializer 

### ViewSet

- [ ]  `ReadOnlyModelViewSet`
- [ ] `get_queryset()` 
- [ ]  `permission_classes`
- [ ]  `perform_create()`  owner/author
- [ ] （ ViewSet ）
- [ ] （throttling）

### 

- [ ] async  ORM（ `aget`/`afilter`/`sync_to_async`）
- [ ]  `await`
- [ ] `transaction.atomic()`  `sync_to_async` 
- [ ]  `async_capable = True` 
- [ ]  QuerySet  `async for` + `aiterator()`

### 

- [ ] `CORS_ALLOWED_ORIGINS`  `CORS_ALLOW_ALL_ORIGINS = True`
- [ ] （、）
- [ ] Session （`SESSION_COOKIE_AGE`）
- [ ]  RotatingFileHandler， stdout
- [ ]  `CONN_MAX_AGE` 
