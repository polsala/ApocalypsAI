#!/usr/bin/env node
const { findDustBunnies, deleteDustBunnies, defaultPatterns } = require('./sweeper');
const path = require('path');
const readline = require('readline');
const { program } = require('commander');

program
    .name('nightly-dust-bunny-sweeper')
    .description('A Node.js CLI tool to sweep away digital dust bunnies (temporary files and build artifacts) from your projects.')
    .version('1.0.0')
    .argument('[directory]', 'Directory to scan for dust bunnies (defaults to current directory)', '.')
    .option('-f, --force', 'Skip confirmation and delete all found dust bunnies immediately.')
    .option('-p, --patterns <patterns...>', 'Comma-separated list of custom patterns to search for (overrides defaults).', (value) => value.split(','))
    .action(async (directory, options) => {
        const targetDir = path.resolve(process.cwd(), directory);
        const patternsToUse = options.patterns && options.patterns.length > 0 ? options.patterns : defaultPatterns;

        console.log(`\n🧹 Sweeping for digital dust bunnies in: ${targetDir}`);
        if (options.patterns && options.patterns.length > 0) {
            console.log(`🔍 Using custom patterns: ${patternsToUse.join(', ')}`);
        } else {
            console.log(`🔍 Using default patterns: ${patternsToUse.join(', ')}`);
        }

        const foundBunnies = findDustBunnies(targetDir, patternsToUse);

        if (foundBunnies.length === 0) {
            console.log('\n✨ No digital dust bunnies found. Your project is sparkling clean!');
            process.exit(0);
        }

        console.log(`\nFound ${foundBunnies.length} digital dust bunnies:`);
        foundBunnies.forEach(bunny => console.log(`  - ${bunny}`));

        if (options.force) {
            console.log('\n🗑️ Force deleting all dust bunnies...');
            const result = deleteDustBunnies(foundBunnies);
            if (result.errorCount > 0) {
                console.error(`\n❌ Encountered ${result.errorCount} errors during deletion:`);
                result.errors.forEach(err => console.error(`  - ${err.path}: ${err.error}`));
            }
            console.log(`\n✅ Swept away ${result.deletedCount} dust bunnies.`);
            process.exit(0);
        }

        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        rl.question('\nDo you want to sweep these dust bunnies away? (y/N) ', async (answer) => {
            rl.close();
            if (answer.toLowerCase() === 'y') {
                console.log('\n🗑️ Sweeping away dust bunnies...');
                const result = deleteDustBunnies(foundBunnies);
                if (result.errorCount > 0) {
                    console.error(`\n❌ Encountered ${result.errorCount} errors during deletion:`);
                    result.errors.forEach(err => console.error(`  - ${err.path}: ${err.error}`));
                }
                console.log(`\n✅ Swept away ${result.deletedCount} dust bunnies.`);
            } else {
                console.log('\n👍 Digital dust bunnies spared. Run again anytime!');
            }
            process.exit(0);
        });
    });

program.parse(process.argv);
