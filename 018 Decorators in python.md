# 018: Decorators in Python

Decorators are one of the most powerful and elegant design patterns in Python. They allow you to dynamically modify or extend the behavior of a function or method without permanently altering its source code.

---

## 🚦 The Tollbooth Mental Model
Think of a **decorator as a Tollbooth on a highway**:
- Every vehicle (function call) heading toward a destination (function logic) must pass through the tollbooth first.
- The tollbooth can check credentials (authentication), log entry time (telemetry/timing), or calculate fees (transform data).
- The road/destination doesn't need to know how the toll is collected—the tollbooth manages that independently.

---

## 🏗️ Core Structure of a Decorator
```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        # 1. Action BEFORE the function executes
        print("[Before] Pre-processing...")
        
        # 2. Execute original function and store result
        result = func(*args, **kwargs)
        
        # 3. Action AFTER the function executes
        print("[After] Post-processing...")
        
        return result
    return wrapper
```

Applied cleanly using the `@` symbol:
```python
@my_decorator
def greet(name):
    return f"Hello, {name}!"
```

---

## 🛠️ Practical Implementations & Case Studies

Detailed notes and deep dives generated from lecture content:

1. **[Understanding Decorators & Tollbooth Analogy](notes/2026-09-02/01_understanding_python_decorators_and_tollbooth_analogy.md)**
   - First-class citizens, functions inside functions, returning functions, closures.
2. **[Timing Function Execution (`@timer`)](notes/2026-09-02/02_timing_function_execution_with_decorators.md)**
   - Benchmarking and profiling latency using `time.time()` and `*args, **kwargs`.
3. **[Debugging & Telemetry (`@debug`)](notes/2026-09-02/03_debugging_and_logging_function_calls_decorator.md)**
   - Logging function names, argument signatures, and return values with `repr()`.
4. **[Caching & Memoization (`@cache`)](notes/2026-09-02/04_caching_and_memoization_decorator_in_python.md)**
   - Storing expensive computation results in dictionary closure memory.

---

## 📝 Summary & Key Takeaways
- **First-Class Citizens:** Python functions can be passed as arguments, assigned to variables, and returned from functions.
- **`*args` and `**kwargs`:** Always accept and forward `*args` (positional) and `**kwargs` (keyword) in wrappers to support any function signature.
- **Return Values:** Always return the result of `func(*args, **kwargs)` from the inner wrapper function.
