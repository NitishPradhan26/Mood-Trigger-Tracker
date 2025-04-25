from flask import Flask, request, jsonify
from models.database import (
    ClientModel, TriggerModel, 
    MoodHistoryModel, TriggerHistoryModel,
    triggers, clients, trigger_history, mood_history
)
from flask_cors import CORS
from models.database import Query

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",  # Your frontend in development
            "https://your-production-domain.com"  # Your frontend in production
        ]
    }
})


@app.route("/")
def hello_world():
    return 'Hello, World'

@app.route("/client", methods=['POST'])
def create_client():
    data = request.get_json()
    try:
        client_id = ClientModel.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone_number=data['phone_number']
        )
        return jsonify({'client_id': client_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route("/trigger", methods=['POST'])
def create_trigger():
    data = request.get_json()
    try:
        trigger_id = TriggerModel.create(
            name=data['name'],
            description=data.get('description'),
            feelings=data.get('feelings', [])  # Optional array of feelings
        )
        return jsonify({'trigger_id': trigger_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route("/mood", methods=['POST'])
def record_mood():
    data = request.get_json()
    print('reached record mood')
    print('data', data)
    try:
        mood_id = MoodHistoryModel.create(
            #Client ID is hardcoded to 1 for now
            client_id=1,
            mood=data['mood']
        )
        return jsonify({'mood_id': mood_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/trigger-history", methods=['POST'])
def record_trigger():
    data = request.get_json()
    #debug
    print(data)
    try:
        # Get trigger name from request
        trigger_name = data['trigger_name']
        intensity = data['intensity']
        
        # Find trigger_id from name
        Trigger = Query()
        print('Reached just before query---------')
        trigger = triggers.get(Trigger.name == trigger_name)
        print('Received trigger_name:', trigger_name)  # Debug the incoming name
        print('Found trigger:', trigger)  # Debug what was found

        if not trigger:
            print(f'Trigger "{trigger_name}" not found')
            return jsonify({'error': f'Trigger "{trigger_name}" not found'}), 404

        print('triggerId', trigger['trigger_id'])  # Only access after checking existence
            
        # For now, we'll use a fixed client_id (e.g., 1)
        history_id = TriggerHistoryModel.create(
            client_id=1,  # Fixed client_id for now
            trigger_id=trigger['trigger_id'],
            intensity=intensity
        )
        return jsonify({'history_id': history_id}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/client/<full_name>", methods=['GET'])
def get_client(full_name):
    try:
        # Split the full name into first and last name
        first_name, last_name = full_name.split(' ')
        
        Client = Query()
        client = clients.get(
            (Client.first_name == first_name) & 
            (Client.last_name == last_name)
        )
        
        if not client:
            return jsonify({'error': 'Client not found'}), 404
            
        return jsonify(client), 200
        
    except ValueError as e:
        return jsonify({'error': 'Invalid name format. Use "First Last"'}), 400

@app.route("/trigger-history/<full_name>", methods=['GET'])
def get_trigger_history(full_name):
    try:
        # Split the full name into first and last name
        first_name, last_name = full_name.split(' ')
        print('first_name', first_name)
        print('last_name', last_name)
        # First find the client
        Client = Query()
        client = clients.get(
            (Client.first_name == first_name) & 
            (Client.last_name == last_name)
        )
        
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        
        print('client', client)
        # Get all trigger history entries for this client
        TriggerHistory = Query()
        history = trigger_history.search(TriggerHistory.client_id == client['client_id'])
        # Enhance the history with trigger names
        enhanced_history = []
        for entry in history:
            trigger = triggers.get(doc_id=entry['trigger_id'])
            enhanced_history.append({
                'date': entry['entry_date'],
                'trigger_name': trigger['name'],
                'intensity': entry['intensity'],
                'feelings': trigger['feelings']  # Add feelings to response
            })
            
        return jsonify(enhanced_history), 200
        
    except ValueError as e:
        return jsonify({'error': 'Invalid name format. Use "First Last"'}), 400

@app.route("/clients", methods=['GET'])
def get_all_clients():
    try:
        # Get all clients from the database
        all_clients = clients.all()
        
        if not all_clients:
            return jsonify({'message': 'No clients found'}), 404
            
        return jsonify(all_clients), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/mood-history/<full_name>", methods=['GET'])
def get_mood_history(full_name):
    try:
        # Split the full name into first and last name
        first_name, last_name = full_name.split(' ')
        print('---------Full name:', full_name)
        # First find the client
        Client = Query()
        client = clients.get(
            (Client.first_name == first_name) & 
            (Client.last_name == last_name)
        )
        
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        
        print('---------Found client:', client['client_id'])
        # Get all mood history entries for this client
        MoodHistory = Query()
        history = mood_history.search(MoodHistory.client_id == client['client_id'])
        
        print('---------Found history:')
        # Format the mood history
        formatted_history = []
        for entry in history:
            formatted_history.append({
                'date': entry['entry_date'],
                'mood': entry['mood'],
            })
            
        return jsonify(formatted_history), 200
        
    except ValueError as e:
        return jsonify({'error': 'Invalid name format. Use "First Last"'}), 400

@app.route("/triggers", methods=['GET'])
def get_all_triggers():
    try:
        # Get all triggers directly from the triggers table
        all_triggers = triggers.all()
        
        if not all_triggers:
            return jsonify({'message': 'No triggers found'}), 404
            
        # Format the response to include all trigger details
        formatted_triggers = []
        for trigger in all_triggers:
            formatted_triggers.append({
                'trigger_id': trigger['trigger_id'],
                'name': trigger['name'],
                'description': trigger['description'],
                'feelings': trigger['feelings']
            })
            
        return jsonify(formatted_triggers), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add this block to make the file runnable
if __name__ == '__main__':
    app.run(debug=True)