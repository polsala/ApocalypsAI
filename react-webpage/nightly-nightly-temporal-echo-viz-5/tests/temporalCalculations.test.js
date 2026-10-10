import { calculateImpactRadius } from '../src/utils/temporalCalculations';

describe('temporalCalculations', () => {
  test('calculateImpactRadius returns correct values for various intensities', () => {
    expect(calculateImpactRadius(1)).toBe(1); // Min intensity
    expect(calculateImpactRadius(5)).toBe(5);
    expect(calculateImpactRadius(10)).toBe(10); // Max intensity
  });

  test('calculateImpactRadius clamps values below 1 to 1', () => {
    expect(calculateImpactRadius(0)).toBe(1);
    expect(calculateImpactRadius(-5)).toBe(1);
  });

  test('calculateImpactRadius clamps values above 10 to 10', () => {
    expect(calculateImpactRadius(11)).toBe(10);
    expect(calculateImpactRadius(100)).toBe(10);
  });

  test('calculateImpactRadius handles non-integer inputs by clamping', () => {
    expect(calculateImpactRadius(0.5)).toBe(1);
    expect(calculateImpactRadius(10.5)).toBe(10);
    expect(calculateImpactRadius(7.3)).toBe(7.3); // Should pass through if within range
  });
});
