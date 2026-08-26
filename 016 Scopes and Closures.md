Scope determines where your variables live and who has access to them. Think of Scope like a house. If you create a variable out in the open (Global Scope), everyone can see it. If you create a variable inside a function (Local Scope), it is locked inside that "house."

Understanding this hierarchy, and what happens when a function "packs its bags" to leave the house (Closures), separates junior developers from senior engineers.

The Scope Hierarchy (The House Analogy): 
In Python, whenever you indent code (like inside a ```def``` function or an ```if``` block), you are creating a new Scope.
- Global Scope (The World): Variables defined at the top level of your file without indentation.
- Local Scope (The House): Variables defined inside a specific function.

The Golden Rule of Scope Access:
- You can always look OUT of the house to see the world. (Functions can read Global variables).
- You can never look IN to the house from the world. (The Global scope cannot read variables trapped inside a function).
```
username = "Suraj Kanse" # GLOBAL SCOPE

def my_func():
    balance = 100 # LOCAL SCOPE
    print(username) # Works! The function can look out and see "Suraj Kanse"

print(balance) # CRASH! The global scope cannot look into the function's house.
```

The Climbing Algorithm (LEGB Rule): 
What happens if you have variables with the exact same name? Python follows an strict order of operations to find a variable, often referred to academically as the LEGB Rule (Local, Enclosing, Global, Built-in).

The "Climbing" theory:
- Python first looks inside the current room (Local Function).
- If it doesn't find the variable, it steps out into the hallway (Enclosing/Parent Function).
- If it doesn't find it there, it steps out of the house into the world (Global Scope).
```
x = 99 # Global Scope

def func1():
    x = 88 # Enclosing Scope
    
    def func2():
        print(x) # Where does it get 'x' from?
        
    func2()

func1() 
# Outputs: 88. 
# It checked func2 (empty), climbed up to func1 and found 88. It stopped there and never needed to check Global.
```

The ```global``` Keyword (And Why to Avoid It): 
If a function tries to modify a global variable, Python will normally prevent it by just creating a brand new local variable with the same name instead.

If you absolutely must force a function to overwrite the Global variable, you use the ```global``` keyword.
```
x = 99

def change_x():
    global x # Tells Python: "I am taking control of the global x"
    x = 12

change_x()
print(x) # Outputs: 12
```

Production Warning: Modifying global variables using the ```global``` keyword is considered a terrible practice in production code. If 5 developers are working on a file and one function silently changes a global variable, it creates massive, unpredictable bugs. Read globals, but never overwrite them from inside a function.



Closures & Factory Functions (The "Bag Theory"): 
What happens if a function returns another function instead of returning a value?

The "Bag Theory": When a parent function returns a child function, the child function doesn't just leave empty-handed. It packs a "Backpack" (a Closure) containing all the variables from the parent's house that it might need later.

The Factory Function Example:
```
def chai_coder(num): # Parent Function
    
    def actual(x): # Child Function
        return x ** num # Uses 'num' from the parent
        
    return actual # Returning the DEFINITION of the function, not executing it

# We create two "Factories"
f = chai_coder(2) # f now holds the 'actual' function, and packs 'num=2' in its bag
g = chai_coder(3) # g now holds the 'actual' function, and packs 'num=3' in its bag

# Now we execute them
print(f(3)) # Outputs 9 (Because 3 ** 2)
print(g(3)) # Outputs 27 (Because 3 ** 3)
```

Why this is powerful:
Even though ```chai_coder(2)``` finished running and its "house" was destroyed, the ```f``` function still remembered that ```num``` was ```2``` because it carried that memory reference in its Closure (backpack). This pattern is heavily used in advanced Python frameworks like Django.


Summary & Takeaways
- Scope: The hierarchy of variable visibility. Global is outside, Local is inside a function.
- Access Rules: Inner scopes can read outer scopes, but outer scopes cannot read inner scopes.
- The Climbing Rule: Python searches for variables from the inside out (Local ➔ Parent ➔ Global).
- The ```global``` Keyword: Forces a function to overwrite a global variable. Avoid using this in production code.
- Closures (Bag Theory): When a function returns another function, the returned function remembers and retains access to the variables from its parent's scope, carrying them like a backpack.





