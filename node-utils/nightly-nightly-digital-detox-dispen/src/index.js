#!/usr/bin/env node

const { Command } = require('commander');
const chalk = require('chalk');
const { generateActivity, generateMessage, activities, messageTemplates } = require('./detoxer');

const program = new Command();

program
  .name('detox-dispenser')
  .description(chalk.hex('#FFD700')('✨ Your guide to digital serenity in the post-digital age. ✨'))
  .version('1.0.0');

program.command('start')
  .description('Initiate a digital detox session.')
  .option('-d, --duration <string>', 'Specify the length of your detox (e.g., "2 hours", "until dawn").')
  .option('-r, --reason <string>', 'Provide a reason for your detox (e.g., "deep contemplation", "hunting for temporal anomalies").')
  .option('-p, --preferences <string>', 'Comma-separated list of activity preferences (e.g., "creative,physical").')
  .action((options) => {
    console.log(chalk.hex('#8A2BE2')('\n✨ Dispensing Digital Detox Potion... ✨\n'));

    const preferences = options.preferences ? options.preferences.split(',').map(p => p.trim()) : [];
    const activity = generateActivity(preferences);
    console.log(chalk.hex('#00FFFF')('Your recommended offline activity:\n'));
    console.log(chalk.white(`  ${activity}\n`));

    const message = generateMessage(options.duration, options.reason);
    console.log(chalk.hex('#00FFFF')('Your personalized disconnect message:\n'));
    console.log(chalk.white(`  "${message}"\n`));

    console.log(chalk.hex('#FFD700')('Remember to truly disconnect! May your detox be fruitful!\n'));
  });

program.command('activities')
  .description('List all available offline activity suggestions.')
  .action(() => {
    console.log(chalk.hex('#00FFFF')('\n🌌 Available Offline Activities: 🌌\n'));
    activities.forEach((activity, index) => {
      console.log(chalk.white(`  ${index + 1}. ${activity}`));
    });
    console.log('\n');
  });

program.command('messages')
  .description('List all available disconnect message templates.')
  .action(() => {
    console.log(chalk.hex('#00FFFF')('\n📜 Disconnect Message Templates: 📜\n'));
    messageTemplates.forEach((template, index) => {
      console.log(chalk.white(`  ${index + 1}. ${template.replace('{duration}', '<duration>').replace('{reason}', '<reason>')}`));
    });
    console.log('\n');
  });

program.parse(process.argv);
