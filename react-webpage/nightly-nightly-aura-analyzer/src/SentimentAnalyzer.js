export const analyze = (text) => {
  if (!text || text.trim() === '') {
    return { sentiment: 'neutral', score: 0, description: 'Awaiting input...' };
  }

  const lowerText = text.toLowerCase();
  let positiveScore = 0;
  let negativeScore = 0;

  const positiveWords = ['good', 'great', 'excellent', 'happy', 'joy', 'love', 'hope', 'peace', 'thrive', 'survive', 'strong', 'safe', 'well', 'calm', 'bright', 'resourceful', 'abundance', 'success', 'victory'];
  const negativeWords = ['bad', 'terrible', 'awful', 'sad', 'fear', 'hate', 'despair', 'danger', 'threat', 'weak', 'unsafe', 'sick', 'anxious', 'dark', 'scarce', 'failure', 'defeat', 'ruin', 'lost', 'broken'];

  positiveWords.forEach(word => {
    if (lowerText.includes(word)) {
      positiveScore++;
    }
  });

  negativeWords.forEach(word => {
    if (lowerText.includes(word)) {
      negativeScore++;
    }
  });

  const score = positiveScore - negativeScore;

  let sentiment = 'neutral';
  let description = 'Feeling balanced.';

  if (score > 0) {
    sentiment = 'positive';
    if (score >= 3) description = 'Radiant with hope!';
    else description = 'Optimistic vibrations.';
  } else if (score < 0) {
    sentiment = 'negative';
    if (score <= -3) description = 'Shadows of despair...';
    else description = 'A touch of gloom.';
  }

  return { sentiment, score, description };
};
