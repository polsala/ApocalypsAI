import pytest
from src.analyzer import analyze_sentiment


def test_positive_sentiment():
    text = "I love this wonderful, fantastic day!"
    assert analyze_sentiment(text) == "😊"


def test_negative_sentiment():
    text = "I hate this terrible, awful situation."
    assert analyze_sentiment(text) == "😞"


def test_neutral_sentiment():
    text = "The sky is blue and the grass is green."
    assert analyze_sentiment(text) == "😐"


def test_mixed_sentiment_equal_counts():
    # One positive, one negative → neutral
    text = "I love the food but hate the service."
    assert analyze_sentiment(text) == "😐"


def test_mixed_sentiment_more_negative():
    # Two negatives vs one positive → negative
    text = "I love the food but the service is terrible and awful."
    assert analyze_sentiment(text) == "😞"
