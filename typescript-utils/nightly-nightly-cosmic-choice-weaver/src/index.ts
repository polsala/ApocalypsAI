import { readFileSync } from 'fs';
import { join } from 'path';
import { Choice, CosmicInfluence, WeaverConfig } from './types';
import { weaveCosmicChoice } from './weaver';

function loadConfig(configPath: string): WeaverConfig {
  try {
    const rawConfig = readFileSync(configPath, 'utf-8');
    const config = JSON.parse(rawConfig);

    // Basic validation
    if (!Array.isArray(config.choices)) {
      throw new Error('Config must contain a "choices" array.');
    }
    return config as WeaverConfig;
  } catch (error: any) {
    console.error(`Error loading or parsing config file at ${configPath}: ${error.message}`);
    process.exit(1);
  }
}

function main() {
  const args = process.argv.slice(2);
  let configPath: string | undefined;
  let seed: string | undefined;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--config' && args[i + 1]) {
      configPath = args[++i];
    } else if (args[i] === '--seed' && args[i + 1]) {
      seed = args[++i];
    } else if (args[i] === '--help' || args[i] === '-h') {
      console.log(`\nUsage: nightly-cosmic-choice-weaver [options]\n\nA type-safe CLI tool that helps make decisions by weaving cosmic suggestions from a predefined list of options.\n\nOptions:\n  --config <path>  Path to a JSON configuration file containing choices and influences.\n                   Defaults to a built-in example if not provided.\n  --seed <string>  A string seed for deterministic choice weaving.\n  --help, -h       Show this help message.\n\nExample config.json:\n{\n  "choices": [\n    { "id": "1", "name": "Explore the Whispering Wastes", "tags": ["adventure", "risky"] },\n    { "id": "2", "name": "Refactor the Temporal Anomaly Detector", "tags": ["productive", "safe"] },\n    { "id": "3", "name": "Brew a Calming Herbal Infusion", "tags": ["relaxing", "safe"] }\n  ],\n  "influences": [\n    { "tag": "risky", "multiplier": 0.5 },\n    { "tag": "productive", "multiplier": 1.8 }\n  ]\n}\n      `);
      process.exit(0);
    }
  }

  let config: WeaverConfig;
  if (configPath) {
    config = loadConfig(configPath);
  } else {
    // Default example config
    config = {
      choices: [
        { id: '1', name: 'Explore the Whispering Wastes', description: 'Seek out new resources and dangers.', tags: ['adventure', 'risky'] },
        { id: '2', name: 'Refactor the Temporal Anomaly Detector', description: 'Improve the core systems for future stability.', tags: ['productive', 'safe'] },
        { id: '3', name: 'Brew a Calming Herbal Infusion', description: 'Relax and recharge after a long cycle.', tags: ['relaxing', 'safe'] },
        { id: '4', name: 'Organize the Survival Cache', description: 'Ensure all supplies are accounted for and secure.', tags: ['productive', 'safe'] },
        { id: '5', name: 'Decipher Ancient Void Whispers', description: 'Uncover forgotten knowledge, or madness.', tags: ['mystery', 'risky'] }
      ],
      influences: [
        { tag: 'risky', multiplier: 0.7 },
        { tag: 'productive', multiplier: 1.5 },
        { tag: 'relaxing', multiplier: 1.2 }
      ]
    };
  }

  if (seed) {
    config.seed = seed;
  }

  const chosen = weaveCosmicChoice(config);

  if (chosen) {
    console.log(`\n✨ The Cosmic Choice Weaver has spoken! ✨`);
    console.log(`\nYour Stellar Alignment suggests:`);
    console.log(`  \"${chosen.name}\"`);
    if (chosen.description) {
      console.log(`  ${chosen.description}`);
    }
    if (chosen.tags && chosen.tags.length > 0) {
      console.log(`  (Tags: ${chosen.tags.join(', ')})`);
    }
    console.log('\nMay your path be clear, wanderer.\n');
  } else {
    console.log('The Cosmic Choice Weaver found no choices to weave. Perhaps the void is truly empty.');
  }
}

main();
