const chalk = require('chalk');

const cosmicEvents = [
  'Nebula Bloom',
  "Comet's Kiss",
  'Stardust Shower',
  'Galactic Whisper',
  'Supernova Echo',
  'Aurora Borealis Surge',
  'Lunar Tide Shift',
  'Solar Flare Gleam',
  'Asteroid Belt Dance',
  'Black Hole Hum'
];

function getRandomElement(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function getCosmicDirection() {
  const now = new Date();
  const hours = now.getHours();
  const minutes = now.getMinutes();
  const seconds = now.getSeconds();

  // Base direction based on time (a bit abstract and whimsical)
  let baseDirection;
  if (hours < 6) {
    baseDirection = 'the Dawn Horizon';
  } else if (hours < 12) {
    baseDirection = 'the Zenith Sky';
  } else if (hours < 18) {
    baseDirection = 'the Twilight Veil';
  } else {
    baseDirection = 'the Midnight Expanse';
  }

  const randomEvent = getRandomElement(cosmicEvents);

  // Combine base direction with event for a whimsical output
  const direction = `Towards the ${baseDirection}, guided by a ${randomEvent}!`;

  return direction;
}

function main() {
  const direction = getCosmicDirection();
  console.log(chalk.blue.bold('Your cosmic direction is:') + ' ' + chalk.yellow.italic(direction));
}

if (require.main === module) {
  main();
}

module.exports = { getCosmicDirection };
