import React from 'react';

const SentimentDisplay = ({ sentiment }) => {
  const getDisplayInfo = (currentSentiment) => {
    switch (currentSentiment) {
      case 'hopeful':
        return { icon: '☀️', message: 'Hopeful Breezes: The community feels optimistic and resilient.' };
      case 'anxious':
        return { icon: '🌬️', message: 'Anxious Gusts: A sense of unease or mixed feelings prevails.' };
      case 'despair':
        return { icon: '⛈️', message: 'Despair Storms: Deep concerns and distress are evident.' };
      case 'neutral':
      default:
        return { icon: '☁️', message: 'Neutral Drizzle: The sentiment is calm, balanced, or unclear.' };
    }
  };

  const { icon, message } = getDisplayInfo(sentiment);

  return (
    <div className={`sentiment-display ${sentiment}`}>
      <span className="sentiment-icon" role="img" aria-label={sentiment}>{icon}</span>
      <p>{message}</p>
    </div>
  );
};

export default SentimentDisplay;
