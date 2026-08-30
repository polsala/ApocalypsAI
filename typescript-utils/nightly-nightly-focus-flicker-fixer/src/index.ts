import { microQuests, distractionDetoxes, Mood, MicroQuest, DistractionDetox } from './quests';

function getRandomElement<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

function getQuest(mood: Mood = 'any'): MicroQuest {
  const availableQuests = microQuests.filter(q => q.moods.includes(mood) || q.moods.includes('any'));
  return getRandomElement(availableQuests.length > 0 ? availableQuests : microQuests); // Fallback to all if no specific mood quests
}

function getDetox(): DistractionDetox {
  return getRandomElement(distractionDetoxes);
}

function displayQuest(quest: MicroQuest): void {
  console.log(`\n✨ Micro-Quest Initiated: ${quest.title} ✨`);
  console.log(`-------------------------------------------------`);
  console.log(`Objective: ${quest.description}`);
  console.log(`Estimated Duration: ${quest.durationMinutes} minutes`);
  console.log(`-------------------------------------------------\n`);
}

function displayDetox(detox: DistractionDetox): void {
  console.log(`\n🚫 Distraction-Detox Protocol: ${detox.title} 🚫`);
  console.log(`-------------------------------------------------`);
  console.log(`Action: ${detox.description}`);
  console.log(`Recommended Duration: ${detox.durationMinutes} minutes`);
  console.log(`-------------------------------------------------\n`);
}

function parseArgs(args: string[]): { type: 'quest' | 'detox'; mood?: Mood } {
  const typeArg = args.find(arg => arg === '--quest' || arg === '--detox');
  const moodArgIndex = args.findIndex(arg => arg === '--mood');
  let mood: Mood | undefined;

  if (moodArgIndex !== -1 && args[moodArgIndex + 1]) {
    const potentialMood = args[moodArgIndex + 1].toLowerCase();
    if (['low', 'medium', 'high'].includes(potentialMood)) {
      mood = potentialMood as Mood;
    } else {
      console.warn(`Invalid mood: "${potentialMood}". Using 'any'. Valid moods are 'low', 'medium', 'high'.`);
      mood = 'any';
    }
  }

  if (typeArg === '--detox') {
    return { type: 'detox' };
  } else {
    return { type: 'quest', mood: mood || 'any' };
  }
}

// Main execution
if (require.main === module) {
  const { type, mood } = parseArgs(process.argv.slice(2));

  if (type === 'detox') {
    displayDetox(getDetox());
  } else {
    displayQuest(getQuest(mood));
  }
}

// Export for testing
export { getQuest, getDetox, displayQuest, displayDetox, parseArgs, getRandomElement };
