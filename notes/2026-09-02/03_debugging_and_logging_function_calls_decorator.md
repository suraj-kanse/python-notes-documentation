# Debugging & Logging Function Calls Decorator

> **Source:** [YouTube Lecture](https://youtu.be/ZEKiIwWv9nM?si=uEq-ADaTkXLOYnpM)  
> **Date:** 2026-09-02  
> **Topic:** Practical Problem 2 - Inspecting Arguments, Function Names, and Return Values

---

## 🎯 Problem Statement
During development and debugging, you often want to trace:
1. Which function was called?
2. What positional arguments were passed (`args`)?
3. What keyword arguments were passed (`kwargs`)?
4. What was the exact returned value?

Instead of littering print statements throughout your functions, a `@debug` decorator provides automatic, uniform telemetry across your entire codebase.

---

## 💻 Implementation: The `@debug` Decorator

```python
def debug(func):
    """Decorator to print function name, inputs, and output upon each call."""
    def wrapper(*args, **kwargs):
        # Format positional arguments
        args_repr = [repr(a) for a in args]
        
        # Format keyword arguments
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        
        # Combine arguments for clean display
        signature = ", ".join(args_repr + kwargs_repr)
        
        print(f"--> Calling {func.__name__}({signature})")
        
        # Execute the function
        result = func(*args, **kwargs)
        
        print(f"<-- {func.__name__} returned {result!r}")
        
        return result
    return wrapper
```

---

## 🧪 Testing the Decorator

```python
@debug
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

@debug
def calculate_area(width, height, unit="sq meters"):
    area = width * height
    return f"{area} {unit}"

# Test calls
msg = greet("Suraj", greeting="Namaste")
print(f"Final Message: {msg}\n")

area = calculate_area(10, 25, unit="sq feet")
print(f"Final Area: {area}")
```

### 🖥️ Expected Output:
```text
--> Calling greet('Suraj', greeting='Namaste')
<-- greet returned 'Namaste, Suraj!'
Final Message: Namaste, Suraj!

--> Calling calculate_area(10, 25, unit='sq feet')
<-- calculate_area returned '250 sq feet'
Final Area: 250 sq feet
```

---

## 🧠 Deep Dive: `repr()` vs `str()`
- `str()` gives human-readable text (e.g. `Suraj`).
- `repr()` gives unambiguous string representation showing data types (e.g. `'Suraj'`, strings quoted, numbers unquoted).
- Using `!r` in f-strings (`f"{v!r}"`) is equivalent to calling `repr(v)`.

---

## 📝 Summary & Key Takeaways
- Decorators excel at logging and telemetry without polluting core logic.
- Joining formatted `args` and `kwargs` provides an exact snapshot of how a function was invoked.
- Capturing and logging `result` before returning completes the full execution trace.
