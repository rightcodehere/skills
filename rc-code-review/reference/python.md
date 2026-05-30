# Python Code Review Guide

> Python ，、async/await、、、。

## 

- [](#)
- [](#)
- [](#)
- [](#)
- [](#)
- [](#)
- [](#)
- [Review Checklist](#review-checklist)

---

## 

### 

```python
# ❌ ，IDE 
def process_data(data, count):
    return data[:count]

# ✅ 
def process_data(data: str, count: int) -> str:
    return data[:count]

# ✅  typing 
from typing import Optional, Union

def find_user(user_id: int) -> Optional[User]:
    """ None"""
    return db.get(user_id)

def handle_input(value: Union[str, int]) -> str:
    """"""
    return str(value)
```

### 

```python
from typing import List, Dict, Set, Tuple, Sequence

# ❌ 
def get_names(users: list) -> list:
    return [u.name for u in users]

# ✅ （Python 3.9+  list[User]）
def get_names(users: List[User]) -> List[str]:
    return [u.name for u in users]

# ✅  Sequence（）
def process_items(items: Sequence[str]) -> int:
    return len(items)

# ✅ 
def count_words(text: str) -> Dict[str, int]:
    words: Dict[str, int] = {}
    for word in text.split():
        words[word] = words.get(word, 0) + 1
    return words

# ✅ （）
def get_point() -> Tuple[float, float]:
    return (1.0, 2.0)

# ✅ 
def get_scores() -> Tuple[int, ...]:
    return (90, 85, 92, 88)
```

###  TypeVar

```python
from typing import TypeVar, Generic, List, Callable

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# ✅ 
def first(items: List[T]) -> T | None:
    return items[0] if items else None

# ✅  TypeVar
from typing import Hashable
H = TypeVar('H', bound=Hashable)

def dedupe(items: List[H]) -> List[H]:
    return list(set(items))

# ✅ 
class Cache(Generic[K, V]):
    def __init__(self) -> None:
        self._data: Dict[K, V] = {}

    def get(self, key: K) -> V | None:
        return self._data.get(key)

    def set(self, key: K, value: V) -> None:
        self._data[key] = value
```

### Callable 

```python
from typing import Callable, Awaitable

# ✅ 
Handler = Callable[[str, int], bool]

def register_handler(name: str, handler: Handler) -> None:
    handlers[name] = handler

# ✅ 
AsyncHandler = Callable[[str], Awaitable[dict]]

async def fetch_with_handler(
    url: str,
    handler: AsyncHandler
) -> dict:
    return await handler(url)

# ✅ 
def create_multiplier(factor: int) -> Callable[[int], int]:
    def multiplier(x: int) -> int:
        return x * factor
    return multiplier
```

### TypedDict 

```python
from typing import TypedDict, Required, NotRequired

# ✅ 
class UserDict(TypedDict):
    id: int
    name: str
    email: str
    age: NotRequired[int]  # Python 3.11+

def create_user(data: UserDict) -> User:
    return User(**data)

# ✅ 
class ConfigDict(TypedDict, total=False):
    debug: bool
    timeout: int
    host: Required[str]  # 
```

### Protocol 

```python
from typing import Protocol, runtime_checkable

# ✅ （）
class Readable(Protocol):
    def read(self, size: int = -1) -> bytes: ...

class Closeable(Protocol):
    def close(self) -> None: ...

# 
class ReadableCloseable(Readable, Closeable, Protocol):
    pass

def process_stream(stream: Readable) -> bytes:
    return stream.read()

# ✅ 
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...

def render(obj: object) -> None:
    if isinstance(obj, Drawable):  # 
        obj.draw()
```

---

## 

### async/await 

```python
import asyncio

# ❌ 
def fetch_all_sync(urls: list[str]) -> list[str]:
    results = []
    for url in urls:
        results.append(requests.get(url).text)  # 
    return results

# ✅ 
async def fetch_url(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def fetch_all(urls: list[str]) -> list[str]:
    tasks = [fetch_url(url) for url in urls]
    return await asyncio.gather(*tasks)  # 
```

### 

```python
from contextlib import asynccontextmanager
from typing import AsyncIterator

# ✅ 
class AsyncDatabase:
    async def __aenter__(self) -> 'AsyncDatabase':
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.disconnect()

# ✅ 
@asynccontextmanager
async def get_connection() -> AsyncIterator[Connection]:
    conn = await create_connection()
    try:
        yield conn
    finally:
        await conn.close()

async def query_data():
    async with get_connection() as conn:
        return await conn.fetch("SELECT * FROM users")
```

### 

```python
from typing import AsyncIterator

# ✅ 
async def fetch_pages(url: str) -> AsyncIterator[dict]:
    page = 1
    while True:
        data = await fetch_page(url, page)
        if not data['items']:
            break
        yield data
        page += 1

# ✅ 
async def process_all_pages():
    async for page in fetch_pages("https://api.example.com"):
        await process_page(page)
```

### 

```python
import asyncio

# ❌ 
async def bad_worker():
    while True:
        await do_work()  # 

# ✅ 
async def good_worker():
    try:
        while True:
            await do_work()
    except asyncio.CancelledError:
        await cleanup()  # 
        raise  # ，

# ✅ 
async def fetch_with_timeout(url: str) -> str:
    try:
        async with asyncio.timeout(10):  # Python 3.11+
            return await fetch_url(url)
    except asyncio.TimeoutError:
        return ""

# ✅ （Python 3.11+）
async def fetch_multiple():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_url("url1"))
        task2 = tg.create_task(fetch_url("url2"))
    # ，
    return task1.result(), task2.result()
```

### 

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

# ✅ 
async def run_sync_in_async():
    loop = asyncio.get_event_loop()
    # 
    result = await loop.run_in_executor(
        None,  # 
        blocking_io_function,
        arg1, arg2
    )
    return result

# ✅ 
def run_async_in_sync():
    return asyncio.run(async_function())

# ❌  time.sleep
async def bad_delay():
    time.sleep(1)  # ！

# ✅  asyncio.sleep
async def good_delay():
    await asyncio.sleep(1)
```

### 

```python
import asyncio

# ✅ 
async def fetch_with_limit(urls: list[str], max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url: str) -> str:
        async with semaphore:
            return await fetch_url(url)

    return await asyncio.gather(*[fetch_one(url) for url in urls])

# ✅  asyncio.Queue -
async def producer_consumer():
    queue: asyncio.Queue[str] = asyncio.Queue(maxsize=100)

    async def producer():
        for item in items:
            await queue.put(item)
        await queue.put(None)  # 

    async def consumer():
        while True:
            item = await queue.get()
            if item is None:
                break
            await process(item)
            queue.task_done()

    await asyncio.gather(producer(), consumer())
```

---

## 

### 

```python
# ❌ Catching too broad
try:
    result = risky_operation()
except:  # Catches everything, even KeyboardInterrupt!
    pass

# ❌  Exception 
try:
    result = risky_operation()
except Exception:
    pass  # ，

# ✅ Catch specific exceptions
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise
except IOError as e:
    logger.error(f"IO error: {e}")
    return default_value

# ✅ 
try:
    result = parse_and_process(data)
except (ValueError, TypeError, KeyError) as e:
    logger.error(f"Data error: {e}")
    raise DataProcessingError(str(e)) from e
```

### 

```python
# ❌ 
try:
    result = external_api.call()
except APIError as e:
    raise RuntimeError("API failed")  # 

# ✅  from 
try:
    result = external_api.call()
except APIError as e:
    raise RuntimeError("API failed") from e

# ✅ （）
try:
    result = external_api.call()
except APIError:
    raise RuntimeError("API failed") from None
```

### 

```python
# ✅ 
class AppError(Exception):
    """"""
    pass

class ValidationError(AppError):
    """"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class NotFoundError(AppError):
    """"""
    def __init__(self, resource: str, id: str | int):
        self.resource = resource
        self.id = id
        super().__init__(f"{resource} with id {id} not found")

# 
def get_user(user_id: int) -> User:
    user = db.get(user_id)
    if not user:
        raise NotFoundError("User", user_id)
    return user
```

### 

```python
from contextlib import contextmanager

# ✅ 
@contextmanager
def transaction():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# ✅  ExceptionGroup（Python 3.11+）
def process_batch(items: list) -> None:
    errors = []
    for item in items:
        try:
            process(item)
        except Exception as e:
            errors.append(e)

    if errors:
        raise ExceptionGroup("Batch processing failed", errors)
```

---

## 

### 

```python
# ❌ Mutable default arguments
def add_item(item, items=[]):  # Bug! Shared across calls
    items.append(item)
    return items

# 
add_item(1)  # [1]
add_item(2)  # [1, 2]  [2]！

# ✅ Use None as default
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# ✅  dataclass  field
from dataclasses import dataclass, field

@dataclass
class Container:
    items: list = field(default_factory=list)
```

### 

```python
# ❌ Using mutable class attributes
class User:
    permissions = []  # Shared across all instances!

# 
u1 = User()
u2 = User()
u1.permissions.append("admin")
print(u2.permissions)  # ["admin"] - ！

# ✅ Initialize in __init__
class User:
    def __init__(self):
        self.permissions = []

# ✅  dataclass
@dataclass
class User:
    permissions: list = field(default_factory=list)
```

### 

```python
# ❌ 
funcs = []
for i in range(3):
    funcs.append(lambda: i)

print([f() for f in funcs])  # [2, 2, 2]  [0, 1, 2]！

# ✅ 
funcs = []
for i in range(3):
    funcs.append(lambda i=i: i)

print([f() for f in funcs])  # [0, 1, 2]

# ✅  functools.partial
from functools import partial

funcs = [partial(lambda x: x, i) for i in range(3)]
```

### is vs ==

```python
# ❌  is 
if x is 1000:  # ！
    pass

# Python  (-5  256)
a = 256
b = 256
a is b  # True

a = 257
b = 257
a is b  # False！

# ✅  == 
if x == 1000:
    pass

# ✅ is  None 
if x is None:
    pass

if x is True:  # 
    pass
```

### 

```python
# ❌ 
result = ""
for item in large_list:
    result += str(item)  # O(n²) 

# ✅  join
result = "".join(str(item) for item in large_list)  # O(n)

# ✅  StringIO 
from io import StringIO

buffer = StringIO()
for item in large_list:
    buffer.write(str(item))
result = buffer.getvalue()
```

---

## 

### pytest 

```python
import pytest

# ✅ 
def test_user_creation_with_valid_email():
    user = User(email="test@example.com")
    assert user.email == "test@example.com"

def test_user_creation_with_invalid_email_raises_error():
    with pytest.raises(ValidationError):
        User(email="invalid")

# ✅ 
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
    ("123", "123"),
])
def test_uppercase(input: str, expected: str):
    assert input.upper() == expected

# ✅ 
def test_division_by_zero():
    with pytest.raises(ZeroDivisionError) as exc_info:
        1 / 0
    assert "division by zero" in str(exc_info.value)
```

### Fixtures

```python
import pytest
from typing import Generator

# ✅  fixture
@pytest.fixture
def user() -> User:
    return User(name="Test User", email="test@example.com")

def test_user_name(user: User):
    assert user.name == "Test User"

# ✅  fixture
@pytest.fixture
def database() -> Generator[Database, None, None]:
    db = Database()
    db.connect()
    yield db
    db.disconnect()  # 

# ✅  fixture
@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient() as client:
        yield client

# ✅  fixture（conftest.py）
# conftest.py
@pytest.fixture(scope="session")
def app():
    """ app """
    return create_app()

@pytest.fixture(scope="module")
def db(app):
    """"""
    return app.db
```

### Mock  Patch

```python
from unittest.mock import Mock, patch, AsyncMock

# ✅ Mock 
def test_send_email():
    mock_client = Mock()
    mock_client.send.return_value = True

    service = EmailService(client=mock_client)
    result = service.send_welcome_email("user@example.com")

    assert result is True
    mock_client.send.assert_called_once_with(
        to="user@example.com",
        subject="Welcome!",
        body=ANY,
    )

# ✅ Patch 
@patch("myapp.services.external_api.call")
def test_with_patched_api(mock_call):
    mock_call.return_value = {"status": "ok"}

    result = process_data()

    assert result["status"] == "ok"

# ✅  Mock
async def test_async_function():
    mock_fetch = AsyncMock(return_value={"data": "test"})

    with patch("myapp.client.fetch", mock_fetch):
        result = await get_data()

    assert result == {"data": "test"}
```

### 

```python
# ✅ 
class TestUserAuthentication:
    """"""

    def test_login_with_valid_credentials(self, user):
        assert authenticate(user.email, "password") is True

    def test_login_with_invalid_password(self, user):
        assert authenticate(user.email, "wrong") is False

    def test_login_locks_after_failed_attempts(self, user):
        for _ in range(5):
            authenticate(user.email, "wrong")
        assert user.is_locked is True

# ✅  mark 
@pytest.mark.slow
def test_large_data_processing():
    pass

@pytest.mark.integration
def test_database_connection():
    pass

# ：pytest -m "not slow"
```

### 

```python
# pytest.ini  pyproject.toml
[tool.pytest.ini_options]
addopts = "--cov=myapp --cov-report=term-missing --cov-fail-under=80"
testpaths = ["tests"]

# ✅ 
def test_empty_input():
    assert process([]) == []

def test_none_input():
    with pytest.raises(TypeError):
        process(None)

def test_large_input():
    large_data = list(range(100000))
    result = process(large_data)
    assert len(result) == 100000
```

---

## 

### 

```python
# ❌  O(n)
if item in large_list:  # 
    pass

# ✅  O(1)
large_set = set(large_list)
if item in large_set:  # 
    pass

# ✅  collections 
from collections import Counter, defaultdict, deque

# 
word_counts = Counter(words)
most_common = word_counts.most_common(10)

# 
graph = defaultdict(list)
graph[node].append(neighbor)

# （ O(1)）
queue = deque()
queue.appendleft(item)  # O(1) vs list.insert(0, item) O(n)
```

### 

```python
# ❌ 
def get_all_users():
    return [User(row) for row in db.fetch_all()]  # 

# ✅ 
def get_all_users():
    for row in db.fetch_all():
        yield User(row)  # 

# ✅ 
sum_of_squares = sum(x**2 for x in range(1000000))  # 

# ✅ itertools 
from itertools import islice, chain, groupby

#  10 
first_10 = list(islice(infinite_generator(), 10))

# 
all_items = chain(list1, list2, list3)

# 
for key, group in groupby(sorted(items, key=get_key), key=get_key):
    process_group(key, list(group))
```

### 

```python
from functools import lru_cache, cache

# ✅ LRU 
@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    return sum(i**2 for i in range(n))

# ✅ （Python 3.9+）
@cache
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# ✅ （）
class DataService:
    def __init__(self):
        self._cache: dict[str, Any] = {}
        self._cache_ttl: dict[str, float] = {}

    def get_data(self, key: str) -> Any:
        if key in self._cache:
            if time.time() < self._cache_ttl[key]:
                return self._cache[key]

        data = self._fetch_data(key)
        self._cache[key] = data
        self._cache_ttl[key] = time.time() + 300  # 5 
        return data
```

### 

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# ✅ IO 
def fetch_all_urls(urls: list[str]) -> list[str]:
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_url, urls))
    return results

# ✅ CPU 
def process_large_dataset(data: list) -> list:
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(heavy_computation, data))
    return results

# ✅  as_completed 
from concurrent.futures import as_completed

with ThreadPoolExecutor() as executor:
    futures = {executor.submit(fetch, url): url for url in urls}
    for future in as_completed(futures):
        url = futures[future]
        try:
            result = future.result()
        except Exception as e:
            print(f"{url} failed: {e}")
```

---

## 

### PEP 8 

```python
# ✅ 
class MyClass:  #  PascalCase
    MAX_SIZE = 100  #  UPPER_SNAKE_CASE

    def method_name(self):  #  snake_case
        local_var = 1  #  snake_case

# ✅ 
# 1. 
import os
import sys
from typing import Optional

# 2. 
import numpy as np
import pandas as pd

# 3. 
from myapp import config
from myapp.utils import helper

# ✅ （79  88 ）
# 
result = (
    long_function_name(arg1, arg2, arg3)
    + another_long_function(arg4, arg5)
)

# ✅ 
class MyClass:
    """"""

    def method_one(self):
        pass

    def method_two(self):  # 
        pass


def top_level_function():  # 
    pass
```

### 

```python
# ✅ Google 
def calculate_area(width: float, height: float) -> float:
    """。

    Args:
        width: （）。
        height: （）。

    Returns:
        。

    Raises:
        ValueError:  width  height 。

    Example:
        >>> calculate_area(3, 4)
        12.0
    """
    if width < 0 or height < 0:
        raise ValueError("Dimensions must be positive")
    return width * height

# ✅ 
class DataProcessor:
    """。

    Attributes:
        source: 。
        format: （'json'  'csv'）。

    Example:
        >>> processor = DataProcessor("data.csv")
        >>> processor.process()
    """
```

###  Python 

```python
# ✅ f-string（Python 3.6+）
name = "World"
print(f"Hello, {name}!")

# 
print(f"Result: {1 + 2 = }")  # "Result: 1 + 2 = 3"

# ✅ （Python 3.8+）
if (n := len(items)) > 10:
    print(f"List has {n} items")

# ✅ （Python 3.8+）
def greet(name, /, greeting="Hello", *, punctuation="!"):
    """name ，punctuation """
    return f"{greeting}, {name}{punctuation}"

# ✅ （Python 3.10+）
def handle_response(response: dict):
    match response:
        case {"status": "ok", "data": data}:
            return process_data(data)
        case {"status": "error", "message": msg}:
            raise APIError(msg)
        case _:
            raise ValueError("Unknown response format")
```

---

## Review Checklist

### 
- [ ] （）
- [ ]  `Optional`  None
- [ ] 
- [ ] mypy （）
- [ ]  `Any`，

### 
- [ ] async/await 
- [ ] 
- [ ]  `CancelledError`
- [ ]  `asyncio.gather`  `TaskGroup` 
- [ ] （async context manager）

### 
- [ ] ， `except:`
- [ ]  `from` 
- [ ] 
- [ ] ，

### 
- [ ] （list、dict、set）
- [ ] 
- [ ] （set vs list ）
- [ ] 

### 
- [ ] （ ≥80%）
- [ ] 
- [ ] 
- [ ] Mock 
- [ ] 

### 
- [ ]  PEP 8 
- [ ]  docstring
- [ ] （、、）
- [ ] 
- [ ]  Python （f-string、walrus operator ）

### 
- [ ] 
- [ ]  join
- [ ] （@lru_cache）
- [ ] IO/CPU 
