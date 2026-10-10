import { Command } from 'commander';
import { ScavengerManifest } from './manifest';
import { ItemCondition } from './types';

const program = new Command();
const manifest = new ScavengerManifest();

program
  .name('scavenger-manifest')
  .description('CLI for managing your scavenged items manifest.')
  .version('1.0.0');

program.command('add')
  .description('Add a new item to the manifest.')
  .requiredOption('-n, --name <name>', 'Name of the item.')
  .requiredOption('-c, --category <category>', 'Category of the item (e.g., Tool, Food, Weapon).')
  .requiredOption('-o, --condition <condition>', 'Condition of the item (Pristine, Good, Worn, Damaged, Broken, Mysterious).')
  .requiredOption('-q, --quantity <quantity>', 'Quantity of the item.', parseInt)
  .option('-s, --notes <notes>', 'Optional notes about the item.')
  .action(async (options) => {
    const { name, category, condition, quantity, notes } = options;
    if (!Object.values(ItemCondition).includes(condition as ItemCondition)) {
      console.error(`Error: Invalid condition '${condition}'. Must be one of: ${Object.values(ItemCondition).join(', ')}`);
      process.exit(1);
    }
    try {
      const newItem = await manifest.addItem(name, category, condition as ItemCondition, quantity, notes);
      console.log(`Added item: ${newItem.name} (ID: ${newItem.id})`);
    } catch (error: any) {
      console.error(`Failed to add item: ${error.message}`);
    }
  });

program.command('list')
  .description('List all items in the manifest.')
  .action(async () => {
    try {
      const items = await manifest.listItems();
      if (items.length === 0) {
        console.log('Manifest is empty. Start scavenging!');
        return;
      }
      items.forEach(item => {
        console.log(`ID: ${item.id}\n  Name: ${item.name}\n  Category: ${item.category}\n  Condition: ${item.condition}\n  Quantity: ${item.quantity}\n  Notes: ${item.notes || 'N/A'}\n  Created: ${new Date(item.createdAt).toLocaleString()}\n  Updated: ${new Date(item.updatedAt).toLocaleString()}\n`);
      });
    } catch (error: any) {
      console.error(`Failed to list items: ${error.message}`);
    }
  });

program.command('update')
  .description('Update an existing item in the manifest.')
  .requiredOption('-i, --id <id>', 'ID of the item to update.')
  .option('-n, --name <name>', 'New name for the item.')
  .option('-c, --category <category>', 'New category for the item.')
  .option('-o, --condition <condition>', 'New condition for the item.')
  .option('-q, --quantity <quantity>', 'New quantity for the item.', parseInt)
  .option('-s, --notes <notes>', 'New notes for the item.')
  .action(async (options) => {
    const { id, name, category, condition, quantity, notes } = options;
    const updates: Partial<ItemCondition | string | number> = {};
    if (name) updates.name = name;
    if (category) updates.category = category;
    if (condition) {
      if (!Object.values(ItemCondition).includes(condition as ItemCondition)) {
        console.error(`Error: Invalid condition '${condition}'. Must be one of: ${Object.values(ItemCondition).join(', ')}`);
        process.exit(1);
      }
      updates.condition = condition;
    }
    if (quantity !== undefined) updates.quantity = quantity;
    if (notes) updates.notes = notes;

    try {
      const updatedItem = await manifest.updateItem(id, updates);
      if (updatedItem) {
        console.log(`Updated item: ${updatedItem.name} (ID: ${updatedItem.id})`);
      } else {
        console.error(`Item with ID '${id}' not found.`);
      }
    } catch (error: any) {
      console.error(`Failed to update item: ${error.message}`);
    }
  });

program.command('remove')
  .description('Remove an item from the manifest.')
  .requiredOption('-i, --id <id>', 'ID of the item to remove.')
  .action(async (options) => {
    const { id } = options;
    try {
      const removed = await manifest.removeItem(id);
      if (removed) {
        console.log(`Removed item with ID: ${id}`);
      } else {
        console.error(`Item with ID '${id}' not found.`);
      }
    } catch (error: any) {
      console.error(`Failed to remove item: ${error.message}`);
    }
  });

program.command('search')
  .description('Search for items in the manifest.')
  .requiredOption('-q, --query <query>', 'Search query string.')
  .option('-f, --field <field>', 'Optional field to search within (name, category, condition, notes).')
  .action(async (options) => {
    const { query, field } = options;
    try {
      const results = await manifest.searchItems(query, field);
      if (results.length === 0) {
        console.log(`No items found matching '${query}'${field ? ` in field '${field}'` : ''}.`);
        return;
      }
      console.log(`Found ${results.length} item(s) matching '${query}'${field ? ` in field '${field}'` : ''}:`);
      results.forEach(item => {
        console.log(`ID: ${item.id}\n  Name: ${item.name}\n  Category: ${item.category}\n  Condition: ${item.condition}\n  Quantity: ${item.quantity}\n  Notes: ${item.notes || 'N/A'}\n`);
      });
    } catch (error: any) {
      console.error(`Failed to search items: ${error.message}`);
    }
  });

program.parse(process.argv);
