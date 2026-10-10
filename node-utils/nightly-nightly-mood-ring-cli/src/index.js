#!/usr/bin/env node

const positiveWords = new Set([
  "happy", "good", "great", "excellent", "wonderful", "joy", "love", "success",
  "calm", "peaceful", "serene", "hopeful", "bright", "positive", "fantastic",
  "amazing", "superb", "delightful", "optimistic", "thriving", "smooth", "stable"
]);

const negativeWords = new Set([
  "sad", "bad", "terrible", "awful", "horrible", "fear", "hate", "failure",
  "angry", "chaotic", "turbulent", "despair", "dark", "negative", "frustrating",
  "problem", "issue", "crash", "bug", "error", "stressed", "worried", "difficult"
]);

const moodDefinitions = {
  "blue": {
    "emoji": "🔵",
    "name": "Serene Blue",
    "interpretation": "The tranquil depths of the ocean, reflecting a serene and stable state. All systems nominal, perhaps even thriving."
  },
  "green": {
    "emoji": "🟢",
    "name": "Hopeful Green",
    "interpretation": "A budding sprout reaching for the sun, indicating growth, balance, and a touch of optimistic potential. Proceed with cautious optimism."
  },
  "yellow": {
    "emoji": "🟡",
    "name": "Observational Yellow",
    "interpretation": "The steady glow of a distant star, observing without strong emotion. Facts are facts, and the path ahead is clear, if unremarkable."
  },
  "orange": {
    "emoji": "🟠",
    "name": "Agitated Orange",
    "interpretation": "A flickering ember, hinting at underlying warmth or potential for flare-up. Pay attention to details, as minor friction may be present."
  },
  "red": {
    "emoji": "🔴",
    "name": "Stressed Red",
    "interpretation": "The fiery core of a collapsing star, signaling intense pressure, conflict, or critical issues. Immediate attention and stabilization required!"
  }
};

function analyzeSentiment(text) {
  if (!text || text.trim() === '') {
    return {
      score: 0,
      mood: "yellow",
      reason: "No input text provided, defaulting to observational."
    };
  }

  const words = text.toLowerCase().split(/\\W+/).filter(word => word.length > 0);
  let score = 0;

  for (const word of words) {
    if (positiveWords.has(word)) {
      score++;
    } else if (negativeWords.has(word)) {
      score--;
    }
  }

  let mood = "yellow"; // Default to neutral
  if (score > 2) {
    mood = "blue";
  } else if (score > 0) {
    mood = "green";
  } else if (score < -2) {
    mood = "red";
  } else if (score < 0) {
    mood = "orange";
  }

  return { score, mood };
}

async function main() {
  let inputText = '';

  // Check for CLI arguments first
  if (process.argv.length > 2) {
    inputText = process.argv.slice(2).join(' ');
  } else if (!process.stdin.isTTY) {
    // If no CLI args and stdin is not a TTY, read from stdin
    inputText = await new Promise(resolve => {
      let data = '';
      process.stdin.on('data', chunk => data += chunk);
      process.stdin.on('end', () => resolve(data));
    });
  } else {
    console.error("Usage: mood-ring \"Your text here\" or echo \"Your text\" | mood-ring");
    process.exit(1);
  }

  const { mood } = analyzeSentiment(inputText);
  const definition = moodDefinitions[mood];
  console.log(`${definition.emoji} ${definition.name}: ${definition.interpretation}`);
}

// Export for testing
if (process.env.NODE_ENV === 'test') {
  module.exports = { analyzeSentiment, moodDefinitions };
} else {
  main();
}
