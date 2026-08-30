import pytest
from src.app import app, analyze_sentiment

# Mock rationale: The sentiment analysis is purely keyword-based and self-contained.
# No external APIs or file system access are involved, so no complex mocking is needed
# for the `analyze_sentiment` function itself.
# For testing the Flask app routes, we use Flask's built-in test client, which
# effectively mocks the HTTP request/response cycle.

@pytest.fixture
def client():
    """Configures the Flask app for testing."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_analyze_sentiment_very_positive():
    """Test very positive sentiment."""
    text = "This is a great success! Feeling awesome and happy."
    analysis, mood, color, emoji = analyze_sentiment(text)
    assert analysis == "Very Positive"
    assert mood == "Blissful Aura"
    assert color == "#8BC34A"
    assert emoji == "✨"

def test_analyze_sentiment_positive():
    """Test positive sentiment."""
    text = "Fixed an issue, feeling good."
    analysis, mood, color, emoji = analyze_sentiment(text)
    assert analysis == "Positive"
    assert mood == "Sunny Disposition"
    assert color == "#CDDC39"
    assert emoji == "😊"

def test_analyze_sentiment_neutral():
    """Test neutral sentiment."""
    text = "Refactored some code. Updated documentation."
    analysis, mood, color, emoji = analyze_sentiment(text)
    assert analysis == "Neutral"
    assert mood == "Calm Current"
    assert color == "#2196F3"
    assert emoji == "😌"

def test_analyze_sentiment_negative():
    """Test negative sentiment."""
    text = "Found a problem, it's a bad issue."
    analysis, mood, color, emoji = analyze_sentiment(text)
    assert analysis == "Negative"
    assert mood == "Cloudy Outlook"
    assert color == "#FF9800"
    assert emoji == "😟"

def test_analyze_sentiment_very_negative():
    """Test very negative sentiment."""
    text = "The system crashed, a terrible error occurred. Everything is broken."
    analysis, mood, color, emoji = analyze_sentiment(text)
    assert analysis == "Very Negative"
    assert mood == "Stormy Seas"
    assert color == "#F44336"
    assert emoji == "⛈️"

def test_analyze_sentiment_mixed():
    """Test mixed sentiment (both positive and negative keywords present, but not strongly one way)."""
    text = "Great new feature, but it has a small bug."
    analysis, mood, color, emoji = analyze_sentiment(text)
    assert analysis == "Mixed"
    assert mood == "Rainbow Ripple"
    assert color == "#9C27B0"
    assert emoji == "🌈"

def test_analyze_sentiment_empty_text():
    """Test with empty text."""
    text = ""
    analysis, mood, color, emoji = analyze_sentiment(text)
    assert analysis == "Neutral"
    assert mood == "Calm Current"
    assert color == "#2196F3"
    assert emoji == "😌"

def test_analyze_sentiment_no_keywords():
    """Test with text containing no defined keywords."""
    text = "The quick brown fox jumps over the lazy dog."
    analysis, mood, color, emoji = analyze_sentiment(text)
    assert analysis == "Neutral"
    assert mood == "Calm Current"
    assert color == "#2196F3"
    assert emoji == "😌"

def test_analyze_endpoint_success(client):
    """Test the /analyze endpoint with a valid request."""
    response = client.post('/analyze', json={'text': 'This is a great success!'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['analysis'] == 'Very Positive'
    assert data['mood'] == 'Blissful Aura'
    assert data['color'] == '#8BC34A'
    assert data['emoji'] == '✨'

def test_analyze_endpoint_missing_text(client):
    """Test the /analyze endpoint with missing 'text' field."""
    response = client.post('/analyze', json={'other_field': 'value'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == "Missing 'text' in request body"

def test_analyze_endpoint_empty_json(client):
    """Test the /analyze endpoint with an empty JSON body."""
    response = client.post('/analyze', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == "Missing 'text' in request body"

def test_analyze_endpoint_non_json(client):
    """Test the /analyze endpoint with a non-JSON body."""
    response = client.post('/analyze', data='plain text body')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
