import { Command } from 'commander';
import chalk from 'chalk';
import { generateQuest, getAllMoods } from './questGenerator';
import { Mood } from './types';

const program = new Command();

program
  .name('nightly-mood-quest-generator')
  .description('A whimsical CLI tool to banish decision paralysis by generating fun, actionable "quests" based on your current mood.')
  .version('1.0.0');

program
  .argument('<mood>', `Your current mood or energy level. Available moods: ${chalk.cyan(getAllMoods().join(', '))}`)
  .action((moodInput: string) => {
    const mood = moodInput.toLowerCase() as Mood;
    const availableMoods = getAllMoods();

    if (!availableMoods.includes(mood)) {
      console.error(chalk.red(`\nError: Invalid mood "${moodInput}".`));
      console.error(chalk.yellow(`Please choose from: ${chalk.cyan(availableMoods.join(', '))}\n`));
      process.exit(1);
    }

    const quest = generateQuest(mood);

    if (quest) {
      console.log(chalk.magenta('\n--- Your Whimsical Quest Awaits! ---'));
      console.log(chalk.green(`\nMood: ${chalk.bold(mood.charAt(0).toUpperCase() + mood.slice(1))}`));
      console.log(chalk.yellow(`Title: ${chalk.bold(quest.title)}`));
      console.log(`\n${quest.description}`);
      if (quest.actionableSteps && quest.actionableSteps.length > 0) {
        console.log(chalk.blue('\nYour First Steps:'));
        quest.actionableSteps.forEach((step, index) => {
          console.log(chalk.blue(`  ${index + 1}. ${step}`));
        });
      }
      console.log(chalk.magenta('\n------------------------------------\n'));
    } else {
      console.log(chalk.yellow(`\nNo specific quest found for "${mood}". Perhaps try a different mood or take a moment to reflect.\n`));
    }
  });

program.parse(process.argv);
