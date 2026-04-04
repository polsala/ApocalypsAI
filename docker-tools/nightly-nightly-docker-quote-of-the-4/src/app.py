import random
from flask import Flask, jsonify

app = Flask(__name__)

def load_quotes():
    with open('quotes.txt', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

QUOTES = load_quotes()

@app.route('/quote')
def quote():
    selected = random.choice(QUOTES)
    return jsonify({"quote": selected})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
