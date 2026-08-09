import * as fs from 'fs';
import * as path from 'path';
import { Chore, CosmicInfluence, AssignedChore } from './types';

// --- Configuration for Cosmic Influences ---
const COSMIC_INFLUENCES: CosmicInfluence[] = [
  {
    name: "Solar Flare Surge",
    modifier: 1.2,
    favoredTags: ["physical", "danger"],
    hinderedTags: ["mental", "logistics"],
    message: "A surge of solar energy invigorates the body but clouds the mind. Embrace the physical challenges!"
  },
  {
    name: "Lunar Lull",
    modifier: 0.9,
    favoredTags: ["maintenance", "crafting"],
    hinderedTags: ["outdoor", "danger"],
    message: "The moon's gentle pull encourages meticulous work and quiet focus. Avoid the harsh outdoors."
  },
  {
    name: "Void Whisper",
    modifier: 0.8,
    favoredTags: ["mental", "logistics"],
    hinderedTags: ["physical", "danger"],
    message: "The void whispers secrets of efficiency. Focus your mind, not your muscle."
  },
  {
    name: "Stardust Shower",
    modifier: 1.0,
    favoredTags: ["farming", "hygiene"],
    hinderedTags: [],
    message: "A shower of stardust brings a touch of renewal. Nurture growth and cleanliness."
  },
  {
    name: "Temporal Ripple",
    modifier: 1.1,
    favoredTags: ["security", "outdoor"],
    hinderedTags: ["maintenance"],
    message: "Time itself feels a bit off. Be vigilant and adaptable, especially outside the shelter."
  }
];

/**
 * Generates a random cosmic influence for the day.
 * @returns A random CosmicInfluence object.
 */
export function generateCosmicInfluence(): CosmicInfluence {
  const randomIndex = Math.floor(Math.random() * COSMIC_INFLUENCES.length);
  return COSMIC_INFLUENCES[randomIndex];
}

/**
 * Assigns a specified number of chores based on available chores and cosmic influence.
 * @param allChores - An array of all possible chores.
 * @param cosmicInfluence - The cosmic influence for the day.
 * @param numChoresToAssign - The desired number of chores to assign.
 * @returns An array of AssignedChore objects.
 */
export function assignChores(
  allChores: Chore[],
  cosmicInfluence: CosmicInfluence,
  numChoresToAssign: number
): AssignedChore[] {
  if (allChores.length === 0) {
    return [];
  }

  const availableChores = [...allChores];
  const assigned: AssignedChore[] = [];

  // Calculate effective difficulty for all chores based on cosmic influence
  const choresWithEffectiveDifficulty = availableChores.map(chore => {
    let effectiveDifficulty = chore.baseDifficulty * cosmicInfluence.modifier;
    let cosmicBoost = false;
    let cosmicHindrance = false;

    // Apply tag-based modifiers
    for (const tag of chore.tags) {
      if (cosmicInfluence.favoredTags.includes(tag)) {
        effectiveDifficulty *= 0.8; // Make favored tags easier
        cosmicBoost = true;
      }
      if (cosmicInfluence.hinderedTags.includes(tag)) {
        effectiveDifficulty *= 1.2; // Make hindered tags harder
        cosmicHindrance = true;
      }
    }

    return {
      ...chore,
      effectiveDifficulty: parseFloat(effectiveDifficulty.toFixed(2)),
      cosmicBoost,
      cosmicHindrance,
    };
  });

  // Sort chores by effective difficulty (easier first) and then randomly for ties
  choresWithEffectiveDifficulty.sort((a, b) => {
    if (a.effectiveDifficulty !== b.effectiveDifficulty) {
      return a.effectiveDifficulty - b.effectiveDifficulty;
    }
    return Math.random() - 0.5; // Random tie-breaker
  });

  // Select the top N chores
  for (let i = 0; i < Math.min(numChoresToAssign, choresWithEffectiveDifficulty.length); i++) {
    assigned.push(choresWithEffectiveDifficulty[i]);
  }

  return assigned;
}

// --- Main execution logic ---
async function main() {
  const args = process.argv.slice(2);
  let choresFilePath: string | undefined;
  let numChores: number = 3;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--chores-file' && args[i + 1]) {
      choresFilePath = args[i + 1];
      i++;
    } else if (args[i] === '--num-chores' && args[i + 1]) {
      numChores = parseInt(args[i + 1], 10);
      i++;
    }
  }

  if (!choresFilePath) {
    console.error('Error: --chores-file argument is required.');
    process.exit(1);
  }

  let allChores: Chore[];
  try {
    const choresRaw = fs.readFileSync(path.resolve(choresFilePath), 'utf8');
    allChores = JSON.parse(choresRaw);
  } catch (error) {
    console.error(`Error reading or parsing chores file: ${error instanceof Error ? error.message : String(error)}`);
    process.exit(1);
  }

  if (!Array.isArray(allChores) || allChores.some(c => !c.id || !c.name || typeof c.baseDifficulty !== 'number' || !Array.isArray(c.tags))) {
    console.error('Error: Chores file must be an array of Chore objects with id, name, baseDifficulty, and tags.');
    process.exit(1);
  }

  const cosmicInfluence = generateCosmicInfluence();
  const assignedChores = assignChores(allChores, cosmicInfluence, numChores);

  console.log('🌌 Nightly Cosmic Chore Chart 🌌\n');
  console.log(`Today's Cosmic Influence: ${cosmicInfluence.name} (Difficulty Modifier: ${cosmicInfluence.modifier})`);
  console.log(`Favored Tags: [${cosmicInfluence.favoredTags.join(', ')}]`);
  console.log(`Hindered Tags: [${cosmicInfluence.hinderedTags.join(', ')}]`);
  console.log(`Cosmic Message: "${cosmicInfluence.message}"\n`);
  console.log('--- Your Assigned Chores ---\n');

  if (assignedChores.length === 0) {
    console.log('No chores could be assigned today. Enjoy the cosmic peace!');
  } else {
    assignedChores.forEach((chore, index) => {
      const boostStatus = chore.cosmicBoost ? ' - ✨ Cosmic Boost!' : chore.cosmicHindrance ? ' - ⚠️ Cosmic Hindrance!' : '';
      console.log(`${index + 1}. ${chore.name} (Effective Difficulty: ${chore.effectiveDifficulty})${boostStatus}`);
    });
  }

  console.log('\nMay your cosmic endeavors be fruitful!');
}

if (require.main === module) {
  main();
}
