import * as fs from 'fs';
import * as path from 'path';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';
import { ChronoShard, DistortionLevel, Urgency, distortionLevelOrder, urgencyOrder } from './chronoShard';

/**
 * Loads chrono shards from a specified JSON file.
 * @param filePath The path to the JSON file.
 * @returns An array of ChronoShard objects.
 * @throws Error if the file does not exist or is malformed.
 */
function loadShards(filePath: string): ChronoShard[] {
  const fullPath = path.resolve(filePath);
  if (!fs.existsSync(fullPath)) {
    throw new Error(`File not found: ${fullPath}`);
  }
  const fileContent = fs.readFileSync(fullPath, 'utf-8');
  const shards: ChronoShard[] = JSON.parse(fileContent);
  // Basic validation for each shard
  for (const shard of shards) {
    if (!shard.id || !shard.timestamp || !shard.event || !shard.distortionLevel || !shard.urgency || !Array.isArray(shard.tags)) {
      console.warn(`Warning: Malformed shard found, skipping or processing with potential issues: ${JSON.stringify(shard)}`);
      // Depending on strictness, one might throw an error here or filter out malformed shards.
      // For this utility, we'll log a warning and proceed.
    }
  }
  return shards;
}

/**
 * Sorts an array of ChronoShard objects based on a specified field and order.
 * @param shards The array of shards to sort.
 * @param sortBy The field to sort by ('urgency', 'distortionLevel', 'timestamp').
 * @param order The sort order ('asc' for ascending, 'desc' for descending).
 * @returns A new array of sorted ChronoShard objects.
 */
function sortShards(
  shards: ChronoShard[],
  sortBy: 'urgency' | 'distortionLevel' | 'timestamp' = 'timestamp',
  order: 'asc' | 'desc' = 'asc'
): ChronoShard[] {
  return [...shards].sort((a, b) => {
    let comparison = 0;
    if (sortBy === 'urgency') {
      comparison = urgencyOrder[a.urgency] - urgencyOrder[b.urgency];
    } else if (sortBy === 'distortionLevel') {
      comparison = distortionLevelOrder[a.distortionLevel] - distortionLevelOrder[b.distortionLevel];
    } else if (sortBy === 'timestamp') {
      comparison = new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime();
    }

    return order === 'asc' ? comparison : -comparison;
  });
}

/**
 * Filters an array of ChronoShard objects by a specific tag.
 * @param shards The array of shards to filter.
 * @param tag The tag to filter by. If undefined, all shards are returned.
 * @returns A new array of filtered ChronoShard objects.
 */
function filterShards(shards: ChronoShard[], tag?: string): ChronoShard[] {
  if (!tag) {
    return shards;
  }
  return shards.filter(shard => shard.tags.includes(tag));
}

/**
 * Main function to parse CLI arguments, load, filter, and sort chrono shards.
 */
async function main() {
  const argv = await yargs(hideBin(process.argv))
    .option('file', {
      alias: 'f',
      type: 'string',
      description: 'Path to the JSON file containing chrono shards',
      demandOption: true,
    })
    .option('sort-by', {
      alias: 's',
      type: 'string',
      choices: ['urgency', 'distortionLevel', 'timestamp'],
      default: 'timestamp',
      description: 'Field to sort shards by',
    })
    .option('order', {
      alias: 'o',
      type: 'string',
      choices: ['asc', 'desc'],
      default: 'asc',
      description: 'Sort order (ascending or descending)',
    })
    .option('filter-tag', {
      alias: 't',
      type: 'string',
      description: 'Filter shards by a specific tag',
    })
    .help()
    .alias('h', 'help')
    .parse();

  try {
    let shards = loadShards(argv.file);
    shards = filterShards(shards, argv.filterTag);
    shards = sortShards(shards, argv.sortBy as 'urgency' | 'distortionLevel' | 'timestamp', argv.order as 'asc' | 'desc');

    console.log(JSON.stringify(shards, null, 2));
  } catch (error: any) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

// Only run main if this script is executed directly
if (require.main === module) {
  main();
}

// Export functions for testing purposes
export { loadShards, sortShards, filterShards };
