# Timing Function Execution with Decorators

> **Source:** [YouTube Lecture](https://youtu.be/ZEKiIwWv9nM?si=uEq-ADaTkXLOYnpM)  
> **Date:** 2026-09-02  
> **Topic:** Practical Problem 1 - Measuring Execution Latency via `@timer`

---

## 🎯 Problem Statement
In software development, you often need to benchmark and profile functions to find performance bottlenecks (e.g., database queries, mathematical computations, API calls).

Manually inserting `start_time = time.time()` and `print(end_time - start_time)` inside every function violates the **DRY (Don't Repeat Yourself)** principle and pollutes clean code.

**Solution:** Create a reusable `@timer` decorator.

---

## 💻 Implementation: The `@timer` Decorator

```python
import time

def timer(func):
    """Decorator to measure and print the execution time of any function."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        # Execute the wrapped function with any arbitrary arguments
        result = func(*args, **kwargs)
        
        end_time = time.time()
        execution_duration = end_time - start_time
        
        # Access the wrapped function's original name via __name__
        print(f"[TIMER] '{func.__name__}' ran in {execution_duration:.4f} seconds")
        
        return result
    return wrapper
```

---

## 🧪 Testing the Decorator

```python
@timer
def heavy_computation(n):
    """Simulates a CPU-heavy or I/O bound task."""
    print(f"Starting computation up to {n}...")
    time.sleep(1.5)  # Simulate network or disk latency
    total = sum(i * i for i in range(n))
    return total

# Execution
result = heavy_computation(1_000_000)
print(f"Computation Result: {result}")
```

### 🖥️ Expected Output:
```text
Starting computation up to 1000000...
[TIMER] 'heavy_computation' ran in 1.5432 seconds
Computation Result: 333332833333500000
```

---

## 🔍 Under the Hood: Why `*args` and `**kwargs` Matter
When you decorate a function:
1. `func` holds a pointer to the original function object.
2. `wrapper` intercepts any number of positional arguments (`*args` as a tuple) and keyword arguments (`**kwargs` as a dict).
3. `func(*args, **kwargs)` unpacks these parameters, ensuring the underlying function receives its exact signature without error.

```
heavy_computation(10) ──► wrapper(10)
                                │
                                └──► func(10)  (via *args unpacking)
```

---

## ⚠️ Common Pitfalls & Interview Tips

1. **Forgetting `return result`:**  
   If you forget `return result` inside the wrapper, calling `res = heavy_computation()` will return `None`. Always return the original result!
2. **Losing Function Metadata (`__name__`, `__doc__`):**  
   Decorating replaces the original function object with `wrapper`. To preserve docstrings and names in production, use `@functools.wraps(func)`:
   ```python
   from functools import wraps

   def timer(func):
       @wraps(func)
       def wrapper(*args, **kwargs):
           ...
           return result
       return wrapper
   ```

---

## 📝 Summary & Key Takeaways
- Use `@timer` whenever profiling performance across multiple functions.
- `func.__name__` exposes the identifier string of the decorated function.
- `time.time()` gives wall-clock time suitable for measuring latency.
- Unpacking `*args, **kwargs` makes your decorator universally compatible with any function signature.
