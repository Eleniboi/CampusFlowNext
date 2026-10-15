import unittest
import tempfile
import os
from campusflow.storage import save_tickets, load_tickets
from campusflow.tickets import create_ticket

class TestStorage(unittest.TestCase):
    
    def setUp(self):
        # Create temp directory for test files
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, "test_tickets.json")
    
    def tearDown(self):
        # Clean up temp files
        if os.path.exists(self.filename):
            os.remove(self.filename)
        os.rmdir(self.temp_dir)
    
    def test_save_and_load(self):
        """Save tickets then load them back"""
        tickets = []
        create_ticket(tickets, "Wi-Fi down", "Network", "high", 15, )
        create_ticket(tickets, "Laptop broken", "Hardware", "medium", 3)
        
        save_tickets(tickets, self.filename)
        loaded = load_tickets(self.filename)
        
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]["id"], "T001")
        self.assertEqual(loaded[1]["id"], "T002")
    
    def test_load_missing_file(self):
        """Missing file returns empty list"""
        result = load_tickets(os.path.join(self.temp_dir, "nonexistent.json"))
        self.assertEqual(result, [])
    
    def test_load_malformed_json(self):
        """Malformed JSON raises ValueError"""
        with open(self.filename, "w") as f:
            f.write("{not valid json")
        
        with self.assertRaises(ValueError):
            load_tickets(self.filename)
    
    def test_unique_ids_after_reload(self):
        """IDs remain unique after save and reload"""
        tickets = []
        create_ticket(tickets, "First", "Network", "high", 15)
        create_ticket(tickets, "Second", "Network", "low", 1)
        
        save_tickets(tickets, self.filename)
        loaded = load_tickets(self.filename)
        
        # Create new ticket after reload
        create_ticket(loaded, "Third", "Software", "medium", 5)
        
        ids = [t["id"] for t in loaded]
        self.assertEqual(len(ids), len(set(ids)), "IDs should be unique")
        self.assertEqual(loaded[2]["id"], "T003")

if __name__ == "__main__":
    unittest.main()
