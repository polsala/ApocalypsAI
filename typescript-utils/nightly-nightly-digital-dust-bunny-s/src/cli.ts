import { Command } from 'commander';
import { DigitalDustBunnySweeper } from './index';
import { DustBunnyConfig } from './types';
import * as path from 'path';

const program = new Command();

program
  .name('nightly-digital-dust-bunny-sweeper')
  .description('A whimsical CLI tool to sweep away digital dust bunnies (old or pattern-matching files).')
  .version('1.0.0');

program
  .argument('<directory>', 'The target directory to sweep for digital dust.')
  .option('-a, --age <days>', 'Minimum age in days for a file to be considered dusty (default: 90)', '90')
  .option('-p, --patterns <list>', 'Comma-separated list of filename patterns (e.g., temp,backup,old)', 'temp,backup,copy,old')
  .option('-r, --recursive', 'Scan directories recursively (default: false)', false)
  .option('-f, --format <type>', 'Output format: "json" or "text" (default: text)', 'text')
  .option('-s, --min-score <score>', 'Minimum dust score for a file to be reported (default: 1)', '1')
  .action(async (directory, options) => {
    const config: DustBunnyConfig = {
      targetDir: path.resolve(directory),
      ageThresholdDays: parseInt(options.age, 10),
      dustPatterns: options.patterns.split(',').map((p: string) => p.trim()).filter(Boolean),
      recursive: options.recursive,
      outputFormat: options.format,
      minDustScore: parseInt(options.minScore, 10),
    };

    if (isNaN(config.ageThresholdDays) || config.ageThresholdDays < 0) {
      console.error('Error: --age must be a non-negative number.');
      process.exit(1);
    }
    if (isNaN(config.minDustScore) || config.minDustScore < 0) {
      console.error('Error: --min-score must be a non-negative number.');
      process.exit(1);
    }
    if (!['json', 'text'].includes(config.outputFormat)) {
      console.error('Error: --format must be "json" or "text".');
      process.exit(1);
    }

    const sweeper = new DigitalDustBunnySweeper(config);
    const dustyFiles = await sweeper.sweep();

    if (dustyFiles.length === 0) {
      console.log('✨ Your digital space is sparkling clean! No dust bunnies found.');
      return;
    }

    if (config.outputFormat === 'json') {
      console.log(JSON.stringify(dustyFiles, null, 2));
    } else {
      console.log(`🧹 Found ${dustyFiles.length} digital dust bunnies in '${config.targetDir}':\n`);
      dustyFiles.forEach(file => {
        console.log(`  - Path: ${file.path}`);
        console.log(`    Age: ${file.ageDays} days old`);
        console.log(`    Dust Score: ${file.dustScore}`);
        console.log(`    Suggestion: ${file.suggestion}\n`);
      });
      console.log('Consider reviewing these files for archiving or deletion to keep your digital realm tidy!');
    }
  });

program.parse(process.argv);
