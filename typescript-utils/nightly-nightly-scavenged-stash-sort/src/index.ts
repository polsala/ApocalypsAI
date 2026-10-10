// src/index.ts

import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';
import { StashSorter, CategorizedStash, Item, Category } from './sorter';

const sorter = new StashSorter();

yargs(hideBin(process.argv))
  .command(
    '$0 [items...]',
    'Categorize and prioritize your scavenged items.',
    (yargs) => {
      yargs.positional('items', {
        describe: 'A list of items to categorize (e.g., "rusty wrench" "glowing mushroom")',
        type: 'string',
        array: true,
        demandOption: true,
      });
    },
    (argv) => {
      if (argv.items && argv.items.length > 0) {
        const itemNames: string[] = argv.items as string[];
        const categorizedStash: CategorizedStash = sorter.categorizeAndPrioritize(itemNames);
        printReport(categorizedStash);
      } else {
        console.log('Please provide at least one item to categorize.');
        yargs.showHelp();
      }
    }
  )
  .help()
  .alias('h', 'help')
  .parse();

function printReport(stash: CategorizedStash): void {
  console.log('\n--- Scavenged Stash Report ---\n');

  // Sort categories by their defined priority (Very High > High > Medium > Low)
  const priorityOrder = { 'Very High': 4, 'High': 3, 'Medium': 2, 'Low': 1 };
  const sortedCategoryNames = Object.keys(stash).sort((a, b) => {
    const catA = sorter.getCategoryConfig(a);
    const catB = sorter.getCategoryConfig(b);
    const prioA = catA ? priorityOrder[catA.priority] : 0; // Uncategorized gets lowest priority
    const prioB = catB ? priorityOrder[catB.priority] : 0;
    return prioB - prioA; // Descending priority
  });

  for (const categoryName of sortedCategoryNames) {
    const items = stash[categoryName];
    if (items.length === 0) continue;

    const categoryConfig = sorter.getCategoryConfig(categoryName);
    const displayPriority = categoryConfig ? ` (Priority: ${categoryConfig.priority})` : '';
    const displayAttribute = categoryConfig ? ` (${categoryConfig.attributeForPrioritization.charAt(0).toUpperCase() + categoryConfig.attributeForPrioritization.slice(1)}: ` : ' (Whimsy: ';

    console.log(`Category: ${categoryName}${displayPriority}`);
    items.forEach((item, index) => {
      const primaryAttrValue = item.attributes[categoryConfig?.attributeForPrioritization || 'whimsy'] || 0;
      const whimsyAttrValue = item.attributes['whimsy'] || 0;
      console.log(`  ${index + 1}. ${item.name}${displayAttribute}${primaryAttrValue}, Whimsy: ${whimsyAttrValue})`);
    });
    console.log('');
  }

  console.log('--- End Report ---\n');
}
