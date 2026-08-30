const cosmicPhrases = require('./cosmicPhrases');

/**
 * Selects a task based on weighted probabilities.
 * @param {Array<{name: string, weight: number}>} tasks - List of tasks with names and weights.
 * @param {function} randomFn - A function that returns a random number between 0 (inclusive) and 1 (exclusive).
 * @returns {string|null} The name of the selected task, or null if no tasks.
 */
function selectWeightedTask(tasks, randomFn = Math.random) {
  if (!tasks || tasks.length === 0) {
    return null;
  }

  const totalWeight = tasks.reduce((sum, task) => sum + (task.weight || 1), 0);
  let randomPoint = randomFn() * totalWeight;

  for (const task of tasks) {
    const weight = task.weight || 1;
    if (randomPoint < weight) {
      return task.name;
    }
    randomPoint -= weight;
  }

  // Fallback in case of floating point inaccuracies or if randomPoint is exactly totalWeight
  return tasks[tasks.length - 1].name;
}

/**
 * Generates a random cosmic alignment phrase.
 * @param {function} randomFn - A function that returns a random number between 0 (inclusive) and 1 (exclusive).
 * @returns {string} A cosmic alignment phrase.
 */
function getCosmicAlignment(randomFn = Math.random) {
  const index = Math.floor(randomFn() * cosmicPhrases.alignments.length);
  return cosmicPhrases.alignments[index];
}

/**
 * Generates a random cosmic introduction phrase.
 * @param {function} randomFn - A function that returns a random number between 0 (inclusive) and 1 (exclusive).
 * @returns {string} A cosmic introduction phrase.
 */
function getCosmicIntroduction(randomFn = Math.random) {
  const index = Math.floor(randomFn() * cosmicPhrases.introductions.length);
  return cosmicPhrases.introductions[index];
}

/**
 * Generates a random cosmic conclusion phrase.
 * @param {function} randomFn - A function that returns a random number between 0 (inclusive) and 1 (exclusive).
 * @returns {string} A cosmic conclusion phrase.
 */
function getCosmicConclusion(randomFn = Math.random) {
  const index = Math.floor(randomFn() * cosmicPhrases.conclusions.length);
  return cosmicPhrases.conclusions[index];
}

module.exports = {
  selectWeightedTask,
  getCosmicAlignment,
  getCosmicIntroduction,
  getCosmicConclusion
};
