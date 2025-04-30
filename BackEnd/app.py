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
        "origins": ["http://localhost:3000"],  # Your frontend development server
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
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
    print('Received request at /mood endpoint')
    print('Request method:', request.method)
    print('Request headers:', request.headers)
    data = request.get_json()
    print('Request data:', data)
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
    
    try:
        # Get trigger name from request and normalize it
        trigger_name = data['trigger_name'].lower()
        intensity = data['intensity']
        
        # Find trigger_id from name with case-insensitive comparison
        Trigger = Query()
        trigger = triggers.get(
            Trigger.name.test(lambda x: x.lower() == trigger_name)
        )

        if not trigger:
            return jsonify({'error': f'Trigger "{data["trigger_name"]}" not found'}), 404
            
        # For now, we'll use a fixed client_id (e.g., 1)
        history_id = TriggerHistoryModel.create(
            client_id=1,
            trigger_id=trigger.doc_id,
            intensity=intensity
        )
        return jsonify({'history_id': history_id}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/client/<full_name>", methods=['GET'])
def get_client(full_name):
    try:
        # Split and normalize the full name
        first_name, last_name = full_name.split(' ')
        first_name = first_name.lower()
        last_name = last_name.lower()
        
        # Find client with case-insensitive comparison
        Client = Query()
        client = clients.get(
            (Client.first_name.test(lambda x: x.lower() == first_name)) & 
            (Client.last_name.test(lambda x: x.lower() == last_name))
        )
        
        if not client:
            return jsonify({'error': 'Client not found'}), 404
            
        return jsonify(client), 200
        
    except ValueError as e:
        return jsonify({'error': 'Invalid name format. Use "First Last"'}), 400

@app.route("/trigger-history/<full_name>", methods=['GET'])
def get_trigger_history(full_name):
    try:
        # Split and normalize the full name
        first_name, last_name = full_name.split(' ')
        first_name = first_name.lower()
        last_name = last_name.lower()
        
        # Find client with case-insensitive comparison
        Client = Query()
        client = clients.get(
            (Client.first_name.test(lambda x: x.lower() == first_name)) & 
            (Client.last_name.test(lambda x: x.lower() == last_name))
        )
        
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        
        # Get all trigger history entries for this client
        TriggerHistory = Query()
        history = trigger_history.search(TriggerHistory.client_id == client['client_id'])
        
        # Enhance the history with trigger names
        enhanced_history = []
        for entry in history:
            trigger = triggers.get(doc_id=entry['trigger_id'])
            if trigger:  # Add this check
                enhanced_history.append({
                    'date': entry['entry_date'],
                    'trigger_name': trigger['name'],
                    'intensity': entry['intensity'],
                    'feelings': trigger['feelings']
                })
            else:
                print(f"Warning: Trigger not found for ID {entry['trigger_id']}")
        
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
        # Split and normalize the full name
        first_name, last_name = full_name.split(' ')
        first_name = first_name.lower()
        last_name = last_name.lower()
        
        # Find client with case-insensitive comparison
        Client = Query()
        client = clients.get(
            (Client.first_name.test(lambda x: x.lower() == first_name)) & 
            (Client.last_name.test(lambda x: x.lower() == last_name))
        )
        
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        
        # Get all mood history entries for this client
        MoodHistory = Query()
        history = mood_history.search(MoodHistory.client_id == client['client_id'])
        
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

@app.route("/trigger-history/batch", methods=['POST'])
def create_trigger_history_batch():
    data = request.get_json()
    results = []
    
    print('Received triggers:', data)
    
    for trigger_entry in data['triggers']:
        try:
            # Case-insensitive trigger name comparison
            trigger_name = trigger_entry['trigger_name'].lower()
            
            # Find the trigger document using consistent Query format
            TriggerQuery = Query()
            trigger = triggers.get(
                TriggerQuery.name.test(lambda x: x.lower() == trigger_name)
            )
            
            if not trigger:
                print(f"Trigger not found: {trigger_entry['trigger_name']}")
                return jsonify({'error': f'Trigger not found: {trigger_entry["trigger_name"]}'}), 400
                
            print(f"Found trigger: {trigger}")
            
            # Get the trigger's ID from the document
            trigger_id = trigger['trigger_id']
            
            history_id = TriggerHistoryModel.create(
                client_id=1,
                trigger_id=trigger_id,
                intensity=trigger_entry['intensity']
            )
            results.append(history_id)
        except Exception as e:
            print(f"Error processing trigger: {str(e)}")
            return jsonify({'error': str(e)}), 400
            
    return jsonify({'trigger_history_ids': results}), 201

@app.route("/chart-data/<full_name>", methods=['GET'])
def get_chart_data(full_name):
    try:
        # Split and normalize the full name
        first_name, last_name = full_name.split(' ')
        first_name = first_name.lower()
        last_name = last_name.lower()
        
        # Find client with case-insensitive comparison
        Client = Query()
        client = clients.get(
            (Client.first_name.test(lambda x: x.lower() == first_name)) & 
            (Client.last_name.test(lambda x: x.lower() == last_name))
        )
        
        if not client:
            return jsonify({'error': 'Client not found'}), 404
            
        # Get all entries
        MoodHistory = Query()
        mood_entries = mood_history.search(MoodHistory.client_id == client['client_id'])
        
        # Get trigger history
        TriggerHistory = Query()
        trigger_entries = trigger_history.search(TriggerHistory.client_id == client['client_id'])
        
        # Format data for charts
        chart_data = []
        
        # Add mood data points
        for entry in sorted(mood_entries, key=lambda x: x['entry_date']):
            chart_data.append({
                'timestamp': entry['entry_date'],
                'value': entry['mood'],
                'type': 'mood'
            })
            
        # Add trigger data points
        for entry in sorted(trigger_entries, key=lambda x: x['entry_date']):
            trigger = triggers.get(doc_id=entry['trigger_id'])
            if trigger:
                chart_data.append({
                    'timestamp': entry['entry_date'],
                    'value': entry['intensity'],
                    'type': trigger['name']
                })
                
        return jsonify(chart_data), 200
        
    except ValueError as e:
        return jsonify({'error': 'Invalid name format. Use "First Last"'}), 400

# Add this block to make the file runnable
if __name__ == '__main__':
    app.run(debug=True)