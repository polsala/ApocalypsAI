import { Command } from 'commander';
import { CosmicCompass } from './index';
import * as chalk from 'chalk';
import * as path from 'path';

const program = new Command();

program
  .name('cosmic-compass')
  .description(chalk.magenta('Navigate your project\'s celestial bodies with the Cosmic Compass!'))
  .version('1.0.0');

program
  .argument('<path>', 'The stellar path (directory) to explore.')
  .option('-s, --search <keywords...>', 'Keywords to search for among the celestial bodies.')
  .action(async (targetPath, options) => {
    const absolutePath = path.resolve(targetPath);
    console.log(chalk.cyan(`\nInitiating Cosmic Scan of: ${chalk.yellow(absolutePath)}`));

    const compass = new CosmicCompass(absolutePath);
    try {
      await compass.buildAtlas();
      const atlas = compass.getAtlas();

      if (options.search && options.search.length > 0) {
        console.log(chalk.blue(`Searching for cosmic anomalies matching: ${chalk.yellow(options.search.join(', '))}`));
        const results = compass.searchAtlas(options.search);

        if (results.length === 0) {
          console.log(chalk.gray('No celestial bodies found matching your search criteria. The void is vast.'));
        } else {
          console.log(chalk.green(`\n${results.length} celestial bodies detected:`));
          results.forEach(result => {
            const typeIcon = result.celestialBody.type === 'file' ? '⭐' : '🌌';
            console.log(`  ${typeIcon} ${chalk.white(result.celestialBody.path)}`);
            result.matches.forEach(match => console.log(chalk.dim(`    - ${match}`)));
          });
        }
      } else {
        console.log(chalk.green(`\nCosmic Atlas built! ${Object.keys(atlas).length} celestial bodies mapped.`));
        console.log(chalk.gray('Use --search <keywords...> to find specific stellar phenomena.'));
      }
    } catch (error: any) {
      console.error(chalk.red(`\nCosmic disturbance detected: ${error.message}`));
      process.exit(1);
    }
  });

program.parse(process.argv);
