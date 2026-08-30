import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Retrieve message and color from environment variables, with defaults
    message = os.environ.get('BEACON_MESSAGE', 'Status: Unknown. Proceed with caution.')
    color = os.environ.get('BEACON_COLOR', 'lightgray')
    return render_template('index.html', message=message, color=color)

if __name__ == '__main__':
    # This block is for local development/testing, not typically used in Gunicorn
    app.run(host='0.0.0.0', port=8080, debug=True)
