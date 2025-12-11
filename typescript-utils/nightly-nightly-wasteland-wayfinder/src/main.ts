import { Command } from 'commander';
import { optimizeRoute } from './routeOptimizer';

const program = new Command();

program
  .name('wayfinder')
  .version('1.0.0')
  .description('Post-apocalyptic route optimizer')
  .option('--start <location>', 'Starting location')
  .option('--targets <items...>', 'Priority items to collect')
  .option('--avoid <zones...>', 'Dangerous areas to avoid')
  .action((options) => {
    if (!options.start || !options.targets) {
      program.outputHelp();
      return;
    }

    const route = optimizeRoute(options.start, options.targets, options.avoid);
    console.log(`\n🧭 OPTIMIZED ROUTE:\n${route}`);
  });

program.parse();
