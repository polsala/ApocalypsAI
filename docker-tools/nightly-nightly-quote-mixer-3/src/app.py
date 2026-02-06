import random
from flask import Flask, jsonify

app = Flask(__name__)

inspirational = [
    "The only limit to our realization of tomorrow is our doubts of today.",
    "Believe you can and you're halfway there.",
    "Dream big and dare to fail."
]

apocalyptic = [
    "When the sky falls, we shall dance.",
    "The end is just a new beginning in disguise.",
    "Ashes to ashes, dust to code."
]

def blend_quotes():
    a = random.choice(inspirational)
    b = random.choice(apocalyptic)
    return f"{a} {b}"

@app.route("/quote")
def quote():
    return jsonify({"quote": blend_quotes()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
