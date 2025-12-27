/**
 * @file AnomalyDetector.test.js
 * @description Unit tests for AnomalyDetector utility functions.
 */

import { shouldTriggerAnomaly, getAnomalyDuration } from '../src/AnomalyDetector';

describe('AnomalyDetector', () => {
  const originalMathRandom = Math.random;

  beforeEach(() => {
    // Reset Math.random before each test
    Math.random = originalMathRandom;
  });

  afterAll(() => {
    // Restore original Math.random after all tests
    Math.random = originalMathRandom;
  });

  describe('shouldTriggerAnomaly', () => {
    it('should return false if frequency is 0 or less', () => {
      expect(shouldTriggerAnomaly(0)).toBe(false);
      expect(shouldTriggerAnomaly(-10)).toBe(false);
    });

    it('should return true when Math.random is less than scaled frequency', () => {
      // Mock rationale: Controls random number generation for deterministic testing of anomaly triggers.
      Math.random = jest.fn(() => 0.01); // A small number
      expect(shouldTriggerAnomaly(100)).toBe(true); // scaledFrequency will be 100 * 0.05 = 5, capped at 1. 0.01 < 1 is true.
      expect(shouldTriggerAnomaly(1)).toBe(true);   // scaledFrequency will be 1 * 0.05 = 0.05. 0.01 < 0.05 is true.
    });

    it('should return false when Math.random is greater than or equal to scaled frequency', () => {
      // Mock rationale: Controls random number generation for deterministic testing of anomaly triggers.
      Math.random = jest.fn(() => 0.06); // A number greater than 0.05
      expect(shouldTriggerAnomaly(1)).toBe(false); // scaledFrequency will be 1 * 0.05 = 0.05. 0.06 < 0.05 is false.

      Math.random = jest.fn(() => 0.9); // A large number
      expect(shouldTriggerAnomaly(10)).toBe(false); // scaledFrequency will be 10 * 0.05 = 0.5. 0.9 < 0.5 is false.
    });

    it('should cap the scaled frequency at 1', () => {
      // Mock rationale: Controls random number generation for deterministic testing of anomaly triggers.
      Math.random = jest.fn(() => 0.5); // Should be less than 1
      expect(shouldTriggerAnomaly(100)).toBe(true); // scaledFrequency is 100 * 0.05 = 5, capped at 1. 0.5 < 1 is true.
    });
  });

  describe('getAnomalyDuration', () => {
    it('should return a number within the expected range (500-1500ms)', () => {
      // Mock rationale: Controls random number generation for deterministic testing of anomaly durations.
      Math.random = jest.fn(() => 0); // Should result in min duration
      expect(getAnomalyDuration()).toBe(500);

      Math.random = jest.fn(() => 0.9999999999999999); // Should result in max duration
      expect(getAnomalyDuration()).toBe(1500);

      // Test a few random values in between
      Math.random = jest.fn(() => 0.5);
      const duration1 = getAnomalyDuration();
      expect(duration1).toBeGreaterThanOrEqual(500);
      expect(duration1).toBeLessThanOrEqual(1500);

      Math.random = jest.fn(() => 0.25);
      const duration2 = getAnomalyDuration();
      expect(duration2).toBeGreaterThanOrEqual(500);
      expect(duration2).toBeLessThanOrEqual(1500);
    });
  });
});
