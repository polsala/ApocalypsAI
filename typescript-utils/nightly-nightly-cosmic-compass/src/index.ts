import { CardinalDirection, CosmicGuidance } from './types';

const GUIDANCE_PHRASES: Record<CardinalDirection, string[]> = {
  N: [
    "Follow the faint echo of the void, where forgotten stars hum.",
    "Seek the path illuminated by the North Star's ancient glow.",
    "Ascend towards the celestial zenith, guided by silent whispers."
  ],
  S: [
    "Descend into the shimmering depths, where new constellations are born.",
    "Embrace the warmth of the Southern Cross, finding comfort in the unknown.",
    "Drift with the cosmic currents, towards the heart of the galactic hum."
  ],
  E: [
    "Greet the dawn of new possibilities, where temporal rifts mend.",
    "Journey with the rising sun, towards the ever-expanding horizon.",
    "Unravel the threads of destiny, where the first light touches."
  ],
  W: [
    "Veer slightly towards the shimmering nebula, seeking nascent truths.",
    "Reflect upon the setting sun, and the wisdom it imparts.",
    "Explore the twilight's edge, where realities softly merge."
  ]
};

/**
 * Generates a whimsical, cosmically-aligned path recommendation.
 * @param direction The cardinal direction (N, S, E, W).
 * @returns A CosmicGuidance object with the direction and a generated message.
 */
export function getCosmicGuidance(direction: CardinalDirection): CosmicGuidance {
  const normalizedDirection = direction.toUpperCase() as CardinalDirection;

  if (!GUIDANCE_PHRASES[normalizedDirection]) {
    throw new Error(`Invalid direction: ${direction}. Please use N, S, E, or W.`);
  }

  // Use a simple pseudo-random selection for whimsy
  const phrases = GUIDANCE_PHRASES[normalizedDirection];
  const randomIndex = Math.floor(Math.random() * phrases.length);
  const message = phrases[randomIndex];

  return {
    direction: normalizedDirection,
    message: `To the ${normalizedDirection}: ${message}`
  };
}

// CLI execution
if (require.main === module) {
  const args = process.argv.slice(2);
  const inputDirection = args[0];

  if (!inputDirection) {
    console.error("Error: Please provide a cardinal direction (N, S, E, W).");
    process.exit(1);
  }

  try {
    const guidance = getCosmicGuidance(inputDirection as CardinalDirection);
    console.log(guidance.message);
  } catch (error: any) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}
