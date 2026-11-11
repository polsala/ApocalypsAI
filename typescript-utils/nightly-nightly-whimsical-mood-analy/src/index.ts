import * as fs from 'fs';

enum Mood {
  GloomDoom = 'GloomDoom',
  HopeSpark = 'HopeSpark',
  ChaosChuckle = 'ChaosChuckle',
  VoidZen = 'VoidZen',
  Neutral = 'Neutral',
  Mixed = 'Mixed',
}

interface MoodAnalysisResult {
  totalLines: number;
  totalWords: number;
  moodCounts: Record<Mood, number>;
  dominantMood: Mood | 'Mixed' | 'Neutral';
  moodDistribution: Record<Mood, number>;
}

const MOOD_KEYWORDS: Record<Mood, string[]> = {
  [Mood.GloomDoom]: ['apocalypse', 'doom', 'despair', 'ruin', 'collapse', 'bleak', 'dread', 'end', 'destruction', 'decay'],
  [Mood.HopeSpark]: ['hope', 'future', 'build', 'grow', 'thrive', 'light', 'dawn', 'new beginning', 'progress', 'flourish'],
  [Mood.ChaosChuckle]: ['chaos', 'whimsy', 'giggle', 'mischief', 'random', 'unpredictable', 'quirk', 'absurd', 'playful', 'disorder'],
  [Mood.VoidZen]: ['void', 'zen', 'calm', 'peace', 'stillness', 'meditate', 'empty', 'serene', 'tranquil', 'nothingness'],
  [Mood.Neutral]: [], // Not used for keyword matching, but for result classification
  [Mood.Mixed]: [] // Not used for keyword matching, but for result classification
};

/**
 * Analyzes a given text string and determines its whimsical mood distribution.
 * @param text The input text to analyze.
 * @returns A MoodAnalysisResult object.
 */
export function analyzeText(text: string): MoodAnalysisResult {
  const lines = text.split(/\r?\n/).filter(line => line.trim() !== '');
  const words = text.toLowerCase().match(/\b\w+\b/g) || [];

  const moodCounts: Record<Mood, number> = {
    [Mood.GloomDoom]: 0,
    [Mood.HopeSpark]: 0,
    [Mood.ChaosChuckle]: 0,
    [Mood.VoidZen]: 0,
    [Mood.Neutral]: 0, // Initialize, but won't be incremented by keywords
    [Mood.Mixed]: 0 // Initialize, but won't be incremented by keywords
  };

  for (const mood of Object.values(Mood)) {
    if (mood === Mood.Neutral || mood === Mood.Mixed) continue;
    for (const keyword of MOOD_KEYWORDS[mood]) {
      const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
      const matches = text.toLowerCase().match(regex);
      if (matches) {
        moodCounts[mood] += matches.length;
      }
    }
  }

  let totalMoodScore = 0;
  for (const mood of Object.values(Mood)) {
    if (mood === Mood.Neutral || mood === Mood.Mixed) continue;
    totalMoodScore += moodCounts[mood];
  }

  const moodDistribution: Record<Mood, number> = {
    [Mood.GloomDoom]: 0,
    [Mood.HopeSpark]: 0,
    [Mood.ChaosChuckle]: 0,
    [Mood.VoidZen]: 0,
    [Mood.Neutral]: 0,
    [Mood.Mixed]: 0
  };

  if (totalMoodScore > 0) {
    for (const mood of Object.values(Mood)) {
      if (mood === Mood.Neutral || mood === Mood.Mixed) continue;
      moodDistribution[mood] = moodCounts[mood] / totalMoodScore;
    }
  }

  let dominantMood: Mood | 'Mixed' | 'Neutral' = Mood.Neutral;
  let maxCount = 0;
  let dominantMoodsFound: Mood[] = [];

  for (const mood of Object.values(Mood)) {
    if (mood === Mood.Neutral || mood === Mood.Mixed) continue;
    if (moodCounts[mood] > maxCount) {
      maxCount = moodCounts[mood];
      dominantMoodsFound = [mood];
    } else if (moodCounts[mood] > 0 && moodCounts[mood] === maxCount) {
      dominantMoodsFound.push(mood);
    }
  }

  if (dominantMoodsFound.length === 0) {
    dominantMood = Mood.Neutral;
  } else if (dominantMoodsFound.length > 1) {
    dominantMood = Mood.Mixed;
  } else {
    dominantMood = dominantMoodsFound[0];
  }

  return {
    totalLines: lines.length,
    totalWords: words.length,
    moodCounts,
    dominantMood,
    moodDistribution,
  };
}

async function main() {
  let inputContent: string = '';

  const fileArgIndex = process.argv.indexOf('--file');
  if (fileArgIndex > -1 && process.argv[fileArgIndex + 1]) {
    const filePath = process.argv[fileArgIndex + 1];
    try {
      inputContent = fs.readFileSync(filePath, 'utf8');
    } catch (error) {
      console.error(`Error reading file ${filePath}:`, error instanceof Error ? error.message : String(error));
      process.exit(1);
    }
  } else if (!process.stdin.isTTY) {
    // Read from stdin if not a TTY (i.e., piped input)
    inputContent = await new Promise<string>((resolve) => {
      let data = '';
      process.stdin.on('data', (chunk) => (data += chunk));
      process.stdin.on('end', () => resolve(data));
      process.stdin.on('error', (err) => {
        console.error('Error reading from stdin:', err.message);
        process.exit(1);
      });
    });
  } else {
    console.error('Usage: node dist/index.js --file <path> OR cat <file> | node dist/index.js');
    process.exit(1);
  }

  const result = analyzeText(inputContent);
  console.log(JSON.stringify(result, null, 2));
}

if (require.main === module) {
  main();
}
