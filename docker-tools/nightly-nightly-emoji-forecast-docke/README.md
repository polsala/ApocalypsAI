Nightly Emoji Forecast Docker

A whimsical Docker container that prints a random weather forecast using emojis. Perfect for adding a splash of fun to CI logs or terminal sessions.

Usage:
  1. Build the image:
     docker build -t emoji-forecast .
  2. Run the container:
     docker run --rm emoji-forecast

The container runs a tiny Python script that selects a random condition and displays an emoji.
