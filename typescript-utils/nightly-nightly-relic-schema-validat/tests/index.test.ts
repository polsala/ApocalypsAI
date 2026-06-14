import { validateData } from '../src/validator';
import { RELIC_SCHEMAS } from '../src/schemas';
import * as fs from 'fs'; // Import fs to mock it

// Mock rationale: fs.readFileSync is mocked to prevent actual file system access during tests,
// ensuring tests are deterministic and run offline. This allows simulating various data file
// contents without relying on external files. The CLI's file reading is implicitly tested
// by ensuring the validator works with parsed JSON, which is what the CLI would provide.
jest.mock('fs', () => ({
  readFileSync: jest.fn(),
}));

describe('Relic Schema Validator', () => {
  beforeEach(() => {
    // Clear mock calls before each test
    (fs.readFileSync as jest.Mock).mockClear();
  });

  it('should validate valid ScavengedLog data', () => {
    const data = {
      timestamp: '2077-10-23T14:30:00Z',
      level: 'INFO',
      message: 'Found a shiny new bolt.',
      source: 'Sector 7G'
    };
    const result = validateData('ScavengedLog', data);
    expect(result.isValid).toBe(true);
    expect(result.errors).toEqual([]);
  });

  it('should invalidate ScavengedLog data with missing required field', () => {
    const data = {
      timestamp: '2077-10-23T14:30:00Z',
      level: 'INFO',
      // message is missing
      source: 'Sector 7G'
    };
    const result = validateData('ScavengedLog', data);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("Missing required property: message");
  });

  it('should invalidate ScavengedLog data with wrong type', () => {
    const data = {
      timestamp: '2077-10-23T14:30:00Z',
      level: 123, // Should be string
      message: 'Found a shiny new bolt.',
      source: 'Sector 7G'
    };
    const result = validateData('ScavengedLog', data);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("Property 'level' has incorrect type: expected string, got number");
  });

  it('should validate valid ResourceManifest data', () => {
    const data = {
      resourceId: 'scrap-metal-001',
      quantity: 15,
      location: {
        sector: 'Alpha',
        grid: 'A1'
      },
      scavengerNotes: ['rusty', 'heavy']
    };
    const result = validateData('ResourceManifest', data);
    expect(result.isValid).toBe(true);
    expect(result.errors).toEqual([]);
  });

  it('should invalidate ResourceManifest data with nested missing field', () => {
    const data = {
      resourceId: 'scrap-metal-001',
      quantity: 15,
      location: {
        sector: 'Alpha',
        // grid is missing
      },
      scavengerNotes: ['rusty', 'heavy']
    };
    const result = validateData('ResourceManifest', data);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("Missing required property: location.grid");
  });

  it('should invalidate ResourceManifest data with nested wrong type', () => {
    const data = {
      resourceId: 'scrap-metal-001',
      quantity: 15,
      location: {
        sector: 'Alpha',
        grid: 123 // Should be string
      },
      scavengerNotes: ['rusty', 'heavy']
    };
    const result = validateData('ResourceManifest', data);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("Property 'location.grid' has incorrect type: expected string, got number");
  });

  it('should return errors for unknown schema', () => {
    const data = { some: 'data' };
    const result = validateData('UnknownSchema', data);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("Unknown schema: UnknownSchema");
  });

  it('should allow extra properties not defined in schema', () => {
    const data = {
      timestamp: '2077-10-23T14:30:00Z',
      level: 'INFO',
      message: 'Found a shiny new bolt.',
      source: 'Sector 7G',
      extraField: 'this is fine'
    };
    const result = validateData('ScavengedLog', data);
    expect(result.isValid).toBe(true);
    expect(result.errors).toEqual([]);
  });

  it('should handle empty object for a schema with properties', () => {
    const data = {};
    const result = validateData('ScavengedLog', data);
    expect(result.isValid).toBe(false);
    expect(result.errors).toEqual([
      "Missing required property: timestamp",
      "Missing required property: level",
      "Missing required property: message",
      "Missing required property: source"
    ]);
  });

  it('should handle null data', () => {
    const data = null;
    const result = validateData('ScavengedLog', data);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("Expected object at path '', but got object"); // typeof null is 'object'
  });

  it('should handle non-object data', () => {
    const data = "not an object";
    const result = validateData('ScavengedLog', data);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("Expected object at path '', but got string");
  });
});
