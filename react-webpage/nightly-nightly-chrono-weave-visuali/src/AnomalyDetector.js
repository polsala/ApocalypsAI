/**
 * @file AnomalyDetector.js
 * @description Utility functions for simulating anomaly detection in chrono-threads.
 */

/**
 * Determines if an anomaly should be triggered based on a given frequency.
 * @param {number} frequency - A value between 0 and 1, representing the probability of an anomaly.
 * @returns {boolean} True if an anomaly should be triggered, false otherwise.
 */
export const shouldTriggerAnomaly = (frequency) => {
  if (frequency <= 0) return false;
  // Scale frequency to be more sensitive for visual effect
  const scaledFrequency = Math.min(1, frequency * 0.05); // Adjust multiplier for desired anomaly rate
  return Math.random() < scaledFrequency;
};

/**
 * Returns a random duration for an anomaly in milliseconds.
 * @returns {number} The duration of the anomaly.
 */
export const getAnomalyDuration = () => {
  return Math.floor(Math.random() * (1500 - 500 + 1)) + 500; // Between 500ms and 1500ms
};
