const SentimentAnalyzer = {
  analyze: (text) => {
    if (!text || text.trim() === '') {
      return 'neutral';
    }

    const lowerText = text.toLowerCase();
    let positiveScore = 0;
    let negativeScore = 0;

    const positiveKeywords = [
      'hope', 'joy', 'thrive', 'build', 'grow', 'safe', 'peace', 'good', 'happy', 'strong', 'together', 'future'
    ];
    const negativeKeywords = [
      'fear', 'despair', 'ruin', 'collapse', 'danger', 'threat', 'anxiety', 'bad', 'sad', 'weak', 'alone', 'crisis'
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

    // Determine sentiment based on scores
    // A stronger bias is required for 'hopeful' or 'despair'
    if (positiveScore > negativeScore * 1.5) { 
      return 'hopeful';
    } else if (negativeScore > positiveScore * 1.5) { 
      return 'despair';
    } else if (positiveScore > 0 || negativeScore > 0) { // If there's any sentiment, but not strongly biased
      return 'anxious';
    } else {
      return 'neutral';
    }
  }
};

export default SentimentAnalyzer;
