from flask import Flask, request, jsonify
import random

app = Flask(__name__)

GENRES = {
    'post-apocalyptic': ['Radiation Rock', 'Wasteland Blues'],
    'survival': ['Bushcraft Ballads', 'Foraging Folk'],
    'industrial': ['Scrap Metal Grooves', 'Fusion Core Beats']
}

@app.route('/playlist')
def generate_playlist():
    genre = request.args.get('genre', 'survival')
    mood = request.args.get('mood', 'practical')
    items = GENRES.get(genre, ['Survival Essentials'])
    return jsonify({
        'theme': f"{genre.capitalize()} {mood.title()} Mix",
        'tracks': [f"{item} #{i+1}" for i, item in enumerate(random.sample(items, 5))],
        'survival_tip': 'Store at least 3 liters of water per person per day.'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
