/**
 * Analyzes text for keyword occurrences across defined time slices.
 * @param {string} text The input text to analyze.
 * @param {string[]} keywords An array of keywords/phrases to search for.
 * @param {number} sliceSize The number of lines per 'time slice'.
 * @returns {Array<Object>} An array of objects, where each object represents a slice
 *                          and contains keyword counts for that slice.
 */
export function analyzeTextForEchoes(text, keywords, sliceSize = 100) {
  if (!text || keywords.length === 0) {
    return [];
  }

  const lines = text.split(/\r?\n/);
  const slices = [];
  let currentSlice = {};
  let lineCount = 0;

  const normalizeKeyword = (keyword) => keyword.toLowerCase();
  const normalizedKeywords = keywords.map(normalizeKeyword);

  for (const line of lines) {
    const normalizedLine = line.toLowerCase();
    lineCount++;

    for (const keyword of normalizedKeywords) {
      // Use word boundaries (\b) to match whole words only
      const occurrences = (normalizedLine.match(new RegExp(`\\b${keyword}\\b`, 'g')) || []).length;
      if (occurrences > 0) {
        currentSlice[keyword] = (currentSlice[keyword] || 0) + occurrences;
      }
    }

    if (lineCount % sliceSize === 0) {
      slices.push(currentSlice);
      currentSlice = {};
    }
  }

  // Add any remaining data in the last (incomplete) slice
  if (Object.keys(currentSlice).length > 0) {
    slices.push(currentSlice);
  }

  // Ensure all keywords are present in each slice object, even if count is 0
  return slices.map(slice => {
    const fullSlice = {};
    for (const keyword of normalizedKeywords) {
      fullSlice[keyword] = slice[keyword] || 0;
    }
    return fullSlice;
  });
}
