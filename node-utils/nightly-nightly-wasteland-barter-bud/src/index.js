const yargs = require('yargs');
const chalk = require('chalk');
const path = require('path');
const { loadResources, saveResources, calculateResourceValue, suggestTrade } = require('./barterCalculator');

const RESOURCES_FILE = path.join(__dirname, 'resources.json');

yargs
  .command('list', 'List all available resources and their calculated values', () => {
    const resources = loadResources(RESOURCES_FILE);
    if (Object.keys(resources).length === 0) {
      console.log(chalk.yellow('No resources defined. Add some with the `add` command!'));
      return;
    }
    console.log(chalk.bold('\n--- Wasteland Resources & Values ---'));
    Object.values(resources).forEach(res => {
      const value = calculateResourceValue(res.name, resources);
      console.log(`  ${chalk.cyan(res.name)}: Base Value ${res.baseValue}, Scarcity ${res.scarcity}, Desirability ${res.desirability} => Calculated Value ${chalk.green(value.toFixed(2))}`);
    });
    console.log(chalk.bold('------------------------------------\n'));
  })
  .command('trade <haveResource> <haveAmount> <wantResource>', 'Suggest a fair amount of a resource you want for what you have.', (yargs) => {
    yargs
      .positional('haveResource', {
        describe: 'The resource you possess.',
        type: 'string'
      })
      .positional('haveAmount', {
        describe: 'The amount of the resource you possess.',
        type: 'number'
      })
      .positional('wantResource', {
        describe: 'The resource you desire.',
        type: 'string'
      });
  }, (argv) => {
    const resources = loadResources(RESOURCES_FILE);
    const { haveResource, haveAmount, wantResource } = argv;

    if (!resources[haveResource]) {
      console.error(chalk.red(`Error: Resource '${haveResource}' not found.`));
      return;
    }
    if (!resources[wantResource]) {
      console.error(chalk.red(`Error: Resource '${wantResource}' not found.`));
      return;
    }
    if (haveAmount <= 0) {
      console.error(chalk.red('Error: Amount must be greater than zero.'));
      return;
    }

    const suggestedAmount = suggestTrade(haveResource, wantResource, haveAmount, resources);
    console.log(`\nFor ${chalk.yellow(haveAmount)} units of ${chalk.cyan(haveResource)}, you should expect approximately ${chalk.green(suggestedAmount.toFixed(2))} units of ${chalk.magenta(wantResource)}.`);
    console.log(chalk.gray(' (Remember, these are just suggestions. The wasteland has its own rules!)'));
    console.log('\n');
  })
  .command('add <name> <baseValue> <scarcity> <desirability>', 'Add a new resource or update an existing one.', (yargs) => {
    yargs
      .positional('name', {
        describe: 'The name of the resource.',
        type: 'string'
      })
      .positional('baseValue', {
        describe: 'The base value of the resource.',
        type: 'number'
      })
      .positional('scarcity', {
        describe: 'Scarcity factor (e.g., 0.1 for very scarce, 2.0 for abundant).',n        type: 'number'
      })
      .positional('desirability', {
        describe: 'Desirability factor (e.g., 0.1 for undesirable, 2.0 for highly desired).',n        type: 'number'
      });
  }, (argv) => {
    const resources = loadResources(RESOURCES_FILE);
    const { name, baseValue, scarcity, desirability } = argv;

    if (baseValue <= 0 || scarcity <= 0 || desirability <= 0) {
      console.error(chalk.red('Error: baseValue, scarcity, and desirability must be positive numbers.'));
      return;
    }

    resources[name] = { name, baseValue, scarcity, desirability };
    saveResources(RESOURCES_FILE, resources);
    console.log(chalk.green(`Resource '${name}' ${argv._.includes('add') ? 'added' : 'updated'} successfully.`));
  })
  .command('remove <name>', 'Remove a resource.', (yargs) => {
    yargs
      .positional('name', {
        describe: 'The name of the resource to remove.',
        type: 'string'
      });
  }, (argv) => {
    const resources = loadResources(RESOURCES_FILE);
    const { name } = argv;

    if (!resources[name]) {
      console.error(chalk.red(`Error: Resource '${name}' not found.`));
      return;
    }

    delete resources[name];
    saveResources(RESOURCES_FILE, resources);
    console.log(chalk.green(`Resource '${name}' removed successfully.`));
  })
  .demandCommand(1, 'You need to specify a command.')
  .help()
  .alias('h', 'help')
  .version()
  .alias('v', 'version')
  .argv;
