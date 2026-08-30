import { calculateCelestialPositions, determineAlignmentInfluence } from './utils';

/**
 * Simulates fetching celestial data for a given date.
 * # Mock rationale: In a post-apocalyptic setting, real-time astronomical data might be unreliable or unavailable.
 * This utility simulates celestial mechanics deterministically for consistent "predictions" without external dependencies.
 * This ensures tests are offline and repeatable.
 * @param {Date} date - The date for which to fetch data.
 * @returns {Promise<{positions: import('./utils').CelestialBodyPosition[], influences: string[]}>}
 */
export const fetchCelestialData = async (date) => {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 50));

  const positions = calculateCelestialPositions(date);
  const influences = determineAlignmentInfluence(positions);

  return { positions, influences };
};
