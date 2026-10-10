import datetime
import threading
import uuid

from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory store for messages
# Structure: {recipient: [{id: str, sender: str, message: str, expires_at: datetime.datetime}]}
messages = {}
message_lock = threading.Lock()

def _cleanup_expired_messages():
    """Removes expired messages from the in-memory store."""
    now = datetime.datetime.now()
    with message_lock:
        for recipient in list(messages.keys()): # Iterate over a copy of keys to allow modification during iteration
            messages[recipient] = [msg for msg in messages[recipient] if msg['expires_at'] > now]
            if not messages[recipient]:
                del messages[recipient]

@app.route('/send', methods=['POST'])
def send_message():
    _cleanup_expired_messages() # Clean up before adding new messages to keep store lean
    data = request.get_json()
    if not data or not all(k in data for k in ['sender', 'recipient', 'message', 'ttl_seconds']):
        return jsonify({'error': 'Missing required fields (sender, recipient, message, ttl_seconds)'}), 400

    try:
        ttl_seconds = int(data['ttl_seconds'])
        if ttl_seconds <= 0:
            return jsonify({'error': 'ttl_seconds must be a positive integer'}), 400
    except ValueError:
        return jsonify({'error': 'ttl_seconds must be an integer'}), 400

    msg_id = str(uuid.uuid4())
    now = datetime.datetime.now()
    expires_at = now + datetime.timedelta(seconds=ttl_seconds)

    new_message = {
        'id': msg_id,
        'sender': data['sender'],
        'message': data['message'],
        'expires_at': expires_at
    }

    with message_lock:
        if data['recipient'] not in messages:
            messages[data['recipient']] = []
        messages[data['recipient']].append(new_message)

    return jsonify({'status': 'Message sent', 'message_id': msg_id}), 201

@app.route('/receive/<recipient>', methods=['GET'])
def receive_messages(recipient):
    _cleanup_expired_messages() # Clean up before retrieving messages
    retrieved_messages = []
    with message_lock:
        if recipient in messages:
            # Filter out expired messages and prepare for return
            valid_messages = [msg for msg in messages[recipient] if msg['expires_at'] > datetime.datetime.now()]
            
            for msg in valid_messages:
                retrieved_messages.append({
                    'id': msg['id'],
                    'sender': msg['sender'],
                    'message': msg['message'],
                    'received_at': datetime.datetime.now().isoformat() # Timestamp of retrieval
                })
            
            # Clear all messages for this recipient after retrieval (one-time read behavior)
            del messages[recipient] 

    return jsonify(retrieved_messages), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
