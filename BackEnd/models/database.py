from tinydb import TinyDB, Query
from datetime import datetime
from typing import Optional, List, Dict
import os

# Ensure the data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Initialize database
db = TinyDB('data/db.json')

# Initialize tables
clients = db.table('clients')
triggers = db.table('triggers')
mood_history = db.table('mood_history')
trigger_history = db.table('trigger_history')

class ClientModel:
    @staticmethod
    def create(first_name: str, last_name: str, email: str, phone_number: str) -> int:
        # Check for unique constraints
        User = Query()
        if clients.search(User.email == email) or clients.search(User.phone_number == phone_number):
            raise ValueError("Email or phone number already exists")
        
        # Get next client_id
        existing_ids = [doc.get('client_id', 0) for doc in clients.all()]
        next_id = max(existing_ids, default=0) + 1
        
        client_data = {
            'client_id': next_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': phone_number
        }
        clients.insert(client_data)
        return next_id

class TriggerModel:
    @staticmethod
    def create(name: str, description: Optional[str] = None, feelings: Optional[List[str]] = None) -> int:
        # Check for unique name
        Trigger = Query()
        if triggers.search(Trigger.name == name):
            raise ValueError("Trigger name already exists")
        
        # Get next trigger_id
        existing_ids = [doc.get('trigger_id', 0) for doc in triggers.all()]
        next_id = max(existing_ids, default=0) + 1
        
        trigger_data = {
            'trigger_id': next_id,
            'name': name,
            'description': description,
            'feelings': feelings or [],  # Array of feelings
        }
        triggers.insert(trigger_data)
        return next_id

class MoodHistoryModel:
    @staticmethod
    def create(client_id: int, mood: int, entry_date: Optional[datetime] = None) -> int:
        if entry_date is None:
            entry_date = datetime.now()
            
        # Get next id
        existing_ids = [doc.get('id', 0) for doc in mood_history.all()]
        next_id = max(existing_ids, default=0) + 1
        
        mood_data = {
            'id': next_id,
            'client_id': client_id,
            'mood': mood,
            'entry_date': entry_date.isoformat()
        }
        mood_history.insert(mood_data)
        return next_id

class TriggerHistoryModel:
    @staticmethod
    def create(client_id: int, trigger_id: int, intensity: int, 
              entry_date: Optional[datetime] = None) -> int:
        if entry_date is None:
            entry_date = datetime.now()
            
        # Get next id
        existing_ids = [doc.get('id', 0) for doc in trigger_history.all()]
        next_id = max(existing_ids, default=0) + 1
        
        trigger_history_data = {
            'id': next_id,
            'client_id': client_id,
            'trigger_id': trigger_id,
            'intensity': intensity,
            'entry_date': entry_date.isoformat()
        }
        trigger_history.insert(trigger_history_data)
        return next_id 