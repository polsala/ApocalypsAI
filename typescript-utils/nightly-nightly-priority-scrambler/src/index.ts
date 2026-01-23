import { readFileSync } from 'fs';
import { Item, Factor, Config, PrioritizedItem } from './types';

// Simple argument parser
function parseArgs(args: string[]): { itemsPath: string; configPath: string } {
  let itemsPath = '';
  let configPath = '';
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--items' && args[i + 1]) {
      itemsPath = args[++i];
    } else if (args[i] === '--config' && args[i + 1]) {
      configPath = args[++i];
    }
  }
  if (!itemsPath || !configPath) {
    console.error('Usage: ts-node src/index.ts --items <items.json> --config <config.json>');
    process.exit(1);
  }
  return { itemsPath, configPath };
}

export function loadJson<T>(filePath: string): T {
  try {
    const content = readFileSync(filePath, 'utf8');
    return JSON.parse(content) as T;
  } catch (error) {
    console.error(`Error loading ${filePath}:`, error instanceof Error ? error.message : String(error));
    process.exit(1);
  }
}

export function calculateScore(item: Item, config: Config): PrioritizedItem {
  let score = item.basePriority ?? config.defaultBasePriority;
  const rationale: string[] = [`Base priority: ${score}`];

  for (const factor of config.factors) {
    const matchedKeywords = factor.keywords.filter(keyword =>
      item.name.toLowerCase().includes(keyword.toLowerCase()) ||
      item.description?.toLowerCase().includes(keyword.toLowerCase()) ||
      item.tags?.some(tag => tag.toLowerCase().includes(keyword.toLowerCase()))
    );

    if (matchedKeywords.length > 0) {
      const impact = factor.weight * matchedKeywords.length; // More matches = higher impact
      if (factor.type === 'positive') {
        score += impact;
        rationale.push(`+${impact.toFixed(2)} from "${factor.name}" (keywords: ${matchedKeywords.join(', ')})`);
      } else {
        score -= impact;
        rationale.push(`-${impact.toFixed(2)} from "${factor.name}" (keywords: ${matchedKeywords.join(', ')})`);
      }
    }
  }

  return { item, score: parseFloat(score.toFixed(2)), rationale };
}

function main() {
  const { itemsPath, configPath } = parseArgs(process.argv.slice(2));

  const items = loadJson<Item[]>(itemsPath);
  const config = loadJson<Config>(configPath);

  const prioritizedItems = items.map(item => calculateScore(item, config));

  prioritizedItems.sort((a, b) => b.score - a.score); // Sort descending

  console.log('--- Apocalyptic Priority Scramble Results ---');
  prioritizedItems.forEach((pItem, index) => {
    console.log(`\n${index + 1}. ${pItem.item.name} (Score: ${pItem.score})`);
    if (pItem.item.description) {
      console.log(`   Description: ${pItem.item.description}`);
    }
    console.log(`   Rationale:`);
    pItem.rationale.forEach(r => console.log(`     - ${r}`));
  });
  console.log('\n-------------------------------------------');
}

// Only run main if this script is executed directly
if (require.main === module) {
  main();
}
