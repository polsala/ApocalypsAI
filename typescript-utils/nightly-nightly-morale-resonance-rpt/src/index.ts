import { addMoodEntry, getMoodEntries } from './data';
import { MoodEntry, MoodFactor, EmotionalReport } from './types';

// Helper to parse CLI arguments
function parseArgs(args: string[]): { command: string, options: Record<string, string | boolean> } {
  const command = args[0];
  const options: Record<string, string | boolean> = {};
  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const [key, value] = arg.substring(2).split('=');
      options[key] = value || true;
    }
  }
  return { command, options };
}

// Function to add a mood entry
export function handleAddEntry(moodScore: number, factors: string[], notes?: string): MoodEntry {
  if (moodScore < 1 || moodScore > 5 || !Number.isInteger(moodScore)) {
    throw new Error('Mood score must be an integer between 1 and 5.');
  }
  const validFactors: MoodFactor[] = factors.filter(f => ['food', 'shelter', 'social', 'weather', 'safety', 'anomaly', 'resource_gain', 'resource_loss'].includes(f)) as MoodFactor[];
  if (validFactors.length !== factors.length) {
    console.warn('Warning: Some provided factors were invalid and ignored.');
  }

  const newEntry: MoodEntry = {
    timestamp: Date.now(),
    moodScore: moodScore as MoodEntry['moodScore'],
    factors: validFactors,
    notes,
  };
  addMoodEntry(newEntry);
  return newEntry;
}

// Function to generate the emotional report
export function generateEmotionalReport(targetDate: Date = new Date()): EmotionalReport {
  const allEntries = getMoodEntries();
  const targetDateString = targetDate.toISOString().split('T')[0];

  const entriesForTargetDay = allEntries.filter(entry => {
    const entryDate = new Date(entry.timestamp);
    return entryDate.toISOString().split('T')[0] === targetDateString;
  });

  if (entriesForTargetDay.length === 0) {
    return {
      date: targetDateString,
      averageMood: 0,
      moodTrend: 'stable',
      dominantPositiveFactors: [],
      dominantNegativeFactors: [],
      recommendation: 'No mood data for this day. Encourage sharing!',
    };
  }

  const totalMood = entriesForTargetDay.reduce((sum, entry) => sum + entry.moodScore, 0);
  const averageMood = totalMood / entriesForTargetDay.length;

  const factorCounts: Record<MoodFactor, { positive: number, negative: number }> = {
    food: { positive: 0, negative: 0 },
    shelter: { positive: 0, negative: 0 },
    social: { positive: 0, negative: 0 },
    weather: { positive: 0, negative: 0 },
    safety: { positive: 0, negative: 0 },
    anomaly: { positive: 0, negative: 0 },
    resource_gain: { positive: 0, negative: 0 },
    resource_loss: { positive: 0, negative: 0 },
  };

  entriesForTargetDay.forEach(entry => {
    entry.factors.forEach(factor => {
      if (entry.moodScore >= 3) { // Consider 3, 4, 5 as positive/neutral
        factorCounts[factor].positive++;
      } else { // Consider 1, 2 as negative
        factorCounts[factor].negative++;
      }
    });
  });

  const dominantPositiveFactors: MoodFactor[] = [];
  const dominantNegativeFactors: MoodFactor[] = [];

  let maxPositiveCount = 0;
  let maxNegativeCount = 0;

  for (const factor in factorCounts) {
    const typedFactor = factor as MoodFactor;
    if (factorCounts[typedFactor].positive > maxPositiveCount) {
      maxPositiveCount = factorCounts[typedFactor].positive;
      dominantPositiveFactors.splice(0, dominantPositiveFactors.length, typedFactor); // Clear and add
    } else if (factorCounts[typedFactor].positive === maxPositiveCount && maxPositiveCount > 0) {
      dominantPositiveFactors.push(typedFactor);
    }

    if (factorCounts[typedFactor].negative > maxNegativeCount) {
      maxNegativeCount = factorCounts[typedFactor].negative;
      dominantNegativeFactors.splice(0, dominantNegativeFactors.length, typedFactor); // Clear and add
    } else if (factorCounts[typedFactor].negative === maxNegativeCount && maxNegativeCount > 0) {
      dominantNegativeFactors.push(typedFactor);
    }
  }

  // Determine mood trend (simple: compare with previous day's average if available)
  let moodTrend: EmotionalReport['moodTrend'] = 'stable';
  const previousDay = new Date(targetDate);
  previousDay.setDate(targetDate.getDate() - 1);
  const previousDayString = previousDay.toISOString().split('T')[0];
  const entriesForPreviousDay = allEntries.filter(entry => {
    const entryDate = new Date(entry.timestamp);
    return entryDate.toISOString().split('T')[0] === previousDayString;
  });

  if (entriesForPreviousDay.length > 0) {
    const prevDayAvgMood = entriesForPreviousDay.reduce((sum, entry) => sum + entry.moodScore, 0) / entriesForPreviousDay.length;
    if (averageMood > prevDayAvgMood) {
      moodTrend = 'rising';
    } else if (averageMood < prevDayAvgMood) {
      moodTrend = 'falling';
    }
  }

  let recommendation = 'Maintain vigilance, survivors.';
  if (averageMood >= 4) {
    recommendation = 'Morale is high! Consider a community gathering or a small celebration.';
  } else if (averageMood >= 3) {
    recommendation = 'Morale is stable. Focus on routine tasks and reinforce positive interactions.';
  } else if (averageMood >= 2) {
    recommendation = 'Morale is low. Address dominant negative factors urgently. Small victories are crucial.';
  } else { // averageMood < 2
    recommendation = 'Morale is critical. Prioritize immediate needs: safety, food, and emotional support.';
  }

  return {
    date: targetDateString,
    averageMood: parseFloat(averageMood.toFixed(2)),
    moodTrend,
    dominantPositiveFactors,
    dominantNegativeFactors,
    recommendation,
  };
}

// Main CLI execution
if (require.main === module) {
  const { command, options } = parseArgs(process.argv.slice(2));

  try {
    switch (command) {
      case 'add':
        const score = parseInt(options.score as string, 10);
        const factors = (options.factors as string || '').split(',').map(f => f.trim()).filter(Boolean);
        const notes = options.notes as string;
        if (isNaN(score)) {
          console.error('Error: --score is required and must be a number.');
          process.exit(1);
        }
        handleAddEntry(score, factors, notes);
        console.log('Mood entry added successfully.');
        break;
      case 'report':
        const reportDateStr = options.date as string;
        const reportDate = reportDateStr ? new Date(reportDateStr) : new Date();
        if (isNaN(reportDate.getTime())) {
          console.error('Error: Invalid date format for --date. Use YYYY-MM-DD.');
          process.exit(1);
        }
        const report = generateEmotionalReport(reportDate);
        console.log('\n--- Emotional Resonance Report ---');
        console.log(`Date: ${report.date}`);
        console.log(`Average Mood: ${report.averageMood} (1=Dire, 5=Radiant)`);
        console.log(`Mood Trend: ${report.moodTrend}`);
        if (report.dominantPositiveFactors.length > 0) {
          console.log(`Dominant Positive Factors: ${report.dominantPositiveFactors.join(', ')}`);
        }
        if (report.dominantNegativeFactors.length > 0) {
          console.log(`Dominant Negative Factors: ${report.dominantNegativeFactors.join(', ')}`);
        }
        console.log(`Recommendation: ${report.recommendation}`);
        console.log('----------------------------------\n');
        break;
      case 'help':
      default:
        console.log(`\nUsage:\n  npm run start add -- --score=<1-5> --factors=<comma-separated-list> [--notes="<text>"]\n  npm run start report [--date=<YYYY-MM-DD>]\n  npm run start help\n\nExamples:\n  npm run start add -- --score=4 --factors=food,social --notes="Found a stash of canned beans!"\n  npm run start report --date=2023-10-27\n  npm run start report\n        `);
        break;
    }
  } catch (error: any) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}
