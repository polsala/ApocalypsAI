import { Choice, CosmicInfluence, WeaverConfig } from './types';

// Simple Linear Congruential Generator for deterministic randomness
class SeededRandom {
  private seed: number;
  private readonly m = 0x80000000; // 2^31
  private readonly a = 1103515245;
  private readonly c = 12345;

  constructor(seed: string) {
    this.seed = this.hashString(seed);
  }

  private hashString(str: string): number {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash |= 0; // Convert to 32bit integer
    }
    return Math.abs(hash); // Ensure positive
  }

  next(): number {
    this.seed = (this.a * this.seed + this.c) % this.m;
    return this.seed / (this.m - 1);
  }
}

export function weaveCosmicChoice(config: WeaverConfig): Choice | null {
  if (!config.choices || config.choices.length === 0) {
    return null;
  }

  const seededRandom = new SeededRandom(config.seed || 'apocalypsai-default-seed');

  let totalWeightedScore = 0;
  const choicesWithScores = config.choices.map(choice => {
    let score = choice.weight !== undefined ? choice.weight : 1; // Base weight

    // Apply cosmic influences
    if (config.influences && choice.tags) {
      for (const influence of config.influences) {
        if (choice.tags.includes(influence.tag)) {
          score *= influence.multiplier;
        }
      }
    }
    totalWeightedScore += score;
    return { choice, score };
  });

  // If all scores are zero or negative, fall back to uniform random
  if (totalWeightedScore <= 0) {
    const randomIndex = Math.floor(seededRandom.next() * config.choices.length);
    return config.choices[randomIndex];
  }

  // Select a choice based on weighted scores
  let randomPoint = seededRandom.next() * totalWeightedScore;
  for (const { choice, score } of choicesWithScores) {
    randomPoint -= score;
    if (randomPoint <= 0) {
      return choice;
    }
  }

  // Fallback in case of floating point inaccuracies or edge cases
  return choicesWithScores[choicesWithScores.length - 1].choice;
}
