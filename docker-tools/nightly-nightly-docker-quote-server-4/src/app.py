from flask import Flask, Response
import random\n\napp = Flask(__name__)\n\nQUOTES = [
    "The only limit to our realization of tomorrow is our doubts of today.",
    "Life is 10% what happens to us and 90% how we react to it.",
    "In the middle of difficulty lies opportunity.",
    "The purpose of our lives is to be happy.",
    "Turn your wounds into wisdom."
]\n\n\ndef get_random_quote():
    """Return a random quote from the QUOTES list."""
    return random.choice(QUOTES)\n\n\n@app.route("/", methods=["GET"])
def quote_endpoint():
    quote = get_random_quote()
    return Response(quote, mimetype="text/plain")\n\n\nif __name__ == "__main__":
    # Run on host port 8080 inside the container
    app.run(host="0.0.0.0", port=8080)\n
