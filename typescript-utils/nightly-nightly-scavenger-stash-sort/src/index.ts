import { readFileSync } from 'fs';
import { Item } from './types';
import { defaultCategories } from './categories';
import { sortItemsIntoStashes } from './sorter';

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: npm start -- <path/to/items.json>');
    process.exit(1);
  }

  const itemsFilePath = args[0];

  try {
    const itemsJson = readFileSync(itemsFilePath, 'utf8');
    const items: Item[] = JSON.parse(itemsJson);

    const sortedStash = sortItemsIntoStashes(items, defaultCategories);

    console.log(JSON.stringify(sortedStash, null, 2));
  } catch (error: any) {
    console.error(`Error processing items file: ${error.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
