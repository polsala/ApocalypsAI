import { HoardManager } from './hoardManager';
import { DigitalItem, Scarcity, Utility } from './types';
import { Command } from 'commander';
import * as path from 'path';

const program = new Command();
const dataDir = path.join(process.cwd(), '.hoard_data');
const manager = new HoardManager(dataDir);

program
  .name('hoard-curator')
  .description('CLI tool to manage your digital hoard with scarcity and utility ratings.')
  .version('1.0.0');

program.command('add <name> <type> <pathOrContent> <scarcity> <utility>')
  .description('Add a new digital item to your hoard.')
  .action((name: string, type: DigitalItem['type'], pathOrContent: string, scarcity: Scarcity, utility: Utility) => {
    if (!['file', 'url', 'text'].includes(type)) {
      console.error(`Error: Invalid type '${type}'. Must be 'file', 'url', or 'text'.`);
      process.exit(1);
    }
    if (!['common', 'uncommon', 'rare', 'legendary'].includes(scarcity)) {
      console.error(`Error: Invalid scarcity '${scarcity}'. Must be 'common', 'uncommon', 'rare', or 'legendary'.`);
      process.exit(1);
    }
    if (!['essential', 'useful', 'archive', 'ephemeral'].includes(utility)) {
      console.error(`Error: Invalid utility '${utility}'. Must be 'essential', 'useful', 'archive', or 'ephemeral'.`);
      process.exit(1);
    }
    const newItem = manager.addItem(name, type, pathOrContent, scarcity, utility);
    console.log(`Added item: "${newItem.name}" (ID: ${newItem.id.substring(0, 8)})`);
  });

program.command('list')
  .description('List all items in your digital hoard.')
  .action(() => {
    const items = manager.listItems();
    if (items.length === 0) {
      console.log('Your digital hoard is empty. Time to scavenge!');
      return;
    }
    console.log('--- Your Digital Hoard ---');
    items.forEach(item => {
      console.log(`ID: ${item.id.substring(0, 8)}`);
      console.log(`  Name: ${item.name}`);
      console.log(`  Type: ${item.type}`);
      console.log(`  Path/Content: ${item.pathOrContent.length > 50 ? item.pathOrContent.substring(0, 47) + '...' : item.pathOrContent}`);
      console.log(`  Scarcity: ${item.scarcity}`);
      console.log(`  Utility: ${item.utility}`);
      console.log(`  Added: ${new Date(item.addedAt).toLocaleDateString()}`);
      console.log('--------------------------');
    });
  });

program.command('report')
  .description('Generate a curation report for your hoard.')
  .action(() => {
    const report = manager.generateCurationReport();
    report.forEach(line => console.log(line));
  });

program.command('delete <id>')
  .description('Delete an item from your hoard by ID.')
  .action((id: string) => {
    if (manager.deleteItem(id)) {
      console.log(`Item with ID ${id.substring(0, 8)} deleted.`);
    } else {
      console.error(`Error: Item with ID ${id.substring(0, 8)} not found.`);
      process.exit(1);
    }
  });

program.parse(process.argv);
