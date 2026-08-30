import { ScavengedItem, SurvivalPriority, sortAndFilterItems } from './item';
import * as fs from 'fs';
import * as path from 'path';

function printHelp() {
  console.log(`\nUsage: stash-sorter <command> [options]\n\nCommands:\n  sort <input-file> [output-file]  Sorts and filters items from <input-file>\n                                   and outputs to <output-file> (or stdout).\n\nOptions for 'sort':\n  --category <cat1,cat2,...>       Filter by item categories (e.g., food, weapon)\n  --rarity <rar1,rar2,...>         Filter by item rarities (e.g., common, rare)\n  --min-condition <condition>      Filter by minimum condition (broken, damaged, worn, good, pristine)\n  --sort-by <field>                Sort by item field (e.g., name, value_units, weight_kg, condition)\n  --sort-order <order>             Sort order (asc or desc, default: asc)\n  --limit <number>                 Limit the number of results\n  --help                           Display this help message\n`);
}

function parseArgs(args: string[]): { command: string, inputFile?: string, outputFile?: string, priority: SurvivalPriority, help: boolean } {
  const result: { command: string, inputFile?: string, outputFile?: string, priority: SurvivalPriority, help: boolean } = {
    command: '',
    priority: {},
    help: false
  };

  let i = 0;
  if (args.length === 0) {
    result.help = true;
    return result;
  }

  result.command = args[i++];

  if (result.command === 'sort') {
    if (i < args.length && !args[i].startsWith('--')) {
      result.inputFile = args[i++];
    }
    if (i < args.length && !args[i].startsWith('--')) {
      result.outputFile = args[i++];
    }

    while (i < args.length) {
      const arg = args[i];
      switch (arg) {
        case '--category':
          result.priority.filterCategory = args[++i].split(',') as ScavengedItem['category'][];
          break;
        case '--rarity':
          result.priority.filterRarity = args[++i].split(',') as ScavengedItem['rarity'][];
          break;
        case '--min-condition':
          result.priority.filterConditionMin = args[++i] as ScavengedItem['condition'];
          break;
        case '--sort-by':
          result.priority.sortBy = args[++i] as keyof ScavengedItem;
          break;
        case '--sort-order':
          result.priority.sortOrder = args[++i] as 'asc' | 'desc';
          break;
        case '--limit':
          result.priority.limit = parseInt(args[++i], 10);
          break;
        case '--help':
          result.help = true;
          break;
        default:
          console.error(`Unknown option: ${arg}`);
          result.help = true;
          break;
      }
      i++;
    }
  } else if (result.command === '--help') {
    result.help = true;
  } else {
    console.error(`Unknown command: ${result.command}`);
    result.help = true;
  }

  return result;
}

async function main() {
  const { command, inputFile, outputFile, priority, help } = parseArgs(process.argv.slice(2));

  if (help || !command || (command === 'sort' && !inputFile)) {
    printHelp();
    process.exit(0);
  }

  if (command === 'sort') {
    try {
      const inputPath = path.resolve(process.cwd(), inputFile!);
      const rawData = fs.readFileSync(inputPath, 'utf8');
      const items: ScavengedItem[] = JSON.parse(rawData);

      const sortedItems = sortAndFilterItems(items, priority);
      const outputContent = JSON.stringify(sortedItems, null, 2);

      if (outputFile) {
        const outputPath = path.resolve(process.cwd(), outputFile);
        fs.writeFileSync(outputPath, outputContent, 'utf8');
        console.log(`Sorted items written to ${outputPath}`);
      } else {
        console.log(outputContent);
      }
    } catch (error: any) {
      console.error(`Error processing items: ${error.message}`);
      process.exit(1);
    }
  }
}

if (require.main === module) {
  main();
}
