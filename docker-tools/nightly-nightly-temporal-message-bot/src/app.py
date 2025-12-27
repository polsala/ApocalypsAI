import uuid
from datetime import datetime, timezone
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for messages. In a real application, this would be a database.
# Structure: {message_id: {'message': '...', 'timestamp': datetime_object}}
message_bottles = {}

@app.route('/bottle', methods=['POST'])
def bottle_message():
    """Bottles a message with a specified UTC timestamp."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    message = data.get('message')
    timestamp_str = data.get('timestamp')

    if not message or not timestamp_str:
        return jsonify({'error': 'Missing "message" or "timestamp" field'}), 400

    try:
        # Parse timestamp string into a timezone-aware datetime object (UTC)
        bottling_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        if bottling_time.tzinfo is None:
            bottling_time = bottling_time.replace(tzinfo=timezone.utc)
        else:
            bottling_time = bottling_time.astimezone(timezone.utc)

    except ValueError:
        return jsonify({'error': 'Invalid timestamp format. Use ISO 8601 (e.g., 2024-01-01T12:00:00Z)'}), 400

    message_id = str(uuid.uuid4())
    message_bottles[message_id] = {
        'message': message,
        'timestamp': bottling_time
    }

    return jsonify({
        'status': 'Message bottled successfully',
        'id': message_id,
        'bottled_at': bottling_time.isoformat().replace('+00:00', 'Z')
    }), 201

@app.route('/uncork', methods=['GET'])
def uncork_messages():
    """Retrieves messages whose bottled time has arrived or passed."""
    current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    uncorked = []

    for msg_id, msg_data in message_bottles.items():
        if msg_data['timestamp'] <= current_time:
            uncorked.append({
                'id': msg_id,
                'message': msg_data['message'],
                'timestamp': msg_data['timestamp'].isoformat().replace('+00:00', 'Z')
            })
    
    # Sort by timestamp for consistent output
    uncorked.sort(key=lambda x: x['timestamp'])

    return jsonify({'messages': uncorked}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
