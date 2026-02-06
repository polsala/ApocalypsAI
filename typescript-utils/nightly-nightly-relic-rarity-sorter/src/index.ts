import { Command } from 'commander';
import chalk from 'chalk';
import { classifyRelic, sortClassifiedRelics } from './classifier';
import { Relic, KeywordRule, ClassificationResult, Rarity } from './types';
import * as fs from 'fs';
import * as path from 'path';

const program = new Command();

program
  .name('relic-rarity-sorter')
  .description('A type-safe CLI tool to classify and sort scavenged relics by perceived rarity and utility.')
  .version('1.0.0');

program
  .argument('<relics...>', 'List of relics to classify (e.g., "Rusty Spoon" "Gleaming Data-Chip")')
  .option('-d, --descriptions <descriptions...>', 'Optional descriptions for relics, matching order of relics argument.')
  .option('-r, --rules <file>', 'Path to a JSON file containing custom keyword rules.')
  .action(async (relicNames: string[], options) => {
    const relics: Relic[] = relicNames.map((name, index) => ({
      name,
      description: options.descriptions ? options.descriptions[index] : undefined,
    }));

    let customRules: KeywordRule[] = [];
    if (options.rules) {
      try {
        const rulesPath = path.resolve(process.cwd(), options.rules);
        const rulesContent = fs.readFileSync(rulesPath, 'utf8');
        customRules = JSON.parse(rulesContent) as KeywordRule[];
        console.log(chalk.green(`\nLoaded custom rules from: ${rulesPath}`));
      } catch (error) {
        console.error(chalk.red(`\nError loading custom rules file: ${options.rules}`));
        console.error(chalk.red((error as Error).message));
        process.exit(1);
      }
    }

    const classifiedResults: ClassificationResult[] = relics.map(relic => classifyRelic(relic, customRules));
    const sortedResults = sortClassifiedRelics(classifiedResults);

    console.log(chalk.bold('\n--- Classified Relics ---'));
    sortedResults.forEach(result => {
      let rarityColor: (text: string) => string;
      switch (result.rarity) {
        case 'Common': rarityColor = chalk.gray; break;
        case 'Uncommon': rarityColor = chalk.white; break;
        case 'Rare': rarityColor = chalk.blue; break;
        case 'Legendary': rarityColor = chalk.magenta; break;
        case 'Mythic': rarityColor = chalk.yellow; break;
        default: rarityColor = chalk.white;
      }

      console.log(`\n${chalk.bold('Relic:')} ${result.relic.name}`);
      if (result.relic.description) {
        console.log(`${chalk.bold('  Description:')} ${result.relic.description}`);
      }
      console.log(`${chalk.bold('  Rarity:')} ${rarityColor(result.rarity)}`);
      console.log(`${chalk.bold('  Utility Score:')} ${chalk.cyan(result.utilityScore.toString())}/10`);
      console.log(`${chalk.bold('  Reasoning:')}`);
      result.reason.forEach(r => console.log(`    - ${r}`));
    });
  });

program.parse(process.argv);
