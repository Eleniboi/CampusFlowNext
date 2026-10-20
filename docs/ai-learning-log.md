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

### Interaction 2 — bool is subclass of int
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

### Interaction 3 — unittest assertRaises
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

---

# AI Learning Log

## Fellow: James

### Interaction #1 — Exception Handling

**Problem:** I wasn't sure how to handle errors gracefully in Python

**My initial understanding:** I thought errors would crash the program

**Prompt to AI:** "Explain try/except/else/finally with a 5-line example. I want to understand when each block runs."

**Useful AI guidance:** 
- try: code that might fail
- except: runs if error occurs
- else: runs if no error
- finally: always runs

**My experiment:**
```python
try:
    num = int("abc")  # This will fail
except ValueError:
    print("That's not a number!")
else:
    print("Valid number:", num)
finally:
    print("This always runs")

# Output: "That's not a number!" then "This always runs"

Verification: Ran it, got expected output
Decision: ACCEPTED — using try/except in CLI
Related file: main.py
What I can now explain: try/except catches errors so the program doesn't crash.

### Interaction #2 — Git Merge Conflicts
Problem: I was worried about merge conflicts when merging branches
My initial understanding: Merge conflicts mean I broke something
Prompt to AI: "What causes merge conflicts and how do I resolve them?"
Useful AI guidance:

Conflicts happen when both branches change same lines
Look for <<<<<<< ======= >>>>>>> markers
Choose correct version, remove markers

My experiment:
# Created two branches, changed same line in both
# Got conflict markers:
<<<<<<< HEAD
print("Hello from main")
=======
print("Hello from feature")
>>>>>>> feature

# Resolved by keeping: print("Hello from feature")

Verification: Resolved conflict, code worked
Decision: ACCEPTED — not scared of conflicts anymore
Related file: Git workflow
What I can now explain: Conflicts are normal, just read markers and choose correct code.

### Interaction #3 — List Sorting with Keys
Problem: I needed to sort tickets by priority then ID
My initial understanding: I thought sorted() only worked on simple lists
Prompt to AI: "How do I sort a list of dictionaries by two keys in Python?"
Useful AI guidance:

Use key parameter with a function
Return a tuple for multiple sort criteria

My experiment:
tickets = [
    {"id": "T002", "priority": "high"},
    {"id": "T001", "priority": "critical"},
    {"id": "T003", "priority": "high"}
]

priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}

def sort_key(t):
    return (priority_order[t["priority"]], int(t["id"][1:]))

sorted_tickets = sorted(tickets, key=sort_key)
# Result: T001 (critical), T002 (high), T003 (high)

Verification: Ran it, got correct order
Decision: ACCEPTED — using this for work queue
Related file: campusflow/reports.py
What I can now explain: sorted() with key function can sort by multiple criteria using tuples.







# CampusFlow Next — AI Learning Log (Engineer A)

**Engineer:** Engineer A (Omafu Samuel Oloche)
**Branch:** `feat/21-validation-and-notes`
**Scope:** Validation, ticket creation and IDs, workflow safety, follow-up notes, and JSON persistence.

> **Evidence rule:** Keep this log honest. Record the result you actually observed for each experiment and update the verification lines before submission. Do not claim a test passed unless you ran it.

## Learning Cycle 1 — Required ticket fields and a failing storage test

### Knowledge gap
I understood that `create_ticket()` builds a ticket and `save_tickets()` writes the collection to JSON, but I did not immediately connect the storage validation error to the exact structure returned by the ticket-creation function.

### Exact question asked
> “I need a test file for note.py.”

During debugging, I also shared the failing storage-test output: `ValueError: Ticket is missing required fields: notes`.

### Guidance received
Compare the schema expected by `validate_ticket_collection()` with the dictionary created by `create_ticket()`. My ticket used `"note": []`, while validation required `"notes": []`.

### Small unrelated experiment
Predict the output before running this example. It demonstrates that dictionary keys must match exactly.

```python
record = {"note": []}
print("notes" in record)
record["notes"] = []
print("notes" in record)
```

**Prediction:** __________________________________________  
**Observed output:** ______________________________________

### Independent verification
I inspected the ticket dictionary and exception traceback. The traceback pointed to `validate_ticket_collection()`, and the ticket used the singular key `"note"`. The required schema uses the plural key `"notes"`.

**Complete before submission:** Change the key to `"notes"` in `campusflow/tickets.py`, then run:

```bash
python3 -m unittest tests.test_storage -v
```

**Actual result:** __________________________________________

### Final decision
Use `"notes"` as the canonical field name throughout the application and tests. Fix the ticket producer to match the agreed schema rather than weakening validation to accept a typo.

### What I learned
A test failure is evidence about a specific contract. Reading the traceback and comparing the producer's output with the validator's expected schema is more reliable than removing a validation rule just to make a test pass.

---

## Learning Cycle 2 — Preserving state when an operation is rejected

### Knowledge gap
I needed to understand how to guarantee that a failed operation does not partially modify a ticket or consume a note ID.

### Exact question asked
> “How does your code avoid modifying state on a rejected action?”

### Guidance received
Validate the ticket ID, ticket status, author, and trimmed message before appending a note or advancing the note-ID sequence. Apply the same principle to ticket creation, assignment, and status changes: check the rules first, then mutate state only after validation succeeds.

### Small unrelated experiment
Predict the output before running this unrelated example about validating a value before modifying a list.

```python
items = ["pen", "book"]
candidate = ""

if candidate.strip():
    items.append(candidate.strip())

print(items)
```

**Prediction:** __________________________________________  
**Observed output:** ______________________________________

### Independent verification
Use a unit test that attempts to add a note with a blank author or invalid message, expects `ValueError`, and then checks that the ticket's notes remain unchanged.

```bash
python3 -m unittest tests.test_notes -v
```

**Actual test result and test name:** __________________________________________

### Final decision
Keep validation before mutation. A rejected operation should leave the ticket collection unchanged, and a rejected note should not consume a note ID. Tests should verify both the exception and the unchanged state.

### What I learned
Checking only that an exception is raised is not enough. A test should also inspect the state after failure, because code might raise an error after it has already changed data.

---

## Learning Cycle 3 — Evaluating an AI suggestion against the project contract

### Knowledge gap
I needed to distinguish a quick workaround from a fix that preserves the project's agreed data contract.

### Exact question asked
> “Why does `test_save_and_load` fail with `Ticket is missing required fields: notes`, and what should I change?”

### AI suggestion considered
A possible shortcut would be to relax validation so that tickets with `"note"` are accepted. That might hide the immediate error, but it would leave the application with two field names for the same concept.

### Small unrelated experiment
Predict the output before running this unrelated example.

```python
data = {"colour": "blue"}
print(data.get("color"))
print(data.get("colour"))
```

**Prediction:** __________________________________________  
**Observed output:** ______________________________________

### Independent verification
I compared the project ticket schema with the validation error and ticket dictionary. The schema requires `notes`, while the implementation used `note`. This supports correcting the dictionary key, not weakening the validator.

**Complete before submission:** Confirm the correction with the storage tests and full suite. Record the real output:

```bash
python3 -m unittest discover -s tests -v
```

**Actual result:** __________________________________________

### Final decision
Reject the workaround of accepting inconsistent field names. Use `"notes"` consistently, retain schema validation, and use test results to confirm the correction.

### What I learned
AI output is a suggestion, not proof. I should compare it with the written requirements, inspect the actual code and traceback, run a small experiment, and test the proposed fix before accepting it.

---

## Engineer A — completion checklist

- [ ] Fill in predictions before running each unrelated experiment.
- [ ] Record the actual experiment outputs.
- [ ] Run relevant tests and record the real results.
- [ ] Add any additional coding/debugging cycle required by the mentor.
- [ ] Be prepared to explain each decision in your own words.



## Fellow: Jimmy (Engineer B)
## Branch: `feat/2-search-and-insights`


### Interaction #1: Quiz mistakes and assertRaises

* **Concept gap:** I answered Q3 with "all open records" and thought a filter could match any one condition. Filters combine with AND, so a record has to match every filter supplied. I also answered Q4 with "append anyway" and Q5 with "rename IDs silently." A resolved ticket must reject notes, and duplicate IDs must reject the whole load.
* **Question asked:** I asked the AI to explain the correct answers after I got three wrong.
* **AI guidance summary:** The correct answer depends on the rule being tested. Filters use AND, and a rejected action should leave the data unchanged.
* **Independent check:**
  * I ran `search_filtered` with text "wifi", category "Network", and status "open" on three tickets. It returned only `T001`, which matches the AND rule.
  * I ran `add_note` on a resolved ticket. It was rejected with "Notes can only be added to open or in-progress tickets", and the notes list stayed at 0.
  * Duplicate-ID load: [paste the Test 3 result here before committing]
* **Decision:** I accepted the correct answers, and I'll keep the AND filter rule and the reject-on-duplicate rule in my code and tests.
* **Changed in my code:** None in this step. I checked the behaviour with tests.
* **What I can explain without AI:** Filters combine with AND, so a ticket must match every filter. A resolved ticket can't take notes until it's reopened.

### Interaction #2: Restoring a function after a whole-file replace

* **Concept gap:** I didn't know that replacing a whole file can delete functions that weren't part of the change.
* **Question asked:** I asked how to restore one function without changing the rest of the file.
* **AI guidance summary:** Make targeted edits, and use `git show <commit>:<file>` to get the exact original text.
* **Independent check:** I ran the tests and got 38 passing. I used `git diff -w` to confirm that only `get_report` had changed. Comparing with the original text showed that the only remaining differences in `get_work_queue` are whitespace on blank lines.
* **Decision:** I restored `get_work_queue` with a targeted edit and kept the new `get_report`.
* **Changed in my code:** `campusflow/reports.py`, `get_work_queue`, restored to its original logic and comments.
* **What I can explain without AI:** Before saving a rewritten file, check the diff, so unrelated functions aren't lost.

### Interaction #3: Branch and stash confusion

* **Concept gap:** I didn't understand which branch a commit goes to, or what a stash holds.
* **Question asked:** I asked how to move uncommitted changes to another branch safely.
* **AI guidance summary:** Check the branch with `git branch --show-current`, use `git stash` to move uncommitted changes, then switch and pop.
* **Independent check:** I ran `git status`, `git log`, and `git stash list` to confirm where my changes were. This check showed that I was on `main`, not my feature branch, which I hadn't noticed.
* **Decision:** I'll check the branch and status before every commit and push.
* **Changed in my code:** None. This was a process change only.
* **What I can explain without AI:** Commits go to the branch you're on, so confirm it first.