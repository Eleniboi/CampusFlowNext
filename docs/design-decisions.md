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
