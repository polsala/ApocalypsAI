from flask import Flask, request, jsonify

app = Flask(__name__)

# Define sentiment keywords
POSITIVE_KEYWORDS = ["great", "awesome", "happy", "success", "fix", "resolve", "improve", "good", "excellent", "yay", "hooray"]
NEGATIVE_KEYWORDS = ["bug", "error", "fail", "issue", "problem", "sad", "broken", "bad", "terrible", "crash", "down"]

def analyze_sentiment(text):
    """
    Performs a simple keyword-based sentiment analysis on the given text.
    Returns a tuple: (analysis_category, mood, color, emoji)
    """
    text_lower = text.lower()
    words = text_lower.split()

    pos_count = sum(1 for word in words if word in POSITIVE_KEYWORDS)
    neg_count = sum(1 for word in words if word in NEGATIVE_KEYWORDS)

    analysis = "Neutral"
    mood = "Calm Current"
    color = "#2196F3" # Blue
    emoji = "😌"

    if pos_count > 0 and neg_count > 0:
        # Mixed sentiment
        analysis = "Mixed"
        mood = "Rainbow Ripple"
        color = "#9C27B0" # Purple
        emoji = "🌈"
    elif pos_count > neg_count * 2:
        analysis = "Very Positive"
        mood = "Blissful Aura"
        color = "#8BC34A" # Light Green
        emoji = "✨"
    elif pos_count > neg_count:
        analysis = "Positive"
        mood = "Sunny Disposition"
        color = "#CDDC39" # Lime Green
        emoji = "😊"
    elif neg_count > pos_count * 2:
        analysis = "Very Negative"
        mood = "Stormy Seas"
        color = "#F44336" # Red
        emoji = "⛈️"
    elif neg_count > pos_count:
        analysis = "Negative"
        mood = "Cloudy Outlook"
        color = "#FF9800" # Orange
        emoji = "😟"
    
    return analysis, mood, color, emoji

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400
    
    text = data['text']
    analysis, mood, color, emoji = analyze_sentiment(text)
    
    return jsonify({
        "mood": mood,
        "color": color,
        "emoji": emoji,
        "analysis": analysis
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
