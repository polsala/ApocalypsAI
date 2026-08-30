import { program } from 'commander';
import * as fs from 'fs';
import * as path from 'path';
import { calculateAlignment } from './cosmicAligner';
import { CosmicEntity } from './types';

program
  .name('cosmic-clutter-aligner')
  .description('Align your digital clutter with the cosmos.')
  .version('0.1.0');

program
  .option('-f, --file <path...>', 'Specify file paths to analyze')
  .option('-t, --task <description...>', 'Specify task descriptions to analyze')
  .option('-b, --tab <description...>', 'Specify browser tab descriptions to analyze');

program.parse(process.argv);

const options = program.opts();

async function getFileMetadata(filePath: string): Promise<{ lastModified: Date; sizeBytes: number } | null> {
  try {
    const stats = await fs.promises.stat(filePath);
    return { lastModified: stats.mtime, sizeBytes: stats.size };
  } catch (error) {
    console.warn(`Warning: Could not read metadata for file '${filePath}'. Using defaults. Error: ${error.message}`);
    return null;
  }
}

async function main() {
  const entities: CosmicEntity[] = [];
  let idCounter = 0;

  if (options.file) {
    for (const filePath of options.file) {
      const metadata = await getFileMetadata(filePath);
      entities.push({
        id: `entity-${idCounter++}`,
        name: path.basename(filePath),
        type: 'file',
        lastModified: metadata?.lastModified,
        sizeBytes: metadata?.sizeBytes
      });
    }
  }

  if (options.task) {
    for (const taskDesc of options.task) {
      entities.push({
        id: `entity-${idCounter++}`,
        name: taskDesc,
        type: 'task',
        // Tasks are assumed to be current, no lastModified unless explicitly provided
        // sizeBytes and keywords can be inferred or added manually if needed
        keywords: taskDesc.toLowerCase().split(/\s+/).filter(word => word.length > 2) // Simple keyword extraction
      });
    }
  }

  if (options.tab) {
    for (const tabDesc of options.tab) {
      entities.push({
        id: `entity-${idCounter++}`,
        name: tabDesc,
        type: 'tab',
        // Tabs are assumed to be current
        keywords: tabDesc.toLowerCase().split(/\s+/).filter(word => word.length > 2)
      });
    }
  }

  if (entities.length === 0) {
    console.log("No entities provided. Use --file, --task, or --tab to specify items.");
    program.help();
    return;
  }

  console.log("\n--- Cosmic Alignment Report ---");
  for (const entity of entities) {
    const aligned = calculateAlignment(entity);
    console.log(`\nEntity: ${aligned.entity.name} (Type: ${aligned.entity.type})`);
    console.log(`  Alignment: ${aligned.alignment} (Score: ${aligned.score})`);
    console.log(`  Guidance: ${aligned.recommendation}`);
  }
  console.log("-------------------------------");
}

main().catch(console.error);
