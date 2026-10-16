# Design Decisions

## Data Structure
- Tickets stored as: list of dictionaries
- Each ticket: {id, title, category, urgency, affected_users, priority, status, assigned_to}

## Function Contracts

### tickets.py
- `calculate_priority(urgency, affected_users)` → returns "critical"/"high"/"medium"/"low"
- `create_ticket(tickets, title, category, urgency, affected_users)` → returns ticket dict
- Raises ValueError for invalid inputs

### workflow.py
- `assign_ticket(tickets, ticket_id, staff_name)` → returns updated ticket
- `change_status(tickets, ticket_id, new_status)` → returns updated ticket
- Raises ValueError for invalid operations

### storage.py
- `save_tickets(tickets, filename="data/tickets.json")` → None
- `load_tickets(filename="data/tickets.json")` → list of tickets

### reports.py
- `get_work_queue(tickets)` → sorted list of open tickets
- `get_report(tickets)` → dict with counts and breakdowns

## Error Handling
- Use ValueError with clear messages
- CLI catches and displays errors

## Ownership
- James: tickets.py + test_tickets.py
- Zed: workflow.py, reports.py + test_workflow.py
- Both: storage.py + test_storage.py




# CampusFlow Next — Design Decisions (Engineer A)

**Owner:** Engineer A (Omafu Samuel Oloche)
**Branch:** `feat/21-validation-and-notes`  
**Responsibility:** Validation, ticket creation and ID continuity, workflow safety, follow-up notes, and JSON persistence.

This document records decisions for Engineer A's part of CampusFlow Next. Update it if the team agrees to a different implementation. Describe a decision as completed only after confirming it in the code.

## 1. Shared ticket representation

A ticket is represented as a Python dictionary. The ticket collection is a list of ticket dictionaries passed to functions that create, update, or persist tickets.

The ticket schema retains the original fields:

- `id`
- `title`
- `category`
- `urgency`
- `affected_users`
- `priority`
- `status`
- `assigned_to`

It adds `notes`, initially an empty list. Each note is a dictionary containing `note_id`, `author`, and `message`.

**Decision:** Use the exact field name `notes` everywhere. Do not mix `note` and `notes`.

**Reason:** Consistent keys let validation, workflow functions, tests, and JSON persistence share one data contract.

## 2. Centralized validation

**Decision:** Keep reusable validation in `campusflow/validation.py` and use it from ticket, workflow, note, and storage operations where appropriate.

Validation rules include:

- Title must not be blank after trimming.
- Category must be `Network`, `Hardware`, `Software`, or `Other` (input may be normalized to these canonical values).
- Urgency must be `low`, `medium`, or `high`.
- `affected_users` must be a strictly positive integer; reject booleans, floats, and strings.
- Ticket IDs must be valid and unique.
- Assignment labels must not be blank.
- Note authors must not be blank.
- Note messages must contain 5–300 characters after trimming.

**Reason:** Centralized rules reduce inconsistent behavior and make validation easier to test. Rejecting booleans explicitly matters because Python treats `bool` as a subclass of `int`.

## 3. Validate before mutating state

**Decision:** Check all relevant input and business rules before modifying the ticket collection, ticket fields, note list, or ID sequence.

Examples:

- Invalid ticket creation must not append a partial ticket.
- An invalid assignment must not change `assigned_to`.
- An invalid status transition must leave the status unchanged.
- A rejected note must not be appended and must not consume a note ID.
- Invalid or duplicate-ID JSON must not replace a valid in-memory collection.

**Reason:** A rejected operation should leave application state unchanged. Tests should assert both the expected exception or error and the unchanged state.

## 4. Priority calculation

**Decision:** Preserve the agreed four-rule priority cascade, evaluated in order:

1. High urgency **and** at least 10 affected users → `critical`.
2. High urgency **or** at least 10 affected users → `high`.
3. Medium urgency **or** at least 3 affected users → `medium`.
4. Otherwise → `low`.

**Reason:** The rules overlap, so order matters. The most severe matching rule must be checked first. Boundary tests should cover 2/3 users and 9/10 users, as well as high and medium urgency.

## 5. Ticket and note ID continuity

**Decision:** Generate IDs that remain unique when tickets or notes are created after data has been loaded. Do not rely only on `len(collection) + 1`, because deleted records or gaps can cause collisions.

For tickets, determine the next number from existing numeric ID suffixes (for example, `T001`, `T002`, then `T003`). For notes, use per-ticket IDs such as `N001`, `N002`; identify a note by its ticket ID together with its note ID.

**Reason:** A reload must not cause an existing identifier to be reused. Test normal sequences, gaps, and `T999` to `T1000` if supported by the implementation.

## 6. Workflow and note-state safety

**Decision:** Keep the agreed ticket lifecycle rules:

- A ticket begins in `open`.
- An unassigned ticket cannot move to `in_progress`.
- Valid work proceeds from `open` to `in_progress` to `resolved`.
- A resolved ticket can be reopened through the supported workflow.
- Resolved tickets cannot be reassigned or receive new notes until reopened.
- Existing notes remain attached when a ticket is resolved and reopened.
- Notes may be added only while a ticket is `open` or `in_progress`.

**Reason:** A status change should not bypass assignment or note restrictions. Workflow rules should be enforced in the business-logic layer, not only by hiding CLI options.

## 7. JSON persistence and safe loading

**Decision:** Use JSON for persistence and keep file operations in `campusflow/storage.py`.

On load:

- A missing data file may return an empty collection.
- Malformed JSON should raise a clear `ValueError`.
- Validate the full loaded collection, including required fields and duplicate IDs, before accepting it.
- Preserve notes and identifier continuity across save/reload.
- If legacy tickets predate `notes`, migrate those records by adding `notes: []` before validating the migrated collection, if this migration is part of the agreed implementation.

On save:

- Validate the collection before writing.
- Do not silently save an invalid collection.
- Avoid replacing valid saved data with an invalid or partially validated collection.

**Reason:** Persistence is part of application correctness. Corrupt or inconsistent data should be rejected safely rather than silently accepted or used to overwrite valid state.

**Implementation note:** If atomic file replacement is used, write validated data to a temporary file and replace the destination only after the write succeeds. Keep temporary files out of version control.

## 8. Exceptions and CLI boundary

**Decision:** Business-logic functions should raise `ValueError` for invalid input or rejected operations. The CLI (`main.py`, owned by Engineer B) should catch expected errors and show a useful message rather than exposing a traceback to the user.

**Reason:** This keeps core logic testable without interactive input and separates business rules from user-interface behavior.

## 9. Testing strategy

Engineer A's primary test ownership:

- `tests/test_tickets.py`
- `tests/test_workflow.py`
- `tests/test_storage.py`
- `tests/test_notes.py` (if included in the team's test layout)
- Coordinated validation, note-state, legacy-data, and ID-continuity cases in shared tests.

Tests should include:

- Valid and invalid ticket creation.
- Boundary cases for priority.
- Rejected workflow transitions.
- Blank authors and invalid note lengths.
- Attempts to add notes to resolved or unknown tickets.
- Rejected operations preserving state and not consuming IDs.
- Missing and malformed JSON.
- Duplicate IDs and invalid records.
- Save/reload preserving notes and ID continuity.

**Reason:** Positive-path tests show that features work; negative-path tests show that unsafe changes are rejected without corrupting state.

## 10. Ownership and integration

Engineer A owns:

- `campusflow/validation.py`
- `campusflow/tickets.py`
- `campusflow/workflow.py`
- `campusflow/notes.py`
- `campusflow/storage.py`

Engineer A primarily maintains the corresponding tests. Changes to shared files or function contracts should be agreed with Engineer B before integration. Both engineers should run the full test suite after merging.

**Integration rule:** Keep one shared application and one agreed ticket/note schema. Do not create duplicate modules or silently change public function signatures.

## 11. Decisions to confirm during review

- [ ] Confirm the public `add_note` function signature with Engineer B and the CLI. The project contract names `add_note(ticket_id, author, message)` at the user-facing interface; the implementation must also have an agreed way to access the ticket collection.
- [ ] Confirm exact ticket-ID and note-ID behavior after reload.
- [ ] Confirm how legacy records missing `notes` are migrated and tested.
- [ ] Confirm that the JSON write path prevents invalid data from replacing valid saved data.
- [ ] Update this document to reflect the final merged implementation rather than describing an unimplemented decision as completed.