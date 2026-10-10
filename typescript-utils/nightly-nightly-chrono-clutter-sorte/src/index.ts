import { readFileSync } from 'fs';
import { ChronoClutterSorter, ChronoConfig, SortedResult, Category } from './sorter';

function parseArgs(args: string[]): { configPath: string; items: string[] } {
  let configPath: string | undefined;
  const items: string[] = [];

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--config' && args[i + 1]) {
      configPath = args[++i];
    } else if (!args[i].startsWith('--')) {
      items.push(args[i]);
    }
  }

  if (!configPath) {
    console.error('Error: --config <path_to_config.json> is required.');
    process.exit(1);
  }

  return { configPath, items };
}

function printResults(sortedResult: SortedResult, sorter: ChronoClutterSorter) {
  console.log('\n--- Chrono-Clutter Sorting Report ---\n');

  const categories = sorter.getAllCategories();

  for (const category of categories) {
    const items = sortedResult[category.id];
    if (items && items.length > 0) {
      console.log(`Category: ${category.name} (${category.description})`);
      items.forEach(item => console.log(`  - ${item}`));
      console.log('');
    }
  }
  console.log('-------------------------------------\n');
}

async function main() {
  const { configPath, items } = parseArgs(process.argv.slice(2));

  let config: ChronoConfig;
  try {
    const configFileContent = readFileSync(configPath, 'utf8');
    config = JSON.parse(configFileContent) as ChronoConfig;
  } catch (error) {
    console.error(`Error reading or parsing config file '${configPath}':`, error instanceof Error ? error.message : String(error));
    process.exit(1);
  }

  try {
    const sorter = new ChronoClutterSorter(config);
    const sorted = sorter.sort(items);
    printResults(sorted, sorter);
  } catch (error) {
    console.error('Error during sorting:', error instanceof Error ? error.message : String(error));
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
