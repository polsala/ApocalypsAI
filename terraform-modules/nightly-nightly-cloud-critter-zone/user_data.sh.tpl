#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

# Whimsical messages for our critter
MESSAGES=(
    "Hello, fellow traveler! May your bytes be ever swift."
    "The cloud whispers secrets, listen closely."
    "Your digital garden is blooming!"
    "Even in the void, there is connection."
    "May your uptime be long and your latency low."
    "A byte of joy for your day!"
    "Remember to hydrate your servers!"
    "The pixels dance for you."
)

# Pick a random message
RANDOM_INDEX=$(( RANDOM % ${#MESSAGES[@]} ))
CRITTER_MESSAGE="${MESSAGES[$RANDOM_INDEX]}"

# Create a simple HTML page
echo "<!DOCTYPE html>" > /var/www/html/index.html
echo "<html>" >> /var/www/html/index.html
echo "<head><title>Cloud Critter Comfort Zone</title></head>" >> /var/www/html/index.html
echo "<body>" >> /var/www/html/index.html
echo "<h1>Welcome to your Cloud Critter Comfort Zone!</h1>" >> /var/www/html/index.html
echo "<p>Your critter, ${critter_name}, has a message for you:</p>" >> /var/www/html/index.html
echo "<blockquote><i>\"${CRITTER_MESSAGE}\"</i></blockquote>" >> /var/www/html/index.html
echo "<p>May your cloud adventures be filled with whimsy!</p>" >> /var/www/html/index.html
echo "</body>" >> /var/www/html/index.html
echo "</html>" >> /var/www/html/index.html
