import { addEntry, loadMoraleData, clearEntries } from './data';
import { Mood, MoraleEntry } from './types';

const MOOD_VALUES: Record<Mood, number> = {
  "Gloomy as a Nuclear Winter": 1,
  "Anxious as a Scavenger": 2,
  "Neutral as a Deactivated Sentry": 3,
  "Hopeful as a Seedling": 4,
  "Radiant as a Supernova": 5,
};

function displayHelp() {
  console.log(`\nNightly Morale Monitor - Track your emotional resilience in the wasteland.\n\nUsage:\n  nmm add <mood> [notes]   - Log your current morale.\n                           Moods: ${Object.keys(MOOD_VALUES).join(', ')}\n  nmm list                 - Show all logged morale entries.\n  nmm report               - Generate a morale trend report.\n  nmm clear                - Erase all morale logs (requires confirmation).\n  nmm help                 - Display this help message.\n`);
}

function addMoraleEntry(moodStr: string, notes?: string) {
  const mood = moodStr as Mood;
  if (!Object.keys(MOOD_VALUES).includes(mood)) {
    console.error(`Error: Invalid mood "${moodStr}". Available moods: ${Object.keys(MOOD_VALUES).join(', ')}`);
    return;
  }

  const date = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
  const entry: MoraleEntry = { date, mood, notes };
  addEntry(entry);
  console.log(`Morale entry added for ${date}: ${mood}`);
}

function listMoraleEntries() {
  const data = loadMoraleData();
  if (data.entries.length === 0) {
    console.log("No morale entries logged yet. Stay strong, survivor!");
    return;
  }
  console.log("\n--- Morale Log ---");
  data.entries.forEach(entry => {
    console.log(`${entry.date} - ${entry.mood}${entry.notes ? ` (${entry.notes})` : ''}`);
  });
  console.log("------------------\n");
}

function generateMoraleReport() {
  const data = loadMoraleData();
  if (data.entries.length < 2) {
    console.log("Need at least two entries to generate a trend report. Keep logging, survivor!");
    return;
  }

  const sortedEntries = [...data.entries].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
  const moodScores = sortedEntries.map(entry => MOOD_VALUES[entry.mood]);

  const totalScore = moodScores.reduce((sum, score) => sum + score, 0);
  const averageScore = totalScore / moodScores.length;

  let trendMessage = "Morale is stable.";
  if (moodScores.length >= 2) {
    const lastTwo = moodScores.slice(-2);
    if (lastTwo[1] > lastTwo[0]) {
      trendMessage = "Morale is on the rise! Keep that spirit high!";
    } else if (lastTwo[1] < lastTwo[0]) {
      trendMessage = "Morale seems to be dipping. Remember to seek shelter and rest.";
    }
  }

  console.log("\n--- Morale Report ---");
  console.log(`Total entries: ${data.entries.length}`);
  console.log(`Average morale score: ${averageScore.toFixed(2)} (1=Gloomy, 5=Radiant)`);
  console.log(`Current trend: ${trendMessage}`);
  console.log("---------------------\n");
}

function confirmClearEntries() {
  const confirmArg = process.argv[3];
  if (confirmArg === '--force') {
    clearEntries();
    console.log("All morale entries have been purged. A fresh start, survivor!");
  } else {
    console.log("To clear all entries, run 'nmm clear --force'. This action cannot be undone!");
  }
}

function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'add':
      const mood = args[1];
      const notes = args.slice(2).join(' ');
      if (!mood) {
        console.error("Error: 'add' command requires a mood. See 'nmm help'.");
        return;
      }
      addMoraleEntry(mood, notes || undefined);
      break;
    case 'list':
      listMoraleEntries();
      break;
    case 'report':
      generateMoraleReport();
      break;
    case 'clear':
      confirmClearEntries();
      break;
    case 'help':
    case undefined: // No command given
      displayHelp();
      break;
    default:
      console.error(`Error: Unknown command "${command}". See 'nmm help'.`);
      break;
  }
}

main();
