#!/bin/bash
yum update -y
yum install -y python3 python3-pip
pip3 install flask gunicorn pytz

cat << 'EOF' > /home/ec2-user/app.py
from flask import Flask
from datetime import datetime
import pytz
import random

app = Flask(__name__)

whimsical_messages = [
    "The sands of time continue their relentless march, even here.",
    "Tick-tock goes the cosmic clock, heed its silent decree.",
    "In the grand tapestry of existence, this moment is but a fleeting stitch.",
    "Time, a river without banks, flows ever onward.",
    "Even in the void, the rhythm of time persists."
]

@app.route('/')
def get_time():
    now_utc = datetime.now(pytz.utc)
    message = random.choice(whimsical_messages)
    return {
        "current_utc_time": now_utc.isoformat(),
        "beacon_status": "Operational",
        "whimsical_insight": message
    }

if __name__ == '__main__':
    # Gunicorn will be started by systemd
    pass
EOF

# Create a systemd service file for Gunicorn
cat << 'EOF' > /etc/systemd/system/chrono-beacon.service
[Unit]
Description=Gunicorn instance to serve Chrono Beacon
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user
ExecStart=/usr/local/bin/gunicorn --workers 4 --bind 0.0.0.0:80 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable chrono-beacon
systemctl start chrono-beacon
