const fs = require('fs');
const path = require('path');

const SUPPORTED_EXTENSIONS = new Set([
  '.txt', '.md', '.json', '.js', '.html', '.css', '.xml', '.log'
]);
const MAX_SNIPPET_LENGTH = 200;
const MIN_KEYWORD_LENGTH = 3;

/**
 * Extracts keywords from text content.
 * @param {string} text
 * @returns {string[]}
 */
function extractKeywords(text) {
  return text
    .toLowerCase()
    .split(/\W+/) // Split by non-alphanumeric characters
    .filter(word => word.length >= MIN_KEYWORD_LENGTH)
    .filter(word => !isStopWord(word)); // Basic stop word filtering
}

// A very basic set of stop words for demonstration
const STOP_WORDS = new Set([
  'the', 'and', 'is', 'in', 'it', 'to', 'of', 'for', 'on', 'with', 'as', 'at',
  'be', 'by', 'an', 'or', 'that', 'this', 'from', 'but', 'not', 'you', 'your',
  'we', 'our', 'they', 'their', 'he', 'she', 'him', 'her', 'its', 'was', 'were',
  'has', 'have', 'had', 'do', 'does', 'did', 'will', 'would', 'can', 'could',
  'should', 'may', 'might', 'must', 'are', 'if', 'then', 'than', 'when', 'where',
  'why', 'how', 'what', 'who', 'whom', 'which', 'there', 'here', 'all', 'any',
  'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
  'only', 'own', 'same', 'so', 'too', 'very', 's', 't', 'don', 'just', 'now'
]);

function isStopWord(word) {
  return STOP_WORDS.has(word);
}

/**
 * Scans a directory, extracts content, and creates an index.
 * @param {string} dirPath - The directory to scan.
 * @param {string} outputPath - The path to save the JSON index.
 * @returns {Promise<void>}
 */
async function indexDirectory(dirPath, outputPath = 'dust-bunny-index.json') {
  const index = [];
  const filesToProcess = [];

  function traverse(currentPath) {
    const entries = fs.readdirSync(currentPath, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(currentPath, entry.name);
      if (entry.isDirectory()) {
        traverse(fullPath);
      } else if (entry.isFile()) {
        const ext = path.extname(entry.name).toLowerCase();
        if (SUPPORTED_EXTENSIONS.has(ext)) {
          filesToProcess.push(fullPath);
        }
      }
    }
  }

  try {
    traverse(dirPath);

    for (const filePath of filesToProcess) {
      const content = fs.readFileSync(filePath, 'utf8');
      const snippet = content.substring(0, MAX_SNIPPET_LENGTH).replace(/\s+/g, ' ').trim();
      const keywords = [...new Set(extractKeywords(content))]; // Unique keywords

      index.push({
        path: filePath,
        snippet: snippet,
        keywords: keywords
      });
    }

    fs.writeFileSync(outputPath, JSON.stringify(index, null, 2), 'utf8');
    console.log(`Index created successfully at: ${outputPath}`);
    console.log(`Indexed ${index.length} files.`);
  } catch (error) {
    console.error(`Error indexing directory ${dirPath}:`, error.message);
    throw error;
  }
}

/**
 * Searches the loaded index for a given keyword.
 * @param {string} keyword - The keyword to search for.
 * @param {string} indexPath - The path to the JSON index file.
 * @returns {Promise<void>}
 */
async function searchIndex(keyword, indexPath = 'dust-bunny-index.json') {
  try {
    const indexContent = fs.readFileSync(indexPath, 'utf8');
    const index = JSON.parse(indexContent);
    const searchLower = keyword.toLowerCase();

    const results = index.filter(entry =>
      entry.keywords.some(k => k.includes(searchLower)) ||
      entry.path.toLowerCase().includes(searchLower) ||
      entry.snippet.toLowerCase().includes(searchLower)
    );

    if (results.length === 0) {
      console.log(`No results found for "${keyword}".`);
    } else {
      console.log(`Found ${results.length} results for "${keyword}":`);
      results.forEach(result => {
        console.log(`\nPath: ${result.path}`);
        console.log(`Snippet: ${result.snippet}...`);
        console.log(`Keywords: ${result.keywords.join(', ')}`);
      });
    }
  } catch (error) {
    console.error(`Error searching index at ${indexPath}:`, error.message);
    throw error;
  }
}

module.exports = {
  indexDirectory,
  searchIndex,
  extractKeywords, // Export for testing
  isStopWord // Export for testing
};
