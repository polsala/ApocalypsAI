#!/usr/bin/env node

const { program } = require('commander');
const fs = require('fs').promises;
const path = require('path');
const chalk = require('chalk');

async function getFilesOlderThan(directory, ageDays, verbose = false) {
    const cutoffDate = new Date(Date.now() - ageDays * 24 * 60 * 60 * 1000);
    const oldFiles = [];

    async function traverse(currentPath) {
        try {
            const entries = await fs.readdir(currentPath, { withFileTypes: true });
            for (const entry of entries) {
                const fullPath = path.join(currentPath, entry.name);
                if (entry.isDirectory()) {
                    await traverse(fullPath);
                } else if (entry.isFile()) {
                    const stats = await fs.stat(fullPath);
                    if (stats.mtime < cutoffDate) {
                        oldFiles.push({
                            path: fullPath,
                            mtime: stats.mtime,
                            ageDays: Math.floor((Date.now() - stats.mtime.getTime()) / (24 * 60 * 60 * 1000))
                        });
                    } else if (verbose) {
                        console.log(chalk.gray(`  Skipping: ${fullPath} (too new)`));
                    }
                }
            }
        } catch (error) {
            console.error(chalk.red(`Error accessing ${currentPath}: ${error.message}`));
        }
    }

    await traverse(directory);
    return oldFiles;
}

async function scanCommand(directory, options) {
    const { age, verbose } = options;
    if (!age) {
        console.error(chalk.red('Error: --age is required for scanning.'));
        program.help();
        return;
    }

    console.log(chalk.blue(`\nSweeping for digital dust bunnies older than ${age} days in: ${directory}`));
    if (verbose) {
        console.log(chalk.gray('Verbose mode enabled.'));
    }

    const oldFiles = await getFilesOlderThan(directory, age, verbose);

    if (oldFiles.length === 0) {
        console.log(chalk.green('\nNo digital dust bunnies found! Your directory is sparkling clean. \u2728'));
    } else {
        console.log(chalk.yellow(`\nFound ${oldFiles.length} digital dust bunnies:`));
        oldFiles.forEach(file => {
            console.log(`- ${chalk.cyan(file.path)} (Modified: ${file.mtime.toLocaleDateString()}, Age: ${file.ageDays} days)`);
        });
        console.log(chalk.yellow('\nConsider reviewing these files for archival or deletion.'));
    }
}

async function quarantineCommand(directory, options) {
    const { age, output, verbose } = options;
    if (!age || !output) {
        console.error(chalk.red('Error: --age and --output are required for quarantining.'));
        program.help();
        return;
    }

    const quarantineDir = path.resolve(output);
    console.log(chalk.blue(`\nQuarantining digital dust bunnies older than ${age} days from: ${directory}`));
    console.log(chalk.blue(`To: ${quarantineDir}`));
    if (verbose) {
        console.log(chalk.gray('Verbose mode enabled.'));
    }

    try {
        await fs.mkdir(quarantineDir, { recursive: true });
        console.log(chalk.green(`Ensured quarantine directory exists: ${quarantineDir}`));
    } catch (error) {
        console.error(chalk.red(`Error creating quarantine directory ${quarantineDir}: ${error.message}`));
        return;
    }

    const oldFiles = await getFilesOlderThan(directory, age, verbose);

    if (oldFiles.length === 0) {
        console.log(chalk.green('\nNo digital dust bunnies found to quarantine! Your directory is sparkling clean. \u2728'));
        return;
    }

    console.log(chalk.yellow(`\nAttempting to quarantine ${oldFiles.length} digital dust bunnies:`));
    for (const file of oldFiles) {
        const fileName = path.basename(file.path);
        const newPath = path.join(quarantineDir, fileName);
        try {
            await fs.rename(file.path, newPath);
            console.log(`- ${chalk.cyan(file.path)} -> ${chalk.magenta(newPath)}`);
        } catch (error) {
            console.error(chalk.red(`  Error quarantining ${file.path}: ${error.message}`));
        }
    }
    console.log(chalk.green('\nQuarantine operation complete. Review files in the quarantine directory.'));
}

program
    .name('dust-sweeper')
    .description('A whimsical utility to sweep away digital dust bunnies (old files).')
    .version('1.0.0');

program.command('scan <directory>')
    .description('Scans the specified directory for files older than --age days and lists them.')
    .option('-a, --age <days>', 'Minimum age in days for a file to be considered old.', parseInt)
    .option('-v, --verbose', 'Display more detailed output during scanning.')
    .action(scanCommand);

program.command('quarantine <directory>')
    .description('Scans the specified directory for files older than --age days and moves them to --output directory.')
    .option('-a, --age <days>', 'Minimum age in days for a file to be considered old.', parseInt)
    .option('-o, --output <path>', 'The directory where identified files will be moved.')
    .option('-v, --verbose', 'Display more detailed output during scanning.')
    .action(quarantineCommand);

program.parse(process.argv);

// If no command is given, show help
if (!process.argv.slice(2).length) {
    program.help();
}
