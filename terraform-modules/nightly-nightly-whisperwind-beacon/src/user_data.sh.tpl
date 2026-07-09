#!/bin/bash
set -euo pipefail

# Install Python and Flask
sudo yum update -y
sudo yum install -y python3 python3-pip

# Install AWS CLI for S3 interaction
sudo pip3 install awscli flask boto3

# Create a simple Flask app
mkdir -p /opt/beacon
cat <<EOF > /opt/beacon/app.py
from flask import Flask
import os
import datetime
import boto3

app = Flask(__name__)

BEACON_MESSAGE = "${beacon_message}"
BEACON_PORT = ${beacon_port}
S3_BUCKET_NAME = "${s3_bucket_name}"
AWS_REGION = "${region}"

s3_client = boto3.client('s3', region_name=AWS_REGION)

@app.route('/')
def hello_world():
    timestamp = datetime.datetime.now().isoformat()
    log_message = f"[{timestamp}] Beacon emitted: {BEACON_MESSAGE}"
    print(log_message)

    # Log to S3
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=f"beacon-logs/{timestamp}.log",
            Body=log_message.encode('utf-8')
        )
        print(f"Logged to S3: s3://{S3_BUCKET_NAME}/beacon-logs/{timestamp}.log")
    except Exception as e:
        print(f"Error logging to S3: {e}")

    return f"<h1>Whisperwind Beacon Active!</h1><p>{BEACON_MESSAGE}</p><p>Last emitted: {timestamp}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=BEACON_PORT)
EOF

# Start the Flask app using systemd
cat <<EOF > /etc/systemd/system/beacon.service
[Unit]
Description=Whisperwind Beacon Flask App
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/opt/beacon
ExecStart=/usr/bin/python3 /opt/beacon/app.py
Restart=always
RestartSec=3
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=whisperwind-beacon

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable beacon
sudo systemctl start beacon
