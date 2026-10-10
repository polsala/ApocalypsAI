import os
import random
from flask import Flask, jsonify

app = Flask(__name__)

# A collection of comforting image URLs (placeholders for demonstration)
# In a real deployment, these would point to actual, publicly accessible comforting images.
COMFORT_IMAGES = [
    "https://i.imgur.com/example1.jpg", # Placeholder: A fluffy kitten sleeping
    "https://i.imgur.com/example2.jpg", # Placeholder: A serene mountain lake at sunrise
    "https://i.imgur.com/example3.jpg", # Placeholder: A warm cup of tea by a window
    "https://i.imgur.com/example4.jpg", # Placeholder: A cozy blanket fort
    "https://i.imgur.com/example5.jpg", # Placeholder: A friendly dog's happy face
    "https://i.imgur.com/example6.jpg", # Placeholder: A field of wildflowers
    "https://i.imgur.com/example7.jpg", # Placeholder: A gentle rain on a windowpane
    "https://i.imgur.com/example8.jpg"  # Placeholder: A smiling baby
]

SOOTHING_QUOTES = [
    "Even the darkest night will end and the sun will rise.",
    "You are stronger than you think.",
    "Take a deep breath. Everything will be okay.",
    "Small steps every day lead to big changes.",
    "Kindness is a language everyone understands.",
    "The present moment is filled with joy and happiness. If you are attentive, you will see it.",
    "This too shall pass.",
    "You are capable of amazing things.",
    "Rest and be thankful.",
    "Every day is a new beginning."
]

@app.route('/comfort', methods=['GET'])
def get_comfort():
    """
    Returns a random comforting image URL and a soothing quote.
    """
    image_url = random.choice(COMFORT_IMAGES)
    quote = random.choice(SOOTHING_QUOTES)
    return jsonify({
        "image_url": image_url,
        "quote": quote,
        "message": "May this bring a moment of peace to your apocalyptic day!"
    })

@app.route('/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint.
    """
    return jsonify({"status": "Critter is purring!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
