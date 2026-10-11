# AI Learning Log

## Fellow: Zedick

### Interaction #1 — JSON Persistence

**Problem:** I don't understand how to save Python dictionaries to a file

**My initial understanding:** JSON is a text format, but I'm not sure how to convert Python data back and forth

**Prompt to AI:** "Explain json.dump() and json.load() with a 5-line example using a simple shopping list. Then quiz me on what happens if the file doesn't exist."

**Useful AI guidance:** 
- dump() writes Python data to file
- load() reads file back into Python
- Need to handle FileNotFoundError

**My experiment:**
```python
import json

# Test saving
data = {"items": ["apple", "bread"], "total": 5.50}
with open("test.json", "w") as f:
    json.dump(data, f)

# Test loading
with open("test.json", "r") as f:
    loaded = json.load(f)
    
print(loaded["total"])  # I predicted: 5.5 ✓
```
Verification: Ran code, checked test.json content, it worked!
Decision: ACCEPTED — I'll use this pattern for tickets.json
Related file: campusflow/storage.py
What I can now explain: json.dump() takes Python data and a file, converts to text and saves it. json.load() reverses this.
Interaction #2 — bool is subclass of int
Problem: My test for rejecting decimal affected_users was failing
My initial understanding: isinstance(5.5, int) should be False
Prompt to AI: "My test test_reject_decimal_affected_users is failing. Here's my code and traceback. What's wrong?"
Useful AI guidance:

Python's bool is a subclass of int
isinstance(True, int) returns True
Need to check for bool explicitly

My experiment:
print(isinstance(5.5, int))  # False ✓
print(isinstance(True, int))  # True - this is the problem!

Verification: Added or isinstance(affected_users, bool) to validation
Decision: IMPROVED AI suggestion - added bool check to validation
Related file: campusflow/tickets.py
What I can now explain: In Python, bool is a subclass of int, so True == 1 and isinstance(True, int) is True.
Interaction #3 — unittest assertRaises
Problem: I wasn't sure how to test that functions raise errors
My initial understanding: I thought I needed try/except in tests
Prompt to AI: "How do I test that a function raises ValueError in Python unittest?"
Useful AI guidance:

Use assertRaises context manager
Can check error message with str(context.exception)

My experiment:
import unittest

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

class TestDivide(unittest.TestCase):
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError) as context:
            divide(10, 0)
        self.assertIn("Cannot divide", str(context.exception))

# This passed!
Verification: Ran the test, it passed
Decision: ACCEPTED — using assertRaises in all my tests
Related file: tests/test_tickets.py
What I can now explain: assertRaises checks that an exception is raised, and I can inspect the error message.