import { promises as fs } from 'fs';
import * as path from 'path';
import { program } from 'commander';
import { FileInfo, ScanOptions } from './types';

// Exported for testing
export async function getFileInfo(filePath: string): Promise<FileInfo | null> {
    try {
        const stats = await fs.stat(filePath);
        return {
            name: path.basename(filePath),
            path: filePath,
            isDirectory: stats.isDirectory(),
            modifiedAt: stats.mtime,
            size: stats.size,
        };
    } catch (error) {
        // Ignore files we can't access (e.g., permission errors, broken symlinks)
        return null;
    }
}

// Exported for testing
export async function scanDirectory(dirPath: string, options: ScanOptions): Promise<FileInfo[]> {
    let allFiles: FileInfo[] = [];
    try {
        const entries = await fs.readdir(dirPath, { withFileTypes: true });

        for (const entry of entries) {
            const fullPath = path.join(dirPath, entry.name);
            if (entry.isDirectory()) {
                if (options.recursive) {
                    allFiles = allFiles.concat(await scanDirectory(fullPath, options));
                }
            } else {
                const fileInfo = await getFileInfo(fullPath);
                if (fileInfo) {
                    allFiles.push(fileInfo);
                }
            }
        }
    } catch (error) {
        // console.error(`Error scanning directory ${dirPath}: ${error}`); // Suppress for tests, or mock console.error
    }
    return allFiles;
}

// Exported for testing
export function filterDustBunnies(files: FileInfo[], options: ScanOptions): FileInfo[] {
    const now = new Date();
    const ageThresholdMs = options.ageDays * 24 * 60 * 60 * 1000;

    return files.filter(file => {
        const isOld = (now.getTime() - file.modifiedAt.getTime()) > ageThresholdMs;
        const matchesPattern = options.patterns.some(pattern => new RegExp(pattern).test(file.name));

        return isOld || matchesPattern;
    });
}

async function main() {
    program
        .name('temporal-dust-bunny-collector')
        .description('Finds and reports old or temporary files (temporal "dust bunnies").')
        .argument('<path>', 'The directory to scan for dust bunnies.')
        .option('-a, --age-days <days>', 'Files older than this many days are considered dust bunnies.', '30')
        .option('-p, --patterns <patterns...>', 'File name patterns (regex) to consider as dust bunnies (e.g., ".*\\.bak", "temp_.*", "~$").', [])
        .option('-r, --recursive', 'Scan directories recursively.', false)
        .option('-d, --dry-run', 'Perform a dry run without making any changes. (Default: true)', true)
        .action(async (scanPath: string, opts: { ageDays: string, patterns: string[], recursive: boolean, dryRun: boolean }) => {
            const options: ScanOptions = {
                ageDays: parseInt(opts.ageDays, 10),
                patterns: opts.patterns,
                recursive: opts.recursive,
                dryRun: opts.dryRun,
            };

            console.log(`Scanning '${scanPath}' for temporal dust bunnies...`);
            console.log(`Options: Age > ${options.ageDays} days, Patterns: [${options.patterns.join(', ')}], Recursive: ${options.recursive ? 'Yes' : 'No'}`);

            const allFiles = await scanDirectory(scanPath, options);
            const dustBunnies = filterDustBunnies(allFiles, options);

            if (dustBunnies.length === 0) {
                console.log('No temporal dust bunnies found. Your timeline is pristine!');
                return;
            }

            console.log(`\nFound ${dustBunnies.length} temporal dust bunnies:`);
            dustBunnies.forEach(bunny => {
                console.log(`- ${bunny.path} (Modified: ${bunny.modifiedAt.toLocaleDateString()}, Size: ${bunny.size} bytes)`);
            });

            if (options.dryRun) {
                console.log('\nThis was a DRY RUN. No files were affected.');
                console.log('To actually clean them up (feature not yet implemented, but imagine the possibilities!), consider contributing!');
            } else {
                console.log('\nCleaning up temporal dust bunnies... (Feature not yet implemented, this is still a dry run for now!)');
                // Placeholder for future implementation of actual cleanup logic.
                // For safety and simplicity of this utility, we'll keep it as a reporting tool for now.
            }
        });

    program.parse(process.argv);
}

if (require.main === module) {
    main();
}
