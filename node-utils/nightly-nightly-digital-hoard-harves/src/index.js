#!/usr/bin/env node

const { program } = require('commander');
const fs = require('fs').promises;
const path = require('path');
const chalk = require('chalk');

async function collectDigitalArtifacts(dir, olderThanDays, largerThanMb) {
    const artifacts = [];
    const now = Date.now();
    const olderThanMs = olderThanDays ? olderThanDays * 24 * 60 * 60 * 1000 : 0;
    const largerThanBytes = largerThanMb ? largerThanMb * 1024 * 1024 : 0;

    async function traverse(currentPath) {
        try {
            const entries = await fs.readdir(currentPath, { withFileTypes: true });

            for (const entry of entries) {
                const fullPath = path.join(currentPath, entry.name);
                if (entry.isDirectory()) {
                    await traverse(fullPath);
                } else if (entry.isFile()) {
                    try {
                        const stats = await fs.stat(fullPath);
                        const isOld = olderThanDays ? (now - stats.mtimeMs > olderThanMs) : false;
                        const isLarge = largerThanMb ? (stats.size > largerThanBytes) : false;

                        if ((olderThanDays && isOld) || (largerThanMb && isLarge) || (!olderThanDays && !largerThanMb)) {
                            artifacts.push({
                                path: fullPath,
                                size: stats.size,
                                mtime: new Date(stats.mtimeMs),
                                isOld,
                                isLarge
                            });
                        }
                    } catch (statErr) {
                        // Ignore files we can't stat (e.g., permission denied, broken symlinks)
                        // console.warn(chalk.yellow(`Skipping ${fullPath}: ${statErr.message}`));
                    }
                }
            }
        } catch (readDirErr) {
            // Ignore directories we can't read (e.g., permission denied)
            // console.warn(chalk.yellow(`Skipping directory ${currentPath}: ${readDirErr.message}`));
        }
    }

    await traverse(dir);
    return artifacts;
}

program
    .name('digital-hoard-harvester')
    .description(chalk.cyan('Unearthing your digital artifacts: a quest for old and large files! 🕵️‍♂️💾'))
    .requiredOption('-p, --path <path>', 'The root directory to start scanning from.')
    .option('-o, --older-than-days <days>', 'Only show files last modified more than <days> ago.', parseInt)
    .option('-l, --larger-than-mb <mb>', 'Only show files larger than <mb> megabytes.', parseFloat)
    .action(async (options) => {
        const { path: scanPath, olderThanDays, largerThanMb } = options;

        if (!olderThanDays && !largerThanMb) {
            console.log(chalk.yellow('⚠️  No filters specified. This will list ALL files. Consider adding --older-than-days or --larger-than-mb for a more focused hunt.'));
        }

        console.log(chalk.magenta(`\n🔍 Beginning the digital artifact hunt in: ${chalk.bold(scanPath)}`));
        if (olderThanDays) console.log(chalk.magenta(`   - Seeking relics older than ${chalk.bold(olderThanDays)} days.`));
        if (largerThanMb) console.log(chalk.magenta(`   - Seeking byte-sized burdens larger than ${chalk.bold(largerThanMb)} MB.`));
        console.log(chalk.magenta('--------------------------------------------------'));

        try {
            const artifacts = await collectDigitalArtifacts(scanPath, olderThanDays, largerThanMb);

            if (artifacts.length === 0) {
                console.log(chalk.green('\n✨ The digital landscape is pristine! No matching artifacts found.'));
            } else {
                console.log(chalk.blue(`\n📜 Found ${artifacts.length} digital artifacts matching your criteria:\n`));
                artifacts.forEach(artifact => {
                    let details = [];
                    if (artifact.isOld) details.push(chalk.red(`(Old: ${artifact.mtime.toLocaleDateString()})`));
                    if (artifact.isLarge) details.push(chalk.yellow(`(Size: ${(artifact.size / (1024 * 1024)).toFixed(2)} MB)`));
                    
                    console.log(`${chalk.gray('•')} ${chalk.white(artifact.path)} ${details.join(' ')}`);
                });
                console.log(chalk.magenta('\n--------------------------------------------------'));
                console.log(chalk.cyan('💡 Consider archiving, moving, or deleting these digital relics to lighten your load!'));
            }
        } catch (error) {
            console.error(chalk.red(`\n❌ An anomaly occurred during the harvest: ${error.message}`));
            process.exit(1);
        }
    });

if (require.main === module) {
    program.parse(process.argv);
}

// Export for testing
module.exports = { collectDigitalArtifacts, program };
