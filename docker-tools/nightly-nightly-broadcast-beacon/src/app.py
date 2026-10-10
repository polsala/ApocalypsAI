import os
from flask import Flask, render_template_string, send_from_directory

# Determine the base directory of the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR_PATH = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, static_folder=STATIC_DIR_PATH) # Tell Flask where the static folder is

# HTML template for the main page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nightly Broadcast Beacon</title>
    <style>
        body { font-family: monospace; background-color: #1a1a1a; color: #00ff00; margin: 20px; }
        h1 { color: #00ff00; text-shadow: 0 0 5px #00ff00; }
        ul { list-style-type: none; padding: 0; }
        li { margin-bottom: 10px; }
        a { color: #00ffff; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .footer { margin-top: 30px; font-size: 0.8em; color: #008800; }
    </style>
</head>
<body>
    <h1>📡 Nightly Broadcast Beacon 📡</h1>
    <p>Tune in to the whispers of the wasteland:</p>
    <ul>
        {% for file in files %}
            <li><a href="/broadcast/{{ file }}">{{ file }}</a></li>
        {% else %}
            <li>No broadcasts found. The airwaves are silent...</li>
        {% endfor %}
    </ul>
    <div class="footer">
        <p>Stay vigilant. Stay safe. This message brought to you by ApocalypsAI.</p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """
    Lists all available broadcast files in the static directory.
    """
    try:
        # Use STATIC_DIR_PATH for listing files
        files = sorted([f for f in os.listdir(STATIC_DIR_PATH) if os.path.isfile(os.path.join(STATIC_DIR_PATH, f))])
    except FileNotFoundError:
        files = []
    return render_template_string(HTML_TEMPLATE, files=files)

@app.route('/broadcast/<filename>')
def broadcast_file(filename):
    """
    Serves a specific broadcast file from the static directory.
    Flask's send_from_directory will use the static_folder configured in the app.
    """
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    # Ensure the static directory exists for local testing
    if not os.path.exists(STATIC_DIR_PATH):
        os.makedirs(STATIC_DIR_PATH)
        # Create some dummy files for local testing
        with open(os.path.join(STATIC_DIR_PATH, 'message_01.txt'), 'w') as f:
            f.write("Greetings, survivor! Remember to conserve water.")
        with open(os.path.join(STATIC_DIR_PATH, 'ambient_winds.txt'), 'w') as f: # Using .txt for simplicity, could be .mp3
            f.write("Sound of distant winds...")
    app.run(debug=True, host='0.0.0.0', port=8080)
