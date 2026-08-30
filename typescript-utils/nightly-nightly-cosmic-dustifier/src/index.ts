import { Command } from 'commander';
import * as chalk from 'chalk';
import { scanAndIdentifyDust, performDustification } from './fileScanner';
import { DustificationAction, DustificationOptions } from './types';
import * as path from 'path';

const program = new Command();

program
  .name('cosmic-dustifier')
  .description(chalk.hex('#FFD700')('🌌 ApocalypsAI Nightly Cosmic Dustifier 🌌\n') +
               chalk.gray('  Identifies and optionally "dustifies" (archives or deletes) files\n') +
               chalk.gray('  older than a specified cosmic decay threshold.'))
  .version('1.0.0');

program
  .argument('<path>', 'The cosmic directory to scan for ancient files.')
  .option('-t, --threshold <days>', 'Files older than this many days will be considered cosmic dust.', '30')
  .option('-a, --action <type>', 'Action to perform: list (default), archive, or delete.', 'list')
  .option('-d, --archive-dir <directory>', 'Directory to move archived files to. Required for "archive" action.')
  .option('-n, --dry-run', 'Simulate the dustification process without making any changes.')
  .action(async (targetPath: string, options: any) => {
    const thresholdDays = parseInt(options.threshold, 10);
    if (isNaN(thresholdDays) || thresholdDays <= 0) {
      console.error(chalk.red('❌ Error: --threshold must be a positive number of days.'));
      process.exit(1);
    }

    const action: DustificationAction = options.action.toLowerCase();
    if (!['list', 'archive', 'delete'].includes(action)) {
      console.error(chalk.red('❌ Error: --action must be one of "list", "archive", or "delete".'));
      process.exit(1);
    }

    if (action === 'archive' && !options.archiveDir) {
      console.error(chalk.red('❌ Error: --archive-dir is required for the "archive" action.'));
      process.exit(1);
    }

    const dustificationOptions: DustificationOptions = {
      path: path.resolve(targetPath),
      thresholdDays,
      action,
      archiveDir: options.archiveDir ? path.resolve(options.archiveDir) : undefined,
      dryRun: !!options.dryRun,
    };

    console.log(chalk.hex('#8A2BE2')(`\n✨ Initiating Cosmic Dustification Scan in ${dustificationOptions.path}...`));
    if (dustificationOptions.dryRun) {
      console.log(chalk.yellow('🔭 Performing a DRY RUN. No actual changes will be made.'));
    }
    console.log(chalk.cyan(`⏳ Looking for files older than ${dustificationOptions.thresholdDays} days.`));
    console.log(chalk.magenta(`🚀 Action: ${dustificationOptions.action.toUpperCase()}`));
    if (dustificationOptions.action === 'archive' && dustificationOptions.archiveDir) {
      console.log(chalk.magenta(`📦 Archive Directory: ${dustificationOptions.archiveDir}`));
    }
    console.log(''); // Newline for spacing

    try {
      const dustFiles = await scanAndIdentifyDust(dustificationOptions);

      if (dustFiles.length === 0) {
        console.log(chalk.green('✅ No cosmic dust found! Your directory is sparkling clean.'));
        return;
      }

      console.log(chalk.hex('#FFA500')(`🌠 Found ${dustFiles.length} files ready for cosmic dustification:`));
      for (const file of dustFiles) {
        const result = await performDustification(file, dustificationOptions);
        console.log(result);
      }
      console.log(chalk.hex('#FFD700')('\n🌌 Cosmic Dustification complete. May your digital space be ever vast and clean.'));

    } catch (error) {
      console.error(chalk.red(`\n❌ A cosmic anomaly occurred: ${error instanceof Error ? error.message : String(error)}`));
      process.exit(1);
    }
  });

program.parse(process.argv);
