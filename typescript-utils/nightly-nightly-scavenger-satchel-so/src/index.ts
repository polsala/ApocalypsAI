import { Command } from 'commander';
import * as fs from 'fs';
import { sortSatchel } from './sorter';
import { Item, SatchelConfig } from './types';

const program = new Command();

program
  .name('scavenger-satchel-sorter')
  .description('Optimizes satchel contents for post-apocalyptic scavengers.')
  .version('1.0.0');

program
  .requiredOption('-f, --items-file <path>', 'Path to a JSON file containing item definitions.')
  .requiredOption('-w, --max-weight <number>', 'Maximum weight capacity of the satchel (e.g., kg).', parseFloat)
  .requiredOption('-v, --max-volume <number>', 'Maximum volume capacity of the satchel (e.g., liters).', parseFloat)
  .action((options) => {
    try {
      const itemsRaw = fs.readFileSync(options.itemsFile, 'utf8');
      const items: Item[] = JSON.parse(itemsRaw);

      if (!Array.isArray(items) || !items.every(i => typeof i.name === 'string' && typeof i.weight === 'number' && typeof i.volume === 'number' && typeof i.survival_score === 'number')) {
        throw new Error('Invalid items file format. Expected an array of objects with name, weight, volume, and survival_score.');
      }

      const config: SatchelConfig = {
        maxWeight: options.maxWeight,
        maxVolume: options.maxVolume,
      };

      const selectedItems = sortSatchel(items, config);

      console.log('--- Scavenger\'s Satchel Report ---');
      console.log(`Max Capacity: ${config.maxWeight}kg, ${config.maxVolume}L`);
      console.log('\nSelected Items:');
      if (selectedItems.length === 0) {
        console.log('  No items selected. Perhaps your satchel is too small or items are too heavy/bulky.');
      } else {
        let totalWeight = 0;
        let totalVolume = 0;
        let totalSurvivalScore = 0;
        selectedItems.forEach((item) => {
          console.log(`  - ${item.name} (Score: ${item.survival_score}, W: ${item.weight}kg, V: ${item.volume}L)`);
          totalWeight += item.weight;
          totalVolume += item.volume;
          totalSurvivalScore += item.survival_score;
        });
        console.log('\nSummary:');
        console.log(`  Total Weight: ${totalWeight.toFixed(2)}kg`);
        console.log(`  Total Volume: ${totalVolume.toFixed(2)}L`);
        console.log(`  Total Survival Score: ${totalSurvivalScore}`);
      }
    } catch (error: any) {
      console.error(`Error: ${error.message}`);
      process.exit(1);
    }
  });

if (require.main === module) {
  program.parse(process.argv);
}
