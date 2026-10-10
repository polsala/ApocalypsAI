import { CosmicChoreConfig, CosmicChoreSuggestion } from './types';

// Simple seeded random number generator (Linear Congruential Generator)
class SeededRandom {
  private seed: number;

  constructor(seed: number) {
    // Ensure seed is positive and within a reasonable range for LCG
    this.seed = seed % 2147483647;
    if (this.seed <= 0) this.seed += 2147483646;
  }

  next(): number {
    // LCG formula: X_n+1 = (a * X_n + c) mod m
    // Here, a=16807, c=0, m=2147483647 (2^31 - 1, a Mersenne prime)
    this.seed = (this.seed * 16807) % 2147483647;
    return (this.seed - 1) / 2147483646; // Map to [0, 1)
  }
}

export function chooseCosmicChore(config: CosmicChoreConfig): CosmicChoreSuggestion {
  const { tasks, seed } = config;

  if (tasks.length === 0) {
    return {
      chosenTask: "Contemplate the infinite void.",
      rationale: "The cosmos offers no specific guidance when your path is empty. Seek inner wisdom.",
      cosmicAlignmentScore: 0,
    };
  }

  const effectiveSeed = seed !== undefined ? seed : Date.now();
  const rng = new SeededRandom(effectiveSeed);

  const randomIndex = Math.floor(rng.next() * tasks.length);
  const chosenTask = tasks[randomIndex];
  const cosmicAlignmentScore = parseFloat(rng.next().toFixed(4)); // A "score" for whimsy

  const rationales = [
    `The celestial currents whisper this task is aligned with your immediate destiny.`,
    `A faint shimmer in the astral plane points to this as your next endeavor.`,
    `By the decree of the cosmic dust bunnies, this chore awaits your touch.`,
    `The stars have aligned, and this task has been illuminated for you.`,
    `A ripple in the fabric of spacetime suggests this is the optimal path.`,
    `The quantum fluctuations of the universe demand your attention here.`,
    `Observe the cosmic dance; this task is its next step for you.`,
    `The Great Beyond has nudged this task into your awareness.`,
    `Your cosmic energy field resonates most strongly with this action.`,
    `A fleeting vision of a sentient nebula confirmed this choice.`,
    `The cosmic librarian has stamped this task as 'urgently recommended'.`,
    `An echo from a parallel dimension insists upon this course of action.`,
    `The universal algorithm has computed this as your most harmonious next step.`
  ];

  const rationaleIndex = Math.floor(rng.next() * rationales.length);
  const rationale = rationales[rationaleIndex];

  return {
    chosenTask,
    rationale,
    cosmicAlignmentScore,
  };
}
