import * as fs from 'fs';
import * as path from 'path';
import { ArchivistConfig, Category, Rule } from './types';

function printHelp(): void {
    console.log(`
Usage: nightly-digital-detritus-arch --source <source_directory> --dest <destination_directory> --config <config_file.json> [--dry-run]

Arguments:
  --source <path>      The directory containing files to organize.
  --dest <path>        The root directory for categorized files.
  --config <path>      Path to the JSON configuration file.
  --dry-run            (Optional) Simulate actions without moving files.
  --help               Display this help message.
`);
}

function loadConfig(configPath: string): ArchivistConfig {
    try {
        const configContent = fs.readFileSync(configPath, 'utf8');
        const config: ArchivistConfig = JSON.parse(configContent);

        // Basic validation
        if (!config.defaultCategoryName || !Array.isArray(config.categories)) {
            throw new Error('Invalid configuration structure.');
        }
        for (const cat of config.categories) {
            if (!cat.name || !cat.destinationSubdir || !Array.isArray(cat.rules)) {
                throw new Error(`Invalid category structure for '${cat.name}'.`);
            }
            for (const rule of cat.rules) {
                if (!rule.type) {
                    throw new Error(`Invalid rule in category '${cat.name}'.`);
                }
            }
        }

        return config;
    } catch (error: any) {
        console.error(`Error loading configuration from ${configPath}: ${error.message}`);
        process.exit(1);
    }
}

function matchesRule(filePath: string, fileStats: fs.Stats, rule: Rule): boolean {
    const fileName = path.basename(filePath);
    const fileExtension = path.extname(filePath);

    switch (rule.type) {
        case 'name':
            return rule.pattern ? new RegExp(rule.pattern, 'i').test(fileName) : false;
        case 'extension':
            return rule.pattern ? new RegExp(rule.pattern, 'i').test(fileExtension) : false;
        case 'size':
            const fileSizeKB = fileStats.size / 1024;
            const minMatch = rule.minSizeKB === undefined || fileSizeKB >= rule.minSizeKB;
            const maxMatch = rule.maxSizeKB === undefined || fileSizeKB <= rule.maxSizeKB;
            return minMatch && maxMatch;
        case 'content':
            if (rule.pattern) {
                try {
                    const fileContent = fs.readFileSync(filePath, 'utf8');
                    return new RegExp(rule.pattern, 'i').test(fileContent);
                } catch (e) {
                    // Ignore binary files or unreadable content for content rules
                    return false;
                }
            }
            return false;
        default:
            return false;
    }
}

function classifyFile(filePath: string, fileStats: fs.Stats, config: ArchivistConfig): Category {
    for (const category of config.categories) {
        for (const rule of category.rules) {
            if (matchesRule(filePath, fileStats, rule)) {
                return category;
            }
        }
    }
    // Return a default category for unclassified files
    const defaultCategory = config.categories.find(c => c.name === config.defaultCategoryName);
    if (defaultCategory) {
        return defaultCategory;
    } else {
        // Fallback if default category is not explicitly defined in categories list
        return {
            name: config.defaultCategoryName,
            description: 'Files that did not match any specific archiving rules.',
            rules: [],
            destinationSubdir: 'unclassified'
        };
    }
}

async function archiveFiles(sourceDir: string, destDir: string, configPath: string, dryRun: boolean): Promise<void> {
    if (!fs.existsSync(sourceDir)) {
        console.error(`Error: Source directory '${sourceDir}' does not exist.`);
        process.exit(1);
    }
    if (!fs.existsSync(destDir)) {
        console.error(`Error: Destination directory '${destDir}' does not exist.`);
        process.exit(1);
    }

    const config = loadConfig(configPath);
    console.log(`\n--- Digital Detritus Archivist ${dryRun ? '(DRY RUN)' : ''} ---`);
    console.log(`Source: ${sourceDir}`);
    console.log(`Destination: ${destDir}`);
    console.log(`Config: ${configPath}\n`);

    const files = fs.readdirSync(sourceDir);

    if (files.length === 0) {
        console.log('No files found in the source directory to archive.');
        return;
    }

    for (const file of files) {
        const sourceFilePath = path.join(sourceDir, file);
        let fileStats: fs.Stats;
        try {
            fileStats = fs.statSync(sourceFilePath);
        } catch (e) {
            console.warn(`Skipping '${file}': Could not stat file.`);
            continue;
        }

        if (!fileStats.isFile()) {
            console.log(`Skipping '${file}': Not a file.`);
            continue;
        }

        const targetCategory = classifyFile(sourceFilePath, fileStats, config);
        const destSubdirPath = path.join(destDir, targetCategory.destinationSubdir);
        const destFilePath = path.join(destSubdirPath, file);

        console.log(`'${file}' (${(fileStats.size / 1024).toFixed(2)} KB) -> Category: '${targetCategory.name}' (Subdir: '${targetCategory.destinationSubdir}')`);

        if (!dryRun) {
            try {
                if (!fs.existsSync(destSubdirPath)) {
                    fs.mkdirSync(destSubdirPath, { recursive: true });
                    console.log(`  Created destination directory: ${destSubdirPath}`);
                }
                fs.renameSync(sourceFilePath, destFilePath);
                console.log(`  Moved to: ${destFilePath}`);
            } catch (error: any) {
                console.error(`  Error moving '${file}': ${error.message}`);
            }
        }
    }
    console.log(`\n--- Archiving complete ${dryRun ? '(DRY RUN)' : ''} ---`);
}

// CLI entry point
async function main() {
    const args = process.argv.slice(2);
    let sourceDir: string | undefined;
    let destDir: string | undefined;
    let configPath: string | undefined;
    let dryRun = false;

    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--source':
                sourceDir = args[++i];
                break;
            case '--dest':
                destDir = args[++i];
                break;
            case '--config':
                configPath = args[++i];
                break;
            case '--dry-run':
                dryRun = true;
                break;
            case '--help':
                printHelp();
                process.exit(0);
            default:
                console.error(`Unknown argument: ${args[i]}`);
                printHelp();
                process.exit(1);
        }
    }

    if (!sourceDir || !destDir || !configPath) {
        console.error('Error: Missing required arguments (--source, --dest, --config).');
        printHelp();
        process.exit(1);
    }

    await archiveFiles(sourceDir, destDir, configPath, dryRun);
}

if (require.main === module) {
    main();
}
