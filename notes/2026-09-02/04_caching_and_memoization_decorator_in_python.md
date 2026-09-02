# Caching & Memoization Decorator in Python

> **Source:** [YouTube Lecture](https://youtu.be/ZEKiIwWv9nM?si=uEq-ADaTkXLOYnpM)  
> **Date:** 2026-09-02  
> **Topic:** Practical Problem 3 - Optimizing Expensive Computations via Function Scope Caches

---

## 🎯 Problem Statement
When functions perform expensive computations (such as calculating Fibonacci numbers, complex math, or fetching data from a database/API), calling them repeatedly with identical arguments wastes CPU cycles and adds unnecessary latency.

**Memoization** is an optimization technique where you store the results of expensive function calls in a cache and return the cached result when the same inputs occur again.

---

## 💻 Implementation: The `@cache` / Memoization Decorator

```python
import time

def cache(func):
    """Decorator to cache function results based on arguments."""
    cache_store = {}  # Retained in closure memory across invocations
    
    def wrapper(*args):
        # Check if result is already in memory cache
        if args in cache_store:
            print(f"[CACHE HIT] Returning cached result for args: {args}")
            return cache_store[args]
        
        print(f"[CACHE MISS] Computing new result for args: {args}...")
        result = func(*args)
        cache_store[args] = result  # Store for future calls
        return result
        
    return wrapper
```

---

## 🧪 Testing the Decorator

```python
@cache
def expensive_calculation(a, b):
    time.sleep(2)  # Simulate expensive DB query or calculation
    return a ** b

# First call (Cache Miss - Takes ~2 seconds)
print("Result 1:", expensive_calculation(2, 10))

# Second call with same inputs (Cache Hit - Instantaneous)
print("Result 2:", expensive_calculation(2, 10))

# New inputs (Cache Miss - Takes ~2 seconds)
print("Result 3:", expensive_calculation(3, 4))

# Repeating new inputs (Cache Hit - Instantaneous)
print("Result 4:", expensive_calculation(3, 4))
```

### 🖥️ Expected Output:
```text
[CACHE MISS] Computing new result for args: (2, 10)...
Result 1: 1024
[CACHE HIT] Returning cached result for args: (2, 10)
Result 2: 1024
[CACHE MISS] Computing new result for args: (3, 4)...
Result 3: 81
[CACHE HIT] Returning cached result for args: (3, 4)
Result 4: 81
```

---

## 🧠 Memory Model & Closures (Under the Hood)
How does `cache_store` persist between function calls without using global variables?

- When `cache(expensive_calculation)` is defined, Python creates a **Closure**.
- The inner `wrapper` retains a reference in its `__closure__` attribute to the `cache_store` dictionary living in the enclosing scope of `cache`.
- As long as the decorated function remains in memory, its `cache_store` dictionary persists across all calls.

```
cache() scope:
  ┌─────────────────────────┐
  │  cache_store = {        │ ◄─── Persistent closure reference
  │    (2, 10): 1024,       │
  │    (3, 4):  81          │
  │  }                      │
  └───────────┬─────────────┘
              │
              ▼
      wrapper(*args)
```

---

## ⚡ Built-in Alternative: `functools.lru_cache`
Python's standard library provides a production-grade LRU (Least Recently Used) cache:
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(50))  # Computed instantly in O(N) instead of O(2^N)
```

---

## 📝 Summary & Key Takeaways
- **Memoization** dramatically speeds up idempotent, pure functions by caching output values.
- **Closure Scope:** Dictionaries declared inside the decorator function serve as private, persistent in-memory stores.
- **Tuples as Keys:** `args` (a tuple) is hashable and can be used directly as a dictionary key.
- For production applications, utilize `functools.lru_cache` to prevent unbounded memory growth.
