import { Command } from 'commander';
import * as path from 'path';
import { scanDirectory } from './fileScanner';
import { formatReport } from './reporter';
import { Config, DustBunnyReport } from './types';
import chalk from 'chalk';

const program = new Command();

program
  .name('dust-bunny-sweeper')
  .description('Sweeps your project for stale files and directories (digital dust bunnies).')
  .version('1.0.0');

program
  .argument('<path>', 'The directory to scan for dust bunnies.')
  .option('-t, --threshold <days>', 'Minimum age in days for a file/directory to be considered a dust bunny (default: 90).', '90')
  .option('-i, --ignore <patterns...>', 'Space-separated regex patterns to ignore files/directories (e.g., "node_modules" ".git").', [])
  .option('-o, --output <format>', 'Output format: "text" (default) or "json".', 'text')
  .action(async (scanPath: string, options: { threshold: string; ignore: string[]; output: 'json' | 'text' }) => {
    const config: Config = {
      path: path.resolve(scanPath),
      thresholdDays: parseInt(options.threshold, 10),
      ignorePatterns: options.ignore,
      outputFormat: options.output,
    };

    if (isNaN(config.thresholdDays) || config.thresholdDays <= 0) {
      console.error(chalk.red('Error: Threshold must be a positive number of days.'));
      process.exit(1);
    }

    console.log(chalk.gray(`Scanning ${config.path} for digital dust bunnies older than ${config.thresholdDays} days...`));

    try {
      const dustBunnyFiles = await scanDirectory(
        config.path,
        config.thresholdDays,
        config.ignorePatterns
      );

      const report: DustBunnyReport = {
        scannedPath: config.path,
        thresholdDays: config.thresholdDays,
        ignoredPatterns: config.ignorePatterns,
        dustBunnyCount: dustBunnyFiles.length,
        dustBunnyFiles: dustBunnyFiles,
      };

      console.log(formatReport(report, config.outputFormat));
    } catch (error: any) {
      console.error(chalk.red(`Error sweeping dust bunnies: ${error.message}`));
      process.exit(1);
    }
  });

program.parse(process.argv);
