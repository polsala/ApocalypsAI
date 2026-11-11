import { isValidChronalEcho, alignChronalEcho, mergeAlignedData, ChronalEcho, AlignedData, AlignmentError } from '../src';

describe('isValidChronalEcho', () => {
  // Mock rationale: All test data is in-memory JavaScript objects, ensuring deterministic and offline tests.

  it('should return true for a valid ChronalEcho', () => {
    const validEcho: ChronalEcho = {
      id: 'test-001',
      timestamp: 1678886400000,
      source: 'Test-Source',
      dataType: 'test_data',
      payload: { key: 'value' },
    };
    expect(isValidChronalEcho(validEcho)).toBe(true);
  });

  it('should return false for missing id', () => {
    const invalidEcho = {
      timestamp: 1678886400000,
      source: 'Test-Source',
      dataType: 'test_data',
      payload: { key: 'value' },
    };
    expect(isValidChronalEcho(invalidEcho)).toBe(false);
  });

  it('should return false for empty id string', () => {
    const invalidEcho = {
      id: '',
      timestamp: 1678886400000,
      source: 'Test-Source',
      dataType: 'test_data',
      payload: { key: 'value' },
    };
    expect(isValidChronalEcho(invalidEcho)).toBe(false);
  });

  it('should return false for missing timestamp', () => {
    const invalidEcho = {
      id: 'test-001',
      source: 'Test-Source',
      dataType: 'test_data',
      payload: { key: 'value' },
    };
    expect(isValidChronalEcho(invalidEcho)).toBe(false);
  });

  it('should return false for non-numeric timestamp', () => {
    const invalidEcho = {
      id: 'test-001',
      timestamp: 'not-a-number',
      source: 'Test-Source',
      dataType: 'test_data',
      payload: { key: 'value' },
    };
    expect(isValidChronalEcho(invalidEcho)).toBe(false);
  });

  it('should return false for missing source', () => {
    const invalidEcho = {
      id: 'test-001',
      timestamp: 1678886400000,
      dataType: 'test_data',
      payload: { key: 'value' },
    };
    expect(isValidChronalEcho(invalidEcho)).toBe(false);
  });

  it('should return false for missing dataType', () => {
    const invalidEcho = {
      id: 'test-001',
      timestamp: 1678886400000,
      source: 'Test-Source',
      payload: { key: 'value' },
    };
    expect(isValidChronalEcho(invalidEcho)).toBe(false);
  });

  it('should return false for missing payload', () => {
    const invalidEcho = {
      id: 'test-001',
      timestamp: 1678886400000,
      source: 'Test-Source',
      dataType: 'test_data',
    };
    expect(isValidChronalEcho(invalidEcho)).toBe(false);
  });

  it('should return false for non-object payload', () => {
    const invalidEcho = {
      id: 'test-001',
      timestamp: 1678886400000,
      source: 'Test-Source',
      dataType: 'test_data',
      payload: 'not-an-object',
    };
    expect(isValidChronalEcho(invalidEcho)).toBe(false);
  });

  it('should return false for null input', () => {
    expect(isValidChronalEcho(null)).toBe(false);
  });

  it('should return false for non-object input', () => {
    expect(isValidChronalEcho('string')).toBe(false);
    expect(isValidChronalEcho(123)).toBe(false);
  });
});

describe('alignChronalEcho', () => {
  // Mock rationale: All test data is in-memory JavaScript objects, ensuring deterministic and offline tests.

  it('should successfully align a valid ChronalEcho', () => {
    const echo: ChronalEcho = {
      id: 'align-001',
      timestamp: 1678886400000,
      source: 'Align-Source',
      dataType: 'generic_data',
      payload: { status: 'active' },
    };
    const aligned = alignChronalEcho(echo);
    expect(aligned).not.toBeInstanceOf(AlignmentError);
    expect((aligned as AlignedData).id).toBe('align-001');
    expect((aligned as AlignedData).alignedTimestamp).toEqual(new Date(1678886400000));
    expect((aligned as AlignedData).originalSource).toBe('Align-Source');
    expect((aligned as AlignedData).alignedType).toBe('generic_data');
    expect((aligned as AlignedData).harmonizedPayload).toEqual({ status: 'active' });
  });

  it('should return AlignmentError for invalid timestamp value', () => {
    const echo: ChronalEcho = {
      id: 'align-002',
      timestamp: NaN, // Invalid timestamp
      source: 'Align-Source',
      dataType: 'generic_data',
      payload: { status: 'active' },
    };
    const aligned = alignChronalEcho(echo);
    expect(aligned).toBeInstanceOf(AlignmentError);
    expect((aligned as AlignmentError).message).toContain('Invalid timestamp value');
    expect((aligned as AlignmentError).echoId).toBe('align-002');
    expect((aligned as AlignmentError).field).toBe('timestamp');
  });

  it('should harmonize sensor_reading payload with string temperature', () => {
    const echo: ChronalEcho = {
      id: 'sensor-001',
      timestamp: 1678886400000,
      source: 'Sensor-Hub',
      dataType: 'sensor_reading',
      payload: { temperature: '22.5', unit: 'C' },
    };
    const aligned = alignChronalEcho(echo) as AlignedData;
    expect(aligned.harmonizedPayload.temperature).toBe(22.5);
    expect(typeof aligned.harmonizedPayload.temperature).toBe('number');
  });

  it('should harmonize resource_report payload with string quantity', () => {
    const echo: ChronalEcho = {
      id: 'resource-001',
      timestamp: 1678886400000,
      source: 'Scavenger-Log',
      dataType: 'resource_report',
      payload: { resource: 'Water', quantity: '15', location: 'Sector A' },
    };
    const aligned = alignChronalEcho(echo) as AlignedData;
    expect(aligned.harmonizedPayload.quantity).toBe(15);
    expect(typeof aligned.harmonizedPayload.quantity).toBe('number');
  });

  it('should not alter already numeric payload values', () => {
    const echo: ChronalEcho = {
      id: 'sensor-002',
      timestamp: 1678886400000,
      source: 'Sensor-Hub',
      dataType: 'sensor_reading',
      payload: { temperature: 22.5, unit: 'C' },
    };
    const aligned = alignChronalEcho(echo) as AlignedData;
    expect(aligned.harmonizedPayload.temperature).toBe(22.5);
    expect(typeof aligned.harmonizedPayload.temperature).toBe('number');
  });
});

describe('mergeAlignedData', () => {
  // Mock rationale: All test data is in-memory JavaScript objects, ensuring deterministic and offline tests.

  const initialData: AlignedData[] = [
    {
      id: 'item-A',
      alignedTimestamp: new Date(1000),
      originalSource: 'Source-1',
      alignedType: 'type-1',
      harmonizedPayload: { value: 10 },
    },
    {
      id: 'item-B',
      alignedTimestamp: new Date(2000),
      originalSource: 'Source-2',
      alignedType: 'type-2',
      harmonizedPayload: { value: 20 },
    },
  ];

  it('should add a new unique AlignedData entry', () => {
    const newItem: AlignedData = {
      id: 'item-C',
      alignedTimestamp: new Date(3000),
      originalSource: 'Source-3',
      alignedType: 'type-3',
      harmonizedPayload: { value: 30 },
    };
    const merged = mergeAlignedData(initialData, newItem);
    expect(merged.length).toBe(3);
    expect(merged).toContainEqual(newItem);
  });

  it('should update an existing entry if the new data has a newer timestamp', () => {
    const updatedItem: AlignedData = {
      id: 'item-A',
      alignedTimestamp: new Date(1500), // Newer timestamp
      originalSource: 'Source-1-Updated',
      alignedType: 'type-1-updated',
      harmonizedPayload: { value: 15, newKey: 'newValue' },
    };
    const merged = mergeAlignedData(initialData, updatedItem);
    expect(merged.length).toBe(2);
    expect(merged).toContainEqual(updatedItem);
    expect(merged).not.toContainEqual(initialData[0]); // Original should be replaced
  });

  it('should not update an existing entry if the new data has an older timestamp', () => {
    const olderItem: AlignedData = {
      id: 'item-A',
      alignedTimestamp: new Date(500), // Older timestamp
      originalSource: 'Source-1-Old',
      alignedType: 'type-1-old',
      harmonizedPayload: { value: 5 },
    };
    const merged = mergeAlignedData(initialData, olderItem);
    expect(merged.length).toBe(2);
    expect(merged).toContainEqual(initialData[0]); // Original should remain
    expect(merged).not.toContainEqual(olderItem);
  });

  it('should not update an existing entry if the new data has the same timestamp', () => {
    const sameTimestampItem: AlignedData = {
      id: 'item-A',
      alignedTimestamp: new Date(1000), // Same timestamp
      originalSource: 'Source-1-Same',
      alignedType: 'type-1-same',
      harmonizedPayload: { value: 100 },
    };
    const merged = mergeAlignedData(initialData, sameTimestampItem);
    expect(merged.length).toBe(2);
    expect(merged).toContainEqual(initialData[0]); // Original should remain
    expect(merged).not.toContainEqual(sameTimestampItem);
  });

  it('should handle an empty initial dataset correctly', () => {
    const newItem: AlignedData = {
      id: 'item-D',
      alignedTimestamp: new Date(4000),
      originalSource: 'Source-4',
      alignedType: 'type-4',
      harmonizedPayload: { value: 40 },
    };
    const merged = mergeAlignedData([], newItem);
    expect(merged.length).toBe(1);
    expect(merged).toContainEqual(newItem);
  });
});
