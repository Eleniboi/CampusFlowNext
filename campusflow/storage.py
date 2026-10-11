import json
import os

def save_tickets(tickets, filename="data/tickets.json"):
    """
    Save tickets to JSON file.
    
    Args:
        tickets: list of ticket dictionaries
        filename: path to save file
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, "w") as f:
        json.dump(tickets, f, indent=2).


def load_tickets(filename="data/tickets.json"):
    """
    Load tickets from JSON file.
    
    Args:
        filename: path to load file
    
    Returns:
        List of tickets
    
    Raises:
        ValueError: if file is malformed JSON
    """
    if not os.path.exists(filename):
        return []
    
    try:
        with open(filename, "r") as f:
            tickets = json.load(f)
        
        # Validate it's a list
        if not isinstance(tickets, list):
            raise ValueError("Ticket file must contain a list")
        
        return tickets
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Malformed JSON in {filename}: {e}")
