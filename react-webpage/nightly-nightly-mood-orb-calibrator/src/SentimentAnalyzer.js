export const analyzeSentiment = (text) => {
  const lowerText = text.toLowerCase();
  let positiveScore = 0;
  let negativeScore = 0;

  const positiveKeywords = [
    'love', 'joy', 'hope', 'good', 'great', 'happy', 'safe', 'secure', 'thriving', 'peace', 'calm', 'progress', 'success', 'win', 'bright', 'future'
  ];
  const negativeKeywords = [
    'fear', 'danger', 'threat', 'bad', 'awful', 'sad', 'broken', 'lost', 'despair', 'chaos', 'struggle', 'pain', 'fail', 'dark', 'ruin'
  ];

  positiveKeywords.forEach(keyword => {
    if (lowerText.includes(keyword)) {
      positiveScore++;
    }
  });

  negativeKeywords.forEach(keyword => {
    if (lowerText.includes(keyword)) {
      negativeScore++;
    }
  });

  let label = 'neutral';
  if (positiveScore > negativeScore) {
    label = 'positive';
  } else if (negativeScore > positiveScore) {
    label = 'negative';
  }

  return { score: positiveScore - negativeScore, label };
};
