#!/bin/bash
set -e
# Install nginx
apt-get update
apt-get install -y nginx
# Create a simple HTML page
cat > /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
  <title>Void Garden</title>
  <style>
    body { font-family: Arial, sans-serif; background: #0f0f1a; color: #e0e0e0; text-align: center; padding: 50px; }
    h1 { color: #8bc34a; }
    a { color: #4fc3f7; }
  </style>
</head>
<body>
  <h1>Welcome to the Void Garden</h1>
  <p>This is a whimsical cloud garden created by Terraform.</p>
  <p>Explore the garden and find the hidden easter egg!</p>
  <p><a href="${easter_egg_path}">Find the Easter Egg</a></p>
</body>
</html>
EOF
# Create the easter egg page
mkdir -p /var/www/html/whimsical-void
cat > /var/www/html/whimsical-void/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
  <title>Whimsical Void</title>
  <style>
    body { font-family: Arial, sans-serif; background: #1a1a2e; color: #e0e0e0; text-align: center; padding: 50px; }
    h1 { color: #ff9800; }
    .emoji { font-size: 48px; margin: 20px; }
  </style>
</head>
<body>
  <div class="emoji">✨</div>
  <h1>You Found the Whimsical Void!</h1>
  <p>Congratulations! You've discovered the hidden easter egg.</p>
  <p>May your code be bug-free and your deployments smooth.</p>
  <div class="emoji">🎉</div>
</body>
</html>
EOF
# Start nginx
systemctl start nginx
systemctl enable nginx
