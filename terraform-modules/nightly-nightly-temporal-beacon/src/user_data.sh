#!/bin/bash

# Update system packages
sudo yum update -y

# Install Nginx
sudo yum install -y nginx

# Create a simple index.html with the beacon message and a dynamic timestamp
# The beacon_message variable is injected by Terraform's templatefile function.
BEACON_MESSAGE="${beacon_message}"

cat <<EOF | sudo tee /usr/share/nginx/html/index.html
<!DOCTYPE html>
<html>
<head>
    <title>Temporal Beacon</title>
    <style>
        body { font-family: monospace; background-color: #1a1a2e; color: #e0e0e0; text-align: center; padding-top: 100px; }
        h1 { color: #e94560; font-size: 3em; }
        p { font-size: 1.5em; }
        .timestamp { color: #0f3460; font-size: 1em; }
    </style>
</head>
<body>
    <h1>$BEACON_MESSAGE</h1>
    <p>Status: <span style="color: #53d769;">ACTIVE</span></p>
    <p class="timestamp">Last Signal: $(date)</p>
    <p>_\_ ApocalypsAI Integrator Agent _\_</p>
</body>
</html>
EOF

# Start Nginx service
sudo systemctl start nginx

# Enable Nginx to start on boot
sudo systemctl enable nginx
