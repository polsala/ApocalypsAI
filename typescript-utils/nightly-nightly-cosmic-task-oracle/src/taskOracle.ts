import { Task, PrioritizedTask } from './types';

// # Mock rationale: Math.random and Date are mocked in tests to ensure deterministic results.
// This function encapsulates the "cosmic" logic.
export function getCosmicScore(task: Task, currentDate: Date = new Date()): { score: number; rationale: string } {
  let score = 0;
  const rationaleParts: string[] = [];

  // 1. Base score: description length
  score += task.description.length * 0.1;
  rationaleParts.push(`Base score from description length (${task.description.length}): +${(task.description.length * 0.1).toFixed(1)}`);

  // 2. Keyword bonus
  const lowerDescription = task.description.toLowerCase();
  if (lowerDescription.includes('urgent')) {
    score += 10;
    rationaleParts.push("Contains 'urgent' keyword: +10");
  }
  if (lowerDescription.includes('bug')) {
    score += 8;
    rationaleParts.push("Contains 'bug' keyword: +8");
  }
  if (lowerDescription.includes('feature')) {
    score += 5;
    rationaleParts.push("Contains 'feature' keyword: +5");
  }
  if (lowerDescription.includes('refactor')) {
    score += 3;
    rationaleParts.push("Contains 'refactor' keyword: +3");
  }
  if (lowerDescription.includes('dream')) {
    score += 15; // Whimsical bonus!
    rationaleParts.push("Contains 'dream' keyword (whimsical bonus!): +15");
  }

  // 3. Random "cosmic energy"
  const cosmicEnergy = Math.random() * 20;
  score += cosmicEnergy;
  rationaleParts.push(`Random cosmic energy: +${cosmicEnergy.toFixed(1)}`);

  // 4. "Moon phase" (mocked date)
  const dayOfMonth = currentDate.getDate();
  if (dayOfMonth % 3 === 0) { // Simulating a "new moon" phase
    score += 5;
    rationaleParts.push("Aligned with a 'new moon' phase: +5");
  } else if (dayOfMonth % 7 === 0) { // Simulating a "full moon" phase
    score += 10;
    rationaleParts.push("Aligned with a 'full moon' phase: +10");
  } else {
    score += 2;
    rationaleParts.push("Standard cosmic alignment: +2");
  }

  return { score, rationale: rationaleParts.join(', ') };
}

export function prioritizeTasks(tasks: Task[], currentDate: Date = new Date()): PrioritizedTask[] {
  const prioritized = tasks.map(task => {
    const { score, rationale } = getCosmicScore(task, currentDate);
    return {
      ...task,
      cosmicScore: parseFloat(score.toFixed(2)), // Round for cleaner output
      rationale,
    };
  });

  // Sort in descending order of cosmic score
  return prioritized.sort((a, b) => b.cosmicScore - a.cosmicScore);
}
