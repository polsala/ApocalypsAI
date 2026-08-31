/**
 * @typedef {Object} TemporalEcho
 * @property {string} id - Unique identifier for the echo.
 * @property {number} x - X coordinate (0-1, relative to canvas width).
 * @property {number} y - Y coordinate (0-1, relative to canvas height).
 * @property {number} intensity - How strong the echo is (0-1).
 * @property {number} age - How old the echo is (0-1, 1 being fully faded).
 * @property {number} vx - Velocity in X direction.
 * @property {number} vy - Velocity in Y direction.
 */

const MAX_ECHOES = 50;
const FADE_RATE = 0.005;
const SPAWN_CHANCE = 0.1;

/**
 * Generates a new temporal echo.
 * @returns {TemporalEcho}
 */
function createEcho() {
  return {
    id: Math.random().toString(36).substring(2, 9),
    x: Math.random(),
    y: Math.random(),
    intensity: 0.5 + Math.random() * 0.5, // Start with some intensity
    age: 0, // Start fresh
    vx: (Math.random() - 0.5) * 0.005, // Small random velocity
    vy: (Math.random() - 0.5) * 0.005,
  };
}

/**
 * Updates an existing temporal echo's state.
 * @param {TemporalEcho} echo
 * @returns {TemporalEcho}
 */
function updateEcho(echo) {
  const newEcho = { ...echo };
  newEcho.age += FADE_RATE;
  newEcho.intensity = Math.max(0, newEcho.intensity - FADE_RATE * 0.5); // Fade intensity too
  newEcho.x = (newEcho.x + newEcho.vx + 1) % 1; // Wrap around edges
  newEcho.y = (newEcho.y + newEcho.vy + 1) % 1;
  return newEcho;
}

/**
 * Simulates a new set of temporal echoes.
 * @param {TemporalEcho[]} currentEchoes - The current array of echoes.
 * @returns {TemporalEcho[]}
 */
export function simulateEchoes(currentEchoes) {
  let nextEchoes = currentEchoes
    .map(updateEcho)
    .filter(echo => echo.age < 1 && echo.intensity > 0.05); // Remove faded echoes

  // Add new echoes if below max and random chance hits
  if (nextEchoes.length < MAX_ECHOES && Math.random() < SPAWN_CHANCE) {
    nextEchoes.push(createEcho());
  }

  return nextEchoes;
}

/**
 * Generates initial echoes.
 * @param {number} count
 * @returns {TemporalEcho[]}
 */
export function generateInitialEchoes(count) {
  const echoes = [];
  for (let i = 0; i < count; i++) {
    echoes.push(createEcho());
  }
  return echoes;
}
