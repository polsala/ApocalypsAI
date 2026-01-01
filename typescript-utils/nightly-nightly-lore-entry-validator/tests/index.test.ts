import { validateLoreEntry } from '../src/index';
import { LoreEntry } from '../src/schema';

describe('Lore Entry Validator', () => {
  // Mock rationale: Tests operate on in-memory JavaScript objects,
  // not requiring external file system or network interactions.
  // The CLI part that reads files is not directly tested here,
  // only the core validation logic.

  it('should validate a correctly structured lore entry', () => {
    const validEntry: LoreEntry = {
      id: 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
      title: 'The Whispering Monolith',
      category: 'Anomaly',
      description: 'A large, obsidian monolith discovered in Sector Gamma, emitting faint, indecipherable whispers.',
      discoveredBy: 'Scout Unit 7',
      discoveryDate: '2077-10-23T14:30:00Z',
      threatLevel: 4,
      relatedEntries: ['b2c3d4e5-f6a7-8901-2345-67890abcdef0'],
    };
    const result = validateLoreEntry(validEntry);
    expect(result.isValid).toBe(true);
    expect(result.errors).toEqual([]);
    expect(result.data).toEqual(validEntry);
  });

  it('should validate a minimal correctly structured lore entry', () => {
    const minimalEntry: LoreEntry = {
      id: 'f1e2d3c4-b5a6-7890-1234-567890abcdef',
      title: 'Broken Chronometer',
      category: 'Artifact',
      description: 'A non-functional chronometer found near the temporal rift, showing erratic time readings.',
    };
    const result = validateLoreEntry(minimalEntry);
    expect(result.isValid).toBe(true);
    expect(result.errors).toEqual([]);
    expect(result.data).toEqual(minimalEntry);
  });

  it('should reject an entry with a missing required field (id)', () => {
    const invalidEntry = {
      title: 'Missing ID Entry',
      category: 'Event',
      description: 'An event without a proper identifier.',
    };
    const result = validateLoreEntry(invalidEntry);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("id: Required");
  });

  it('should reject an entry with an invalid UUID for id', () => {
    const invalidEntry = {
      id: 'not-a-uuid',
      title: 'Invalid ID Entry',
      category: 'Anomaly',
      description: 'An entry with a malformed ID.',
    };
    const result = validateLoreEntry(invalidEntry);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("id: Lore entry ID must be a valid UUID.");
  });

  it('should reject an entry with a title that is too short', () => {
    const invalidEntry: Partial<LoreEntry> = {
      id: 'c1d2e3f4-a5b6-7890-1234-567890abcdef',
      title: 'Hi', // Too short
      category: 'Person',
      description: 'A person with a short name.',
    };
    const result = validateLoreEntry(invalidEntry);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("title: Title must be at least 3 characters long.");
  });

  it('should reject an entry with an invalid category', () => {
    const invalidEntry = {
      id: 'd1e2f3a4-b5c6-7890-1234-567890abcdef',
      title: 'Unknown Category Item',
      category: 'NonExistentCategory', // Invalid category
      description: 'An item with an unrecognized category.',
    };
    const result = validateLoreEntry(invalidEntry);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("category: Invalid enum value. Expected 'Anomaly' | 'Artifact' | 'Event' | 'Person' | 'Location' | 'Faction' | 'Technology', received 'NonExistentCategory'");
  });

  it('should reject an entry with a description that is too short', () => {
    const invalidEntry: Partial<LoreEntry> = {
      id: 'e1f2a3b4-c5d6-7890-1234-567890abcdef',
      title: 'Short Desc',
      category: 'Location',
      description: 'Short.', // Too short
    };
    const result = validateLoreEntry(invalidEntry);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("description: Description must be at least 10 characters long.");
  });

  it('should reject an entry with an invalid discoveryDate format', () => {
    const invalidEntry: Partial<LoreEntry> = {
      id: 'f1a2b3c4-d5e6-7890-1234-567890abcdef',
      title: 'Bad Date Entry',
      category: 'Event',
      description: 'An event with a malformed date.',
      discoveryDate: '2077-10-23', // Missing time and timezone
    };
    const result = validateLoreEntry(invalidEntry);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("discoveryDate: Discovery date must be a valid ISO 8601 datetime string.");
  });

  it('should reject an entry with a threatLevel out of range (too low)', () => {
    const invalidEntry: Partial<LoreEntry> = {
      id: '1a2b3c4d-e5f6-7890-1234-567890abcdef',
      title: 'Low Threat',
      category: 'Anomaly',
      description: 'An anomaly with a threat level too low.',
      threatLevel: 0, // Out of range
    };
    const result = validateLoreEntry(invalidEntry);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("threatLevel: Number must be greater than or equal to 1");
  });

  it('should reject an entry with a threatLevel out of range (too high)', () => {
    const invalidEntry: Partial<LoreEntry> = {
      id: '2b3c4d5e-f6a7-8901-2345-67890abcdef0',
      title: 'High Threat',
      category: 'Anomaly',
      description: 'An anomaly with a threat level too high.',
      threatLevel: 6, // Out of range
    };
    const result = validateLoreEntry(invalidEntry);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("threatLevel: Number must be less than or equal to 5");
  });

  it('should reject an entry with an unexpected field due to strict schema', () => {
    const invalidEntry = {
      id: '3c4d5e6f-a7b8-9012-3456-7890abcdef01',
      title: 'Extra Field Entry',
      category: 'Technology',
      description: 'An entry with an unexpected field.',
      extraField: 'This should not be here', // Unexpected field
    };
    const result = validateLoreEntry(invalidEntry);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("extraField: Unrecognized key(s) in object: 'extraField'");
  });

  it('should reject an entry with an invalid UUID in relatedEntries', () => {
    const invalidEntry: Partial<LoreEntry> = {
      id: '4d5e6f7a-b8c9-0123-4567-890abcdef012',
      title: 'Related Entry Issue',
      category: 'Event',
      description: 'An event with a malformed related entry ID.',
      relatedEntries: ['valid-uuid-here', 'not-a-uuid-for-related'],
    };
    const result = validateLoreEntry(invalidEntry);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("relatedEntries.1: Related entry ID must be a valid UUID.");
  });
});
