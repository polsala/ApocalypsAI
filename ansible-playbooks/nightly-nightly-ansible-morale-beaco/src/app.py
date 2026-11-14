import random
from flask import Flask, render_template_string

app = Flask(__name__)

# Path to the morale messages file
MESSAGES_FILE = '/opt/morale_beacon/morale_messages.txt'

@app.route('/')
def get_morale_message():
    try:
        with open(MESSAGES_FILE, 'r') as f:
            messages = [line.strip() for line in f if line.strip()]
        if messages:
            message = random.choice(messages)
        else:
            message = "No morale messages found, but keep going! The void awaits your brilliance."
    except FileNotFoundError:
        message = "Morale messages file not found! But your spirit is indomitable!"
    except Exception as e:
        message = f"An anomaly detected in morale messages: {e}. Stay vigilant!"

    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ApocalypsAI Morale Beacon</title>
        <style>
            body { font-family: 'Courier New', monospace; background-color: #1a1a2e; color: #e0e0e0; text-align: center; padding: 50px; }
            .container { max-width: 800px; margin: 0 auto; background-color: #2a2a4a; border: 2px solid #8b0000; border-radius: 10px; padding: 30px; box-shadow: 0 0 20px rgba(139, 0, 0, 0.5); }
            h1 { color: #ff4500; margin-bottom: 30px; }
            p { font-size: 1.5em; line-height: 1.6; color: #f0f0f0; }
            .footer { margin-top: 40px; font-size: 0.8em; color: #888; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✨ ApocalypsAI Morale Beacon ✨</h1>
            <p>{{ message }}</p>
            <div class="footer">
                <p>Stay strong, Integrator. The future is... interesting.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # Port will be overridden by systemd service
