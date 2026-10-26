/*
 * nightly-emoji-mood-analyzer
 *
 * Simple sentiment → emoji mapper.
 * No external dependencies – pure JavaScript.
 */

const POSITIVE_WORDS = [
  'love', 'happy', 'joy', 'awesome', 'great', 'good', 'fantastic',
  'wonderful', 'delight', 'sunny', 'pleased', 'cheer', 'glad'
];
const NEGATIVE_WORDS = [
  'hate', 'sad', 'bad', 'terrible', 'awful', 'depress', 'angry',
  'mad', 'gloom', 'rainy', 'unhappy', 'sorrow', 'pain'
];

/**
 * Analyze the mood of a given text and return an emoji.
 * @param {string} text - Input text to analyze.
 * @returns {string} Emoji representing the mood.
 */
function analyzeMood(text) {
  if (typeof text !== 'string') return '😐';
  const lower = text.toLowerCase();
  let pos = 0;
  let neg = 0;
  for (const w of POSITIVE_WORDS) {
    if (lower.includes(w)) pos++;
  }
  for (const w of NEGATIVE_WORDS) {
    if (lower.includes(w)) neg++;
  }
  if (pos > neg) return '😊';
  if (neg > pos) return '😢';
  return '😐';
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  const getInput = () => {
    return new Promise((resolve) => {
      if (args.length > 0) {
        resolve(args.join(' '));
      } else {
        // Read from stdin
        let data = '';
        process.stdin.setEncoding('utf8');
        process.stdin.on('data', chunk => data += chunk);
        process.stdin.on('end', () => resolve(data.trim()));
      }
    });
  };

  getInput().then(input => {
    const emoji = analyzeMood(input);
    console.log(emoji);
  });
}

module.exports = { analyzeMood };
