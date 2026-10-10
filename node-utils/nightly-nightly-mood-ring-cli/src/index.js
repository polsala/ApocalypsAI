#!/usr/bin/env node

const analyzeMood = (text) => {
  const positiveKeywords = ['love', 'happy', 'joy', 'great', 'excellent', 'wonderful', 'amazing', 'good', 'success', 'win', 'optimistic', 'hope', 'bright'];
  const negativeKeywords = ['sad', 'angry', 'bad', 'terrible', 'awful', 'failure', 'lose', 'hate', 'difficult', 'problem', 'gloom', 'despair', 'dark'];

  const lowerText = text.toLowerCase();
  let positiveCount = 0;
  let negativeCount = 0;

  positiveKeywords.forEach(keyword => {
    if (lowerText.includes(keyword)) {
      positiveCount++;
    }
  });

  negativeKeywords.forEach(keyword => {
    if (lowerText.includes(keyword)) {
      negativeCount++;
    }
  });

  if (positiveCount > negativeCount) {
    return { color: 'Rose Quartz', description: 'Radiant with optimism, a beacon of hope!' };
  } else if (negativeCount > positiveCount) {
    return { color: 'Obsidian Black', description: 'Reflecting deep contemplation, perhaps a touch of cosmic gloom.' };
  } else {
    // If counts are equal, or both zero
    if (positiveCount === 0 && negativeCount === 0) {
      return { color: 'Moonstone Grey', description: 'Calm and collected, observing the cosmic dance with serene detachment.' };
    } else {
      // Equal positive and negative keywords, implies mixed feelings
      return { color: 'Amethyst Purple', description: 'A swirl of emotions, a truly complex cosmic tapestry.' };
    }
  }
};

const runCli = () => {
  const args = process.argv.slice(2);
  let inputText = '';

  if (args.length > 0) {
    inputText = args.join(' ');
  } else {
    // Read from stdin if no arguments provided
    console.error('Usage: nightly-mood-ring <text> or echo "text" | nightly-mood-ring');
    process.exit(1);
  }

  if (!inputText) {
    // This path should ideally be caught by the process.exit(1) above if args.length is 0
    // but included for robustness if an empty string somehow makes it through.
    console.log('No text provided. Defaulting to neutral mood.');
    console.log('Color: Moonstone Grey');
    console.log('Description: Calm and collected, observing the cosmic dance with serene detachment.');
    return;
  }

  const mood = analyzeMood(inputText);
  console.log(`Color: ${mood.color}`);
  console.log(`Description: ${mood.description}`);
};

// Export for testing
module.exports = { analyzeMood, runCli };

// Only run CLI if executed directly
if (require.main === module) {
  runCli();
}
