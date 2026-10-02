import * as readline from 'readline';
import chalk from 'chalk';
import { classifyMood, Mood } from './moods';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function promptUser(question: string): Promise<string> {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer);
    });
  });
}

export async function runMoodRing() {
  console.log(chalk.magenta('\n✨ The Nightly Mood Ring hums softly... ✨'));
  const feeling = await promptUser(
    chalk.cyan('How are you feeling right now, wanderer of the digital wastes? (e.g., \'calm\', \'stressed\', \'happy\')\n> ')
  );

  const mood: Mood = classifyMood(feeling);

  console.log(`\nYour aura glows with ${mood.color(mood.type)}!`);
  console.log(chalk.white(`"${mood.insight}"`));

  rl.close();
}

if (require.main === module) {
  runMoodRing();
}
