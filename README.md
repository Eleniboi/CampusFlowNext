# CampusFlow

A command-line helpdesk ticket manager for Learn2Earn campus staff.

## Team Members
- Zedick - Ticket creation, validation, priority engine
- James - Assignment, workflow, queue, reports

## Setup
1. Clone the repo https://github.com/Otiozee/campusflow.git
2. Run `python main.py`

## Running the CLI

Menu options:
1. Create ticket - Add a new support ticket
2. List all tickets - Show all tickets
3. View ticket details - Show one ticket's full info
4. Assign ticket - Assign to staff member
5. Change status - Move through workflow
6. Show work queue - Open tickets by priority
7. Show reports - Statistics
8. Exit

## Testing
```bash
python -m unittest discover -s tests -v
```

### Priority Rules

high urgency AND >= 10 users → critical
high urgency OR >= 10 users → high
medium urgency OR >= 3 users → medium
everything else → low

### Status Workflow

open → in_progress (requires assignment) → resolved
resolved → open (reopen)

### Data Storage

Tickets saved to data/tickets.json
Delete this file to start fresh

### Known Limitations

- No GUI (command-line only)
- No authentication
- Single-user at a time

### Pull Requests

PR #1: Ticket creation
PR #2: Workflow and reports

