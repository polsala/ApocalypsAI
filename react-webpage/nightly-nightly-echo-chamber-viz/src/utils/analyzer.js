/**
 * Analyzes a list of temporal events to identify recurring words (echoes).
 * @param {Array<Object>} events - An array of event objects, each with a 'message' string.
 * @param {Array<string>} [stopwords=[]] - An optional array of words to ignore.
 * @returns {Object} An object where keys are words and values are their frequencies.
 */
export function analyzeEchoes(events, stopwords = []) {
  const wordCounts = {};
  const lowerCaseStopwords = new Set(stopwords.map(word => word.toLowerCase()));

  events.forEach(event => {
    if (event.message) {
      // Simple tokenization: split by non-alphanumeric characters and convert to lowercase
      const words = event.message
        .toLowerCase()
        .split(/[^a-z0-9]+/)
        .filter(word => word.length > 2 && !lowerCaseStopwords.has(word)); // Ignore short words and stopwords

      words.forEach(word => {
        wordCounts[word] = (wordCounts[word] || 0) + 1;
      });
    }
  });

  return wordCounts;
}

// A default list of common English stopwords. Can be expanded.
export const defaultStopwords = [
  "the", "and", "is", "in", "it", "to", "of", "a", "for", "on", "with", "as", "at", "by",
  "from", "up", "out", "down", "about", "this", "that", "these", "those", "be", "have",
  "has", "had", "do", "does", "did", "will", "would", "can", "could", "should", "may",
  "might", "must", "are", "was", "were", "been", "being", "an", "or", "not", "but",
  "if", "then", "so", "no", "yes", "we", "you", "he", "she", "it", "they", "i", "me",
  "him", "her", "us", "them", "my", "your", "his", "its", "our", "their", "what", "when",
  "where", "why", "how", "which", "who", "whom", "here", "there", "when", "where", "why",
  "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such",
  "no", "nor", "only", "own", "same", "so", "than", "too", "very", "s", "t", "m", "d",
  "ll", "ve", "re", "just", "don", "shouldn", "now"
];
