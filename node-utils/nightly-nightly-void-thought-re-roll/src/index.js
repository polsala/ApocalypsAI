const readline = require('readline');
const chalk = require('chalk');
const { reRollThought } = require('./reRoller');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function askThought() {
  rl.question(chalk.hex('#8A2BE2')('Enter your thought to cast into the void: ') + chalk.reset(), (thought) => {
    if (!thought.trim()) {
      console.log(chalk.red('The void requires a thought, however small.'));
      askThought();
      return;
    }

    console.log(chalk.hex('#FFA500')('Casting your thought into the void...'));
    const reRolledThought = reRollThought(thought);
    console.log(chalk.hex('#00FFFF')(`The void says: ${reRolledThought}`));

    rl.question(chalk.hex('#8A2BE2')('\nCast another thought? (y/N): ') + chalk.reset(), (answer) => {
      if (answer.toLowerCase() === 'y') {
        askThought();
      } else {
        console.log(chalk.hex('#90EE90')('The void wishes you peace. Farewell for now.'));
        rl.close();
      }
    });
  });
}

console.log(chalk.hex('#FF69B4')('\nWelcome to the Nightly Void Thought Re-Roller!'));
console.log(chalk.hex('#FF69B4')('Cast your worries and receive cosmic perspectives.'));
askThought();
