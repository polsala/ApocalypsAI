/**
 * @typedef {Object} CelestialBodyPosition
 * @property {string} name - The name of the celestial body.
 * @property {number} angle - The angle in degrees (0-360) representing its position.
 * @property {string} color - The color associated with the body.
 */

const CELESTIAL_BODIES = [
  { name: 'Solara', color: '#FFD700', factor: 1.2 },
  { name: 'Lunaris', color: '#C0C0C0', factor: 0.8 },
  { name: 'Terra Nova', color: '#00FF7F', factor: 1.5 },
  { name: 'Aetheria', color: '#8A2BE2', factor: 0.5 },
  { name: 'Umbra', color: '#4B0082', factor: 1.0 }
];

const ANGLE_THRESHOLD_CLOSE = 15; // Degrees for conjunction
const ANGLE_THRESHOLD_OPPOSITION = 15; // Degrees around 180 for opposition
const ANGLE_THRESHOLD_SQUARE = 15; // Degrees around 90 or 270 for square
const ANGLE_THRESHOLD_TRINE = 15; // Degrees around 120 or 240 for trine

/**
 * Deterministically calculates the positions of celestial bodies based on a given date.
 * The positions are simulated and consistent for any given date.
 * @param {Date} date - The date for which to calculate positions.
 * @returns {CelestialBodyPosition[]}
 */
export const calculateCelestialPositions = (date) => {
  const dayOfYear = Math.floor((date - new Date(date.getFullYear(), 0, 0)) / (1000 * 60 * 60 * 24));
  const seed = date.getFullYear() * 365 + dayOfYear; // A simple deterministic seed

  return CELESTIAL_BODIES.map((body, index) => {
    // Use a unique offset and factor for each body to ensure distinct movements
    const rawAngle = (seed * body.factor + index * 100) % 360;
    const angle = (rawAngle + 360) % 360; // Ensure angle is positive
    return { ...body, angle };
  });
};

/**
 * Determines whimsical alignment influences based on celestial body positions.
 * @param {CelestialBodyPosition[]} positions - Array of celestial body positions.
 * @returns {string[]}
 */
export const determineAlignmentInfluence = (positions) => {
  const influences = [];

  // Helper to check if two angles are within a threshold
  const areAnglesClose = (angle1, angle2, threshold) => {
    const diff = Math.abs(angle1 - angle2);
    return diff <= threshold || diff >= (360 - threshold);
  };

  // Helper to check if two angles are in opposition
  const areAnglesOpposition = (angle1, angle2, threshold) => {
    const diff = Math.abs(angle1 - angle2);
    return areAnglesClose(diff, 180, threshold);
  };

  // Helper to check if two angles are in square
  const areAnglesSquare = (angle1, angle2, threshold) => {
    const diff = Math.abs(angle1 - angle2);
    return areAnglesClose(diff, 90, threshold) || areAnglesClose(diff, 270, threshold);
  };

  for (let i = 0; i < positions.length; i++) {
    for (let j = i + 1; j < positions.length; j++) {
      const body1 = positions[i];
      const body2 = positions[j];

      if (areAnglesClose(body1.angle, body2.angle, ANGLE_THRESHOLD_CLOSE)) {
        influences.push(`${body1.name}-${body2.name} Conjunction: A day of heightened emotional resonance and potential resource discovery!`);
      } else if (areAnglesOpposition(body1.angle, body2.angle, ANGLE_THRESHOLD_OPPOSITION)) {
        influences.push(`${body1.name}-${body2.name} Opposition: Expect challenges in communication, but breakthroughs in innovation!`);
      } else if (areAnglesSquare(body1.angle, body2.angle, ANGLE_THRESHOLD_SQUARE)) {
        influences.push(`${body1.name}-${body2.name} Square: A period of introspection, perhaps revealing hidden truths or forgotten caches.`);
      }
    }
  }

  // Check for Trine (three bodies roughly 120 degrees apart)
  if (positions.length >= 3) {
    for (let i = 0; i < positions.length; i++) {
      for (let j = i + 1; j < positions.length; j++) {
        for (let k = j + 1; k < positions.length; k++) {
          const b1 = positions[i].angle;
          const b2 = positions[j].angle;
          const b3 = positions[k].angle;

          const diff12 = Math.abs(b1 - b2);
          const diff23 = Math.abs(b2 - b3);
          const diff31 = Math.abs(b3 - b1);

          // Check for approximate 120 degree separation (trine aspect)
          const isTrine = (
            (areAnglesClose(diff12, 120, ANGLE_THRESHOLD_TRINE) || areAnglesClose(diff12, 240, ANGLE_THRESHOLD_TRINE)) &&
            (areAnglesClose(diff23, 120, ANGLE_THRESHOLD_TRINE) || areAnglesClose(diff23, 240, ANGLE_THRESHOLD_TRINE)) &&
            (areAnglesClose(diff31, 120, ANGLE_THRESHOLD_TRINE) || areAnglesClose(diff31, 240, ANGLE_THRESHOLD_TRINE))
          );

          if (isTrine) {
            influences.push(`Grand Trine (${positions[i].name}, ${positions[j].name}, ${positions[k].name}): Harmonious energies abound, perfect for collaborative efforts!`);
          }
        }
      }
    }
  }

  if (influences.length === 0) {
    influences.push("The cosmos hums a neutral tune. Proceed with cautious optimism.");
  }

  return influences;
};
