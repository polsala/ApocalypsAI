const fs = require('fs');
const path = require('path');

const RELICS_DB_PATH = path.join(__dirname, 'relics.json');

function loadRelics() {
  try {
    const data = fs.readFileSync(RELICS_DB_PATH, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error('Error loading relics database:', error.message);
    return [];
  }
}

function findBestMatch(description, relics) {
  const lowerDescription = description.toLowerCase();
  let bestMatch = null;
  let maxScore = 0;

  for (const relic of relics) {
    let score = 0;
    for (const keyword of relic.keywords) {
      if (lowerDescription.includes(keyword)) {
        score++;
      }
    }
    if (score > maxScore) {
      maxScore = score;
      bestMatch = relic;
    }
  }
  return bestMatch;
}

function getRelicInfo(description) {
  const relics = loadRelics();
  const bestMatch = findBestMatch(description, relics);

  if (bestMatch) {
    return {
      name: bestMatch.name,
      purpose: bestMatch.purpose,
      repurpose: bestMatch.repurpose,
      survival_rating: bestMatch.survival_rating
    };
  } else {
    return {
      name: 'Unknown Anomaly',
      purpose: 'Lost to the mists of time, or perhaps never had one.',
      repurpose: 'Use as a paperweight, a conversation starter, or a very slow-acting poison (handle with care).',
      survival_rating: 'Unpredictable'
    };
  }
}

// CLI execution
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log('Usage: node src/index.js \"<item description>\"');
    process.exit(1);
  }
  const itemDescription = args.join(' ');
  const info = getRelicInfo(itemDescription);
  console.log(`Relic Identified: ${info.name}`);
  console.log(`Original Purpose: ${info.purpose}`);
  console.log(`Repurposing Idea: ${info.repurpose}`);
  console.log(`Survival Rating: ${info.survival_rating}`);
}

// Export for testing
module.exports = { getRelicInfo, loadRelics, findBestMatch };
