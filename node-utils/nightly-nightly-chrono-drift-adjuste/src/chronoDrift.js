/**
 * Calculates the temporal drift and associated messages based on a given seed and current time.
 * @param {number} seed - A numerical seed for deterministic drift calculation.
 * @param {Date} currentTime - The current Date object to base calculations on.
 * @returns {{currentTime: Date, seed: number, adjustmentSeconds: number, adjustedTime: Date, stabilityMessage: string}}
 */
const calculateDrift = (seed, currentTime) => {
  // Whimsical drift calculation based on seed
  // This makes the drift deterministic for a given seed, but appears random over time.
  const driftMagnitude = (seed % 13) - 6; // Results in a value between -6 and +6
  const driftDirection = (seed % 2 === 0) ? 1 : -1; // Alternates positive or negative
  const adjustmentSeconds = driftMagnitude * driftDirection;

  let stabilityMessage;
  if (Math.abs(adjustmentSeconds) <= 1) {
    stabilityMessage = 'Temporal fabric is remarkably stable. Minimal adjustments needed.';
  } else if (Math.abs(adjustmentSeconds) <= 3) {
    stabilityMessage = 'Minor temporal ripples detected. A slight recalibration is advised.';
  } else {
    stabilityMessage = 'Significant chrono-distortion detected! Immediate adjustment recommended to prevent further temporal desynchronization.';
  }

  const adjustedTime = new Date(currentTime.getTime() + adjustmentSeconds * 1000);

  return {
    currentTime,
    seed,
    adjustmentSeconds,
    adjustedTime,
    stabilityMessage
  };
};

module.exports = { calculateDrift };
