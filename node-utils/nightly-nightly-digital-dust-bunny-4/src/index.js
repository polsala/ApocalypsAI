#!/usr/bin/env node

const { Command } = require('commander');
const chalk = require('chalk');
const { scan } = require('./fileScanner');
const fs = require('fs');
const path = require('path');

const program = new Command();

program
    .name('digital-dust-bunny')
    .description(chalk.cyan('A whimsical utility to sweep away your digital dust bunnies (old files)!'))
    .version('1.0.0');

program.argument('<path>', 'The root directory to scan for old files.')
    .option('-a, --age <days>', 'Minimum age in days for a file to be considered old (default: 90)', '90')
    .option('-d, --dry-run', 'Perform a dry run without making any changes.')
    .option('-e, --exclude <patterns...>', 'Comma-separated regex patterns to exclude files/directories (e.g., "node_modules,*.log")', [])
    .option('-v, --verbose', 'Show more detailed output.')
    .action(async (scanPath, options) => {
        const minAgeDays = parseInt(options.age, 10);
        const dryRun = options.dryRun;
        // Split comma-separated patterns if they come as a single string, and flatten the array
        const excludePatterns = options.exclude.flatMap(pattern => pattern.split(',').map(p => p.trim()).filter(p => p.length > 0));
        const verbose = options.verbose;

        if (isNaN(minAgeDays) || minAgeDays <= 0) {
            console.error(chalk.red('Error: --age must be a positive number.'));
            process.exit(1);
        }

        console.log(chalk.yellow(`\nSweeping for digital dust bunnies in: ${chalk.bold(scanPath)}`));
        console.log(chalk.yellow(`Looking for files older than: ${chalk.bold(minAgeDays)} days`));
        if (excludePatterns.length > 0) {
            console.log(chalk.yellow(`Excluding paths matching: ${chalk.bold(excludePatterns.join(', '))}`));
        }
        if (dryRun) {
            console.log(chalk.blue('Performing a DRY RUN. No files will be moved or deleted.'));
        }
        console.log(chalk.gray('----------------------------------------------------'));

        const oldFiles = scan(scanPath, minAgeDays, excludePatterns);

        if (oldFiles.length === 0) {
            console.log(chalk.green('\nNo digital dust bunnies found! Your digital space is sparkling clean. ✨'));
        } else {
            console.log(chalk.red(`\nFound ${oldFiles.length} digital dust bunnies:`));
            oldFiles.forEach(file => {
                console.log(`  ${chalk.white(file.path)} (Modified: ${chalk.magenta(file.mtime.toLocaleDateString())}, Age: ${chalk.cyan(file.ageDays)} days)`);
            });

            if (!dryRun) {
                console.log(chalk.yellow('\nConsider moving these files to an archive or deleting them.'));
            }
        }
        console.log(chalk.gray('----------------------------------------------------'));
    });

program.parse(process.argv);
