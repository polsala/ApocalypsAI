import { Command } from 'commander';
import chalk from 'chalk';
import { TemporalResidueScanner } from './scanner';
import { ScanOptions } from './types';
import * as path from 'path';

const program = new Command();

program
  .name('nightly-temporal-residue-scanner')
  .description('Scans project directories for forgotten or unused files and folders, identifying "temporal residue" based on age and patterns.')
  .version('1.0.0');

program
  .argument('[path]', 'Path to the directory to scan', '.')
  .option('-a, --min-age <days>', 'Minimum age in days for a file/directory to be considered residue', '90')
  .option('-i, --ignore <patterns...>', 'Patterns to ignore (e.g., node_modules, .git)', ['node_modules', '.git', 'dist', 'build'])
  .action(async (scanPath, options) => {
    const resolvedPath = path.resolve(scanPath);
    const minAgeDays = parseInt(options.minAge, 10);

    if (isNaN(minAgeDays) || minAgeDays <= 0) {
      console.error(chalk.red('Error: --min-age must be a positive number.'));
      process.exit(1);
    }

    const scanOptions: ScanOptions = {
      path: resolvedPath,
      minAgeDays: minAgeDays,
      ignorePatterns: options.ignore,
      includePatterns: [] // Future expansion: specific patterns to *look for* as residue
    };

    console.log(chalk.blue(`\nScanning for temporal residue in: ${chalk.cyan(scanOptions.path)}`));
    console.log(chalk.blue(`Minimum age for residue: ${chalk.cyan(scanOptions.minAgeDays)} days`));
    console.log(chalk.blue(`Ignoring patterns: ${chalk.cyan(scanOptions.ignorePatterns.join(', '))}\n`));

    try {
      const scanner = new TemporalResidueScanner(scanOptions);
      const residues = await scanner.scan();

      if (residues.length === 0) {
        console.log(chalk.green('No temporal residue detected. Your project is pristine! ✨'));
      } else {
        console.log(chalk.yellow(`Temporal residue detected (${residues.length} items):`));
        residues.forEach(item => {
          const age = Math.floor((new Date().getTime() - item.lastModified.getTime()) / (1000 * 60 * 60 * 24));
          console.log(
            `  ${chalk.red(item.type.toUpperCase())}: ${chalk.white(item.path)} ` +
            chalk.gray(`(Last modified: ${item.lastModified.toLocaleDateString()}, Age: ${age} days)`)
          );
          console.log(chalk.gray(`    Reason: ${item.reason}`));
        });
        console.log(chalk.yellow('\nConsider reviewing these items for archiving or removal.'));
      }
    } catch (error: any) {
      console.error(chalk.red(`\nAn error occurred during scanning: ${error.message}`));
      process.exit(1);
    }
  });

program.parse(process.argv);
