/**
 * Calculates the impact radius of a temporal echo based on its intensity.
 * @param {number} intensity - The intensity of the echo (1-10).
 * @returns {number} The impact radius in kilometers.
 */
export function calculateImpactRadius(intensity) {
  // Whimsical formula: a base radius plus a multiplier based on intensity.
  // Max intensity (10) gives 10km radius, Min intensity (1) gives 1km radius.
  return Math.max(1, Math.min(10, intensity));
}
