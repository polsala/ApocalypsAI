#!/usr/bin/env node

const chalk = require('chalk');

const options = process.argv.slice(2);

const whimsicalMessages = [
  (option) => `The ancient data streams hum a tune, and the frequency points to: ${chalk.bold(option)}. May your journey be swift.`,
  (option) => `A whisper from the void, carried on solar winds, reveals the path: ${chalk.bold(option)}. Embrace the unknown.`,
  (option) => `The flickering neon sign of destiny blinks, settling on: ${chalk.bold(option)}. Follow its glow.`,
  (option) => `Consulting the rusted gears of fate, the mechanism grinds to a halt at: ${chalk.bold(option)}. So it is written.`,
  (option) => `The last remaining digital oracle has spoken, its pixelated wisdom declares: ${chalk.bold(option)}. Proceed with caution, or abandon all hope.`,
  (option) => `Through the static of forgotten broadcasts, a clear signal emerges: ${chalk.bold(option)}. Tune in to your destiny.`,
  (option) => `The shifting sands of time reveal a momentary truth: ${chalk.bold(option)}. Seize the fleeting moment.`
];

function getProphecy(choices) {
  if (choices.length === 0) {
    return chalk.red('The Oracle finds no options to ponder. Its wisdom is silent.');
  }

  const randomIndex = Math.floor(Math.random() * choices.length);
  const chosenOption = choices[randomIndex];

  const messageIndex = Math.floor(Math.random() * whimsicalMessages.length);
  const messageGenerator = whimsicalMessages[messageIndex];

  return messageGenerator(chosenOption);
}

function run() {
  console.log(chalk.cyan.bold('\n--- The Oracle of Odds has spoken ---'));
  console.log(chalk.yellow(getProphecy(options)));
  console.log(chalk.cyan.bold('\n-------------------------------------\n'));
}

if (require.main === module) {
  run();
}

module.exports = { getProphecy, whimsicalMessages };
