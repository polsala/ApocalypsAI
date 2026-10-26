#!/usr/bin/env node
const yargs = require('yargs');
const { hideBin } = require('yargs/helpers');
const { getSnackSuggestion } = require('./snackSuggester');

const argv = yargs(hideBin(process.argv))
  .command('$0 [mood]', 'Suggests a post-apocalyptic snack based on your mood.', (yargs) => {
    yargs.positional('mood', {
      describe: 'Your current mood (e.g., grumpy, energetic, contemplative)',
      type: 'string',
    });
  })
  .help()
  .alias('h', 'help')
  .argv;

async function run() {
  const mood = argv.mood;

  if (!mood) {
    console.log('Please specify your mood. Example: mood-snack grumpy');
    console.log('Run "mood-snack --help" for more options.');
    process.exit(1);
  }

  const suggestion = getSnackSuggestion(mood);
  console.log(`\nMood: ${mood}`);
  console.log(`Suggested Snack: ${suggestion.name}`);
  console.log(`Description: ${suggestion.description}\n`);
}

if (require.main === module) {
  run();
}

// Export for testing purposes
module.exports = { run };
