import { Command } from 'commander';
import * as fs from 'fs';
import * as path from 'path';
import chalk from 'chalk';
import { scryText } from './scryer';
import { ScryOptions, KeywordCategory } from './types';

const program = new Command();

program
  .name('echo-scryer')
  .description('A TypeScript CLI tool to reconstruct fragmented text, highlight key terms, and infer apocalyptic context.')
  .version('1.0.0');

program
  .argument('<file>', 'Path to the fragmented text file to scry')
  .option('-t, --fragment-threshold <number>', 'How much "noise" to tolerate or simulate (0-1, lower means more noise removed/ignored). Currently not fully implemented for dynamic cleaning, but reserved for future use.', '0.5')
  .option('-c, --context-level <level>', 'How detailed the context inference should be (low, medium, high).', 'medium')
  .action(async (filePath, options) => {
    const fullPath = path.resolve(filePath);

    if (!fs.existsSync(fullPath)) {
      console.error(chalk.red(`Error: File not found at ${fullPath}`));
      process.exit(1);
    }

    let fileContent: string;
    try {
      fileContent = fs.readFileSync(fullPath, 'utf-8');
    } catch (error: any) {
      console.error(chalk.red(`Error reading file: ${error.message}`));
      process.exit(1);
    }

    const scryOptions: ScryOptions = {
      fragmentThreshold: parseFloat(options.fragmentThreshold),
      contextLevel: options.contextLevel as ScryOptions['contextLevel'],
    };

    if (!['low', 'medium', 'high'].includes(scryOptions.contextLevel)) {
      console.error(chalk.red(`Error: Invalid context level '${scryOptions.contextLevel}'. Must be 'low', 'medium', or 'high'.`));
      process.exit(1);
    }

    console.log(chalk.yellow(`\n--- Initiating Echo Scrying for: ${filePath} ---`));

    const report = scryText(fileContent, scryOptions);

    console.log(chalk.cyan('\n[ Original Transmission ]'));
    console.log(report.originalText);

    console.log(chalk.cyan('\n[ Cleaned Echoes ]'));
    // Highlight keywords in the cleaned text
    let highlightedText = report.cleanedText;
    const categoryColors: Record<KeywordCategory, chalk.Chalk> = {
      Survival: chalk.green,
      Danger: chalk.red,
      Resource: chalk.blue,
      Hope: chalk.magenta,
      Mystery: chalk.yellow,
      Technology: chalk.cyan
    };

    // Replace keywords with colored versions, ensuring longer keywords are replaced first
    // and avoiding re-highlighting already highlighted parts.
    // This is a simplified approach, a more robust one would involve tokenizing and then coloring.
    // For CLI output, simple string replace is often sufficient.
    const sortedKeywords = report.identifiedKeywords.sort((a, b) => b.keyword.length - a.keyword.length);
    for (const match of sortedKeywords) {
        const colorFn = categoryColors[match.category];
        // Use a regex with global flag to replace all occurrences
        highlightedText = highlightedText.replace(new RegExp(`\\b${match.keyword}\\b`, 'gi'), colorFn(match.keyword));
    }
    console.log(highlightedText);

    console.log(chalk.cyan('\n[ Scrying Report ]'));
    console.log(`  ${chalk.bold('Dominant Vibe:')} ${chalk.bold(report.dominantCategory)}`);
    console.log(`  ${chalk.bold('Apocalyptic Vibe:')} ${report.apocalypticVibe}`);
    console.log(`  ${chalk.bold('Suggested Action:')} ${report.suggestedAction}`);

    console.log(chalk.cyan('\n[ Keyword Frequencies ]'));
    for (const category in report.categoryCounts) {
      const count = report.categoryCounts[category as KeywordCategory];
      if (count > 0) {
        console.log(`  ${categoryColors[category as KeywordCategory](category)}: ${count}`);
      }
    }

    console.log(chalk.yellow('\n--- Echo Scrying Complete ---'));
  });

program.parse(process.argv);
