import React from 'react';
import './SentimentDisplay.css';

function SentimentDisplay({ sentiment }) {
  if (!sentiment) {
    return null;
  }

  const maxScore = Math.max(...Object.values(sentiment));

  return (
    <div className="sentiment-container">
      <h2>Void's Whispers:</h2>
      {Object.entries(sentiment).map(([key, value]) => (
        <div className="sentiment-bar-wrapper" key={key}>
          <span className="sentiment-label">{key.charAt(0).toUpperCase() + key.slice(1)}:</span>
          <div className="sentiment-bar-background">
            <div
              className={`sentiment-bar sentiment-${key}`}
              style={{ width: `${(value / (maxScore || 1)) * 100}%` }}
              title={`${value.toFixed(2)}`}
            >
              <span className="sentiment-value">{value.toFixed(2)}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default SentimentDisplay;
