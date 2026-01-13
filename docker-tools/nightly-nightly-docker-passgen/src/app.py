import secrets
import string
from flask import Flask, request, jsonify

app = Flask(__name__)

ALLOWED_CHARS = string.ascii_letters + string.digits + string.punctuation
DEFAULT_LENGTH = 12
MAX_LENGTH = 64

def generate_password(length: int) -> str:
    """Return a cryptographically secure random password of *length* characters."""
    return ''.join(secrets.choice(ALLOWED_CHARS) for _ in range(length))

@app.route('/generate')
def generate_endpoint():
    # Parse optional length query param
    try:
        length = int(request.args.get('length', DEFAULT_LENGTH))
    except ValueError:
        return jsonify(error='Invalid length parameter'), 400
    if length < 1 or length > MAX_LENGTH:
        return jsonify(error=f'Length must be between 1 and {MAX_LENGTH}'), 400
    pwd = generate_password(length)
    return jsonify(password=pwd)

if __name__ == '__main__':
    # Bind to all interfaces so Docker can expose the port
    app.run(host='0.0.0.0', port=8080)

