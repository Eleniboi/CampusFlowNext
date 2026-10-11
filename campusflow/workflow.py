def assign_ticket(tickets, ticket_id, staff_name):
    """
    Assign a ticket to a staff member.
    
    Args:
        tickets: list of tickets
        ticket_id: string like "T001"
        staff_name: non-empty string
    
    Returns:
        Updated ticket
    
    Raises:
        ValueError: if ticket not found or staff_name blank
    """
    if not staff_name or not staff_name.strip():
        raise ValueError("Staff name cannot be blank")
    
    ticket = find_ticket(tickets, ticket_id)
    if ticket is None:
        raise ValueError(f"Ticket {ticket_id} not found")
    
    ticket["assigned_to"] = staff_name.strip()
    return ticket


def change_status(tickets, ticket_id, new_status):
    """
    Change ticket status following workflow rules.
    
    Valid transitions:
    - open → in_progress (requires assigned_to)
    - in_progress → resolved
    - resolved → open (reopen)
    
    Args:
        tickets: list of tickets
        ticket_id: string like "T001"
        new_status: "open", "in_progress", or "resolved"
    
    Returns:
        Updated ticket
    
    Raises:
        ValueError: if invalid transition
    """
    ticket = find_ticket(tickets, ticket_id)
    if ticket is None:
        raise ValueError(f"Ticket {ticket_id} not found")
    
    current = ticket["status"]
    new = new_status.lower()
    
    # Define valid transitions
    valid_transitions = {
        "open": ["in_progress", "resolved"],
        "in_progress": ["resolved"],
        "resolved": ["open"]  # reopen
    }
    
    if new not in valid_transitions.get(current, []):
        raise ValueError(
            f"Cannot move ticket from '{current}' to '{new}'"
        )
    
    # Special rule: can't go to in_progress without assignment
    if new == "in_progress" and ticket["assigned_to"] is None:
        raise ValueError("Cannot start work on unassigned ticket")
    
    ticket["status"] = new
    return ticket


def find_ticket(tickets, ticket_id):
    """Helper function to find a ticket by ID."""
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    return None
