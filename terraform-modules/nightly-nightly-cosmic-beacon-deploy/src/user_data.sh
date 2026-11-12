#!/bin/bash
set -euo pipefail

# Install necessary packages
sudo yum update -y
sudo yum install -y python3 python3-pip

# Install Flask
pip3 install Flask

# Create the Flask application directory
mkdir -p /opt/beacon_app
cd /opt/beacon_app

# Create the Flask application
cat <<EOF > app.py
from flask import Flask, request
import random
import os

app = Flask(__name__)

MESSAGES = [
    "The cosmos whispers encouragement!",
    "Your resilience shines brighter than a supernova!",
    "Even black holes have a silver lining!",
    "May your journey through the void be filled with stardust!",
    "Embrace the cosmic dance!",
    "You are a star in the making!",
    "The universe believes in you!",
    "Keep shining, cosmic traveler!",
    "Distress signals? More like opportunities for growth!",
    "Your light pierces the darkest corners of space!"
]

@app.route('/')
def home():
    # Simulate some CPU work to trigger scaling
    if random.random() < 0.1: # 10% chance to do some heavy work
        _ = [i*i for i in range(10**6)] # CPU intensive operation
    
    message = random.choice(MESSAGES)
    instance_id = os.getenv('INSTANCE_ID', 'unknown')
    return f"<h1>Cosmic Beacon ({instance_id}): {message}</h1><p>Powered by ApocalypsAI</p>"

if __name__ == '__main__':
    # Get instance ID from instance metadata
    INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id || echo "i-mock-instance")
    os.environ['INSTANCE_ID'] = INSTANCE_ID
    app.run(host='0.0.0.0', port=80)
EOF

# Make the app executable and run it
chmod +x app.py
nohup python3 app.py > /var/log/beacon_app.log 2>&1 &
