import { prioritizeRipple } from '../src/index';
import { RippleType, Severity, Priority, RippleReport } from '../src/index'; // Import types for better test clarity

// Mock rationale: The `uuidv4` and `Date` objects are not directly used in the `prioritizeRipple` function,
// but are part of the `RippleReport` interface. For testing `prioritizeRipple`, we only need to ensure
// the `type` and `severity` properties are correctly handled. We'll create minimal mock RippleReport objects.

describe('prioritizeRipple', () => {
  // Helper function to create a minimal ripple for testing prioritization
  const createMockRipple = (type: RippleType | string, severity: Severity | string): RippleReport => ({
    id: 'mock-id',
    type: type as RippleType, // Cast for valid cases, allows string for invalid test
    severity: severity as Severity, // Cast for valid cases, allows string for invalid test
    description: 'mock-description',
    location: 'mock-location',
    observedAt: new Date('2023-01-01T00:00:00Z'),
  });

  // Test cases for Critical severity
  test('should return Urgent for Critical severity, regardless of type', () => {
    expect(prioritizeRipple(createMockRipple(RippleType.Temporal, Severity.Critical))).toBe(Priority.Urgent);
    expect(prioritizeRipple(createMockRipple(RippleType.Spatial, Severity.Critical))).toBe(Priority.Urgent);
    expect(prioritizeRipple(createMockRipple(RippleType.Causal, Severity.Critical))).toBe(Priority.Urgent);
  });

  // Test cases for Severe severity
  test('should return High for Severe severity with Causal or Temporal type', () => {
    expect(prioritizeRipple(createMockRipple(RippleType.Causal, Severity.Severe))).toBe(Priority.High);
    expect(prioritizeRipple(createMockRipple(RippleType.Temporal, Severity.Severe))).toBe(Priority.High);
  });

  test('should return Medium for Severe severity with other types', () => {
    expect(prioritizeRipple(createMockRipple(RippleType.Spatial, Severity.Severe))).toBe(Priority.Medium);
    expect(prioritizeRipple(createMockRipple(RippleType.Echo, Severity.Severe))).toBe(Priority.Medium);
    expect(prioritizeRipple(createMockRipple(RippleType.RealityDistortion, Severity.Severe))).toBe(Priority.Medium);
  });

  // Test cases for Moderate severity
  test('should return Medium for Moderate severity with Temporal or RealityDistortion type', () => {
    expect(prioritizeRipple(createMockRipple(RippleType.Temporal, Severity.Moderate))).toBe(Priority.Medium);
    expect(prioritizeRipple(createMockRipple(RippleType.RealityDistortion, Severity.Moderate))).toBe(Priority.Medium);
  });

  test('should return Low for Moderate severity with other types', () => {
    expect(prioritizeRipple(createMockRipple(RippleType.Spatial, Severity.Moderate))).toBe(Priority.Low);
    expect(prioritizeRipple(createMockRipple(RippleType.Causal, Severity.Moderate))).toBe(Priority.Low);
    expect(prioritizeRipple(createMockRipple(RippleType.Echo, Severity.Moderate))).toBe(Priority.Low);
  });

  // Test cases for Minor severity
  test('should return Low for Minor severity, regardless of type', () => {
    expect(prioritizeRipple(createMockRipple(RippleType.Temporal, Severity.Minor))).toBe(Priority.Low);
    expect(prioritizeRipple(createMockRipple(RippleType.Spatial, Severity.Minor))).toBe(Priority.Low);
    expect(prioritizeRipple(createMockRipple(RippleType.Causal, Severity.Minor))).toBe(Priority.Low);
  });

  // Edge case: unknown severity (should default to Low)
  test('should return Low for unknown severity', () => {
    expect(prioritizeRipple(createMockRipple(RippleType.Temporal, 'UnknownSeverity'))).toBe(Priority.Low);
  });
});
