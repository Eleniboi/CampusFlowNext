# CampusFlow Next

**A Python-Based Campus Technical Helpdesk System**

CampusFlow Next is a command-line helpdesk application designed to help a campus technical support team manage issues reported by fellows. The system supports ticket creation, input validation, priority classification, staff assignment, status tracking, follow-up notes, ticket searching, reporting, and JSON-based data persistence.

The project was developed collaboratively by two engineers using separate Git feature branches, shared testing, and code review.

## Table of Contents

- [Project Overview](#project-overview)
- [Project Objectives](#project-objectives)
- [Team Contributions](#team-contributions)
- [Features](#features)
- [Priority Classification](#priority-classification)
- [Ticket Workflow](#ticket-workflow)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Data Storage](#data-storage)
- [Design Decisions](#design-decisions)
- [Git Collaboration Workflow](#git-collaboration-workflow)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)

## Project Overview

CampusFlow Next provides a structured way to record, organize, and monitor campus technical issues.

When a fellow reports an issue, the system creates a ticket containing relevant information, calculates its priority, and allows the support team to assign a staff member and track progress until the issue is resolved.

The application also supports searching for tickets, generating reports, and adding follow-up notes so that important updates remain attached to the relevant ticket.

The project emphasizes clean Python code, separation of responsibilities, input validation, automated testing, reliable data storage, and collaborative software development.

## Project Objectives

The main objectives are to:

1. Create and manage helpdesk tickets.
2. Validate user input and ticket data.
3. Automatically classify tickets by priority.
4. Manage ticket assignments and status transitions.
5. Record follow-up notes for ongoing issues.
6. Search and filter tickets using supported criteria.
7. Generate useful ticket reports.
8. Save and reload ticket data using JSON.
9. Test important functionality and edge cases with Python's `unittest` framework.
10. Practice Git branching, pull requests, code reviews, and collaborative development.

## Team Contributions

The project was divided between two engineers to encourage modular development and clear ownership.

### Engineer A — Omafu Samuel

**Feature branch:** `feat/21-validation-and-notes`

Engineer A was responsible for the ticket validation, core ticket operations, workflow management, follow-up notes, and storage functionality.

Responsibilities:

- **Input validation:** Validate ticket fields and reject invalid data.
- **Ticket management:** Create tickets with the required fields and consistent structure.
- **Priority classification:** Calculate ticket priority using urgency and the number of affected users.
- **Workflow management:** Handle valid status transitions, assignment requirements, and reopening resolved tickets.
- **Follow-up notes:** Add structured notes containing an author, message, and unique note identifier.
- **Storage:** Save ticket data to JSON and load it back into the application.
- **Error handling:** Handle missing storage files and invalid or malformed stored data appropriately.
- **Testing:** Develop tests for ticket creation, validation, workflow transitions, notes, and storage.
- **Documentation:** Record AI-assisted learning activities and document important design decisions.

### Engineer B — Akpera James

**Feature branch:** `feat/22-search-and-insights`

Engineer B was responsible for ticket discovery, reporting, understanding checks, and command-line integration.

Responsibilities:

- **Ticket search:** Find tickets using supported search criteria.
- **Combined filtering:** Narrow results using multiple supported filters together.
- **Reports:** Summarize ticket information to help the support team understand the current workload and ticket status.
- **Understanding checks:** Support the project's required checks for understanding the system and its functionality.
- **CLI integration:** Connect the application features through `main.py` and provide the command-line interaction.
- **Testing:** Develop tests for search, filtering, reports, and command-line-related functionality.
- **Integration:** Ensure the features work with the ticket data and functions provided by Engineer A.

### Collaboration

Both engineers contribute to the same project while working on separate feature branches. Changes are reviewed and integrated through pull requests rather than being developed directly on the main branch.

The final application should combine both engineers' contributions into one working system.

## Features

The intended application functionality includes the following.

| Feature | Description |
|---|---|
| Ticket creation | Record a fellow's reported issue. |
| Input validation | Check ticket data before accepting or processing it. |
| Automatic priority | Classify tickets as critical, high, medium, or low. |
| Ticket listing and viewing | Display available tickets and their details through the CLI. |
| Staff assignment | Assign an available support staff member to a ticket. |
| Status management | Track issues from open to in progress and resolved. |
| Follow-up notes | Record updates and additional information on tickets. |
| Ticket searching | Find relevant tickets using supported criteria. |
| Combined filters | Narrow ticket results using multiple criteria. |
| Reports | Summarize ticket information for operational understanding. |
| JSON persistence | Save ticket data and restore it when the application runs again. |
| Automated tests | Verify expected behavior and important error cases. |

## Priority Classification

CampusFlow Next calculates ticket priority using the issue's urgency and the number of affected users.

The priority rules are applied in the following order:

| Condition | Priority |
|---|---|
| High urgency and at least 10 affected users | Critical |
| High urgency or at least 10 affected users, when the critical condition is not met | High |
| Medium urgency or at least 3 affected users, when higher-priority conditions are not met | Medium |
| None of the above conditions | Low |

The order matters. For example, a high-urgency issue affecting 12 users is **critical**, not merely high.

This approach helps the support team identify issues that may require immediate attention.

## Ticket Workflow

Tickets follow a controlled lifecycle.

1. **Open:** A fellow reports an issue and a ticket is created.
2. **Assigned:** A staff member is assigned to handle the issue.
3. **In progress:** Work begins on the ticket.
4. **Resolved:** The issue has been addressed.
5. **Reopened:** A resolved ticket can return to the open state if further work is required.

The workflow rules require an assignment before a ticket can move from `open` to `in_progress`. Resolved tickets must be reopened before they can receive new follow-up notes or be reassigned, according to the project's workflow requirements.

The valid status values are:

- `open`
- `in_progress`
- `resolved`

The application should reject invalid status values and disallowed transitions rather than silently accepting them.

## Technology Stack

- **Programming language:** Python 3
- **Data storage:** JSON
- **Testing framework:** Python `unittest`
- **Version control:** Git
- **Collaboration and code review:** GitHub
- **Interface:** Command-line interface (CLI)

No third-party Python packages should be necessary if the implementation uses only the standard library. If the final implementation introduces external dependencies, document them and install them as part of setup.

## Project Structure

The following structure describes the intended organization. Confirm the exact filenames against the final repository before submission.

```text
CampusFlowNext/
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py
│   ├── validation.py
│   ├── workflow.py
│   ├── notes.py
│   ├── storage.py
│   ├── search.py
│   ├── reports.py
│   └── understanding_check.py
├── tests/
│   ├── test_tickets.py
│   ├── test_workflow.py
│   ├── test_storage.py
│   ├── test_notes.py
│   ├── test_search.py
│   └── test_reports.py
├── docs/
│   ├── ai-learning-log.md
│   └── design-decisions.md
├── main.py
├── README.md
└── .gitignore
```

The actual repository may contain additional files or use slightly different test filenames.

### Main modules

- `tickets.py` — Core ticket creation and ticket-related operations.
- `validation.py` — Validation of ticket fields and ticket collections.
- `workflow.py` — Ticket assignment and status transitions.
- `notes.py` — Creation and management of ticket follow-up notes.
- `storage.py` — JSON persistence and loading.
- `search.py` — Ticket searching and filtering.
- `reports.py` — Ticket reports and summaries.
- `understanding_check.py` — The project's understanding-check functionality.
- `main.py` — Command-line entry point and integration of the application features.

## Getting Started

### Prerequisites

Install Python 3 and Git.

Verify Python is available:

```bash
python3 --version
```

Verify Git is available:

```bash
git --version
```

### 1. Clone the repository

Replace the placeholder with the actual GitHub repository URL.

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd CampusFlowNext
```

### 2. Create and activate a virtual environment

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows Command Prompt:

```bat
python -m venv .venv
.venv\Scripts\activate
```

A virtual environment is recommended to keep project dependencies isolated. If the project uses only Python's standard library, installing third-party packages should not be necessary.

### 3. Verify the project files

Check that the application entry point and package are present:

```bash
ls
```

You should see `main.py`, `campusflow/`, and `tests/` in the project root, along with the other repository files.

## Running the Application

From the project root, run:

```bash
python3 main.py
```

On Windows, use:

```bash
python main.py
```

Follow the prompts provided by the command-line interface.

The available menu options and exact interaction steps depend on the final implementation in `main.py`.

If the application does not start, check that you are in the project root, that Python 3 is installed, and that all required modules are present.

## Running Tests

CampusFlow Next uses Python's built-in `unittest` framework to test the application's behavior.

Run the complete test suite from the project root:

```bash
python3 -m unittest discover -s tests -v
```

On Windows:

```bash
python -m unittest discover -s tests -v
```

The `-v` option displays the name and result of each test.

### Run an individual test file

For example:

```bash
python3 -m unittest discover -s tests -p "test_tickets.py" -v
```

Replace `test_tickets.py` with the filename of the test module you want to run.

### What should be tested?

The test suite should cover:

- Valid and invalid ticket creation.
- Missing fields and incorrect data types.
- Priority classification, including boundary conditions.
- Valid and invalid workflow transitions.
- Assignment requirements.
- Adding notes and rejecting invalid note messages.
- Restrictions on resolved tickets.
- Saving and reloading ticket data.
- Missing JSON files and malformed JSON.
- Duplicate ticket identifiers.
- Searching and combining filters.
- Reports and empty-result scenarios.

The project requirement calls for at least eight automated `unittest` tests. More tests should be added where they provide meaningful coverage of the requirements and edge cases.

**Testing status:** Run the test command on the final merged branch and record the actual result before submitting. Do not report a passing test count unless it has been verified.

## Data Storage

Ticket data is persisted using JSON so that records can be restored after the application exits.

The storage implementation should support:

- Saving a collection of tickets.
- Loading saved ticket records.
- Returning an empty collection when the storage file does not exist.
- Detecting malformed JSON and reporting the error appropriately.
- Validating loaded ticket records before using them.
- Detecting duplicate ticket identifiers.
- Preserving ticket notes and other required fields across save-and-load operations.

The exact JSON filename and storage location depend on the implementation.

JSON provides a simple, human-readable storage format suitable for this project's scope. It is not a replacement for a production database when concurrent users, advanced queries, access controls, or stronger transactional guarantees are required.

## Design Decisions

The project uses a modular structure to separate different responsibilities.

### Separation of concerns

Validation, ticket operations, workflow management, notes, storage, searching, and reporting are organized into separate modules. This makes the code easier to test, understand, and maintain.

### Centralized validation

Ticket data should be checked at appropriate system boundaries, including when data is created and when saved records are loaded. This reduces the risk of invalid records entering the application.

### Explicit workflow rules

Status changes and assignments should follow defined business rules. Invalid transitions should be rejected rather than silently changing ticket state.

### Structured notes

Follow-up notes should be represented as structured records containing a note identifier, author, and message. This makes notes easier to validate and preserve.

### JSON persistence

JSON is used because it is simple to inspect and suitable for a small CLI project. A database could be introduced later if the system's requirements expand.

### Automated testing

Automated tests help verify expected behavior, detect regressions, and confirm that separate modules work as intended.

For additional design details and learning reflections, consult:

- `docs/design-decisions.md`
- `docs/ai-learning-log.md`

These documents should reflect the actual decisions, experiments, and implementation results from the project.

## Git Collaboration Workflow

The team uses separate feature branches for the two engineers.

| Engineer | Name | Feature branch |
|---|---|---|
| Engineer A | Omafu Samuel | `feat/21-validation-and-notes` |
| Engineer B | Akpera James | `feat/22-search-and-insights` |

### General workflow

1. Pull the latest changes from the shared repository.
2. Work on the feature branch assigned to you.
3. Write and run tests for your changes.
4. Commit changes with descriptive commit messages.
5. Push the feature branch to GitHub.
6. Open a pull request against the agreed target branch.
7. Have the other engineer review the changes.
8. Address review feedback and verify tests.
9. Merge the approved pull request.
10. Run the full test suite against the integrated code.

### Example commands for Engineer A

```bash
git switch feat/21-validation-and-notes
git status
```

After making and testing changes:

```bash
git add .
git commit -m "Implement validation, workflow, notes, and storage"
git push -u origin feat/21-validation-and-notes
```

### Example commands for Engineer B

```bash
git switch feat/22-search-and-insights
git status
```

After making and testing changes:

```bash
git add .
git commit -m "Implement ticket search, filters, and reports"
git push -u origin feat/22-search-and-insights
```

Only stage and commit the files intended for your change. Review `git status` before committing, especially when both engineers have made changes to the same working directory.

The team should use pull requests and code reviews to integrate work safely and resolve conflicts.

## Known Limitations

The following limitations are relevant to the project's current scope and should be confirmed against the actual implementation:

- The application is designed as a command-line tool rather than a web or mobile application.
- JSON storage does not provide the full concurrency and transaction guarantees of a database.
- The application may not include user authentication, role-based access control, or audit logging.
- Reporting and searching are limited to the fields and filters implemented in the code.
- Production deployment, automated continuous integration, and large-scale performance testing may be outside the current project scope.

These are scope limitations, not necessarily defects in an educational CLI application.

## Future Improvements

Potential future enhancements include:

- A web interface using a Python web framework.
- Database-backed storage.
- User authentication and staff roles.
- Ticket deadlines and service-level agreement tracking.
- Email or notification alerts for critical tickets.
- More detailed operational dashboards and reports.
- Continuous integration to run tests automatically on pull requests.
- Expanded audit logs and activity history.
- Additional tests for integration, performance, and unusual input conditions.

## Conclusion

CampusFlow Next demonstrates how a campus technical helpdesk can be organized into a modular Python application. Its core design combines ticket validation, priority classification, workflow management, follow-up notes, searching, reporting, and persistent storage.

The collaboration between Engineer A, Omafu Samuel, and Engineer B, Akpera James, also demonstrates practical software development skills, including division of responsibilities, automated testing, Git branching, pull requests, code reviews, and technical documentation.

The final submission should include the integrated code, passing automated tests, accurate documentation, and evidence of each engineer's contribution.

---

**Project:** CampusFlow Next  
**Language:** Python 3  
**Interface:** Command-line application  
**Storage:** JSON  
**Testing:** Python `unittest`  
**Engineer A:** Omafu Samuel — `feat/21-validation-and-notes`  
**Engineer B:** Akpera James — `feat/22-search-and-insights`
