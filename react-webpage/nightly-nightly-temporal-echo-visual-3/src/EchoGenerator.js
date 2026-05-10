/**
 * @typedef {Object} EchoData
 * @property {number} offset - Time offset from the input time in seconds.
 * @property {number} intensity - The intensity of the temporal echo (0.0 to 1.0).
 * @property {string} distortionType - The type of temporal distortion.
 */

/**
 * Generates a deterministic array of temporal echo data based on location and time.
 * The generation uses simple hashing and modulo operations to ensure consistency.
 *
 * @param {string} location - The input location string.
 * @param {string} time - The input time string (e.g., '2077-10-23T14:30').
 * @returns {EchoData[]} An array of generated echo data points.
 */
export const generateEchoData = (location, time) => {
  const seedString = `${location}-${time}`;
  let hash = 0;
  for (let i = 0; i < seedString.length; i++) {
    const char = seedString.charCodeAt(i);
    hash = ((hash << 5) - hash) + char; // Simple hash function
    hash |= 0; // Convert to 32bit integer
  }

  const dataPoints = 20; // Number of echo bars to display
  const echoes = [];
  const distortionTypes = ['Chronal Ripple', 'Paradox Pulse', 'Void Whisper'];

  for (let i = 0; i < dataPoints; i++) {
    // Use a combination of hash and index for deterministic but varied results
    const currentSeed = Math.abs(hash + i * 12345) % 1000000;

    const intensity = (Math.sin(currentSeed / 100000) * 0.4 + 0.6); // Range 0.2 to 1.0
    const offset = i - Math.floor(dataPoints / 2); // Centered around 0
    const distortionType = distortionTypes[currentSeed % distortionTypes.length];

    echoes.push({
      offset: offset,
      intensity: parseFloat(intensity.toFixed(2)),
      distortionType: distortionType,
    });
  }

  return echoes;
};
