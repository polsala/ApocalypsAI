import { sortAnomalies } from '../src/sorter';
import { Anomaly, Rule, CategorizedAnomalies } from '../src/types';

describe('sortAnomalies', () => {
  const mockAnomalies: Anomaly[] = [
    {
      id: 'A001',
      description: 'My coffee brewed itself, but it was green.',
      timestamp: '2024-07-20T08:00:00Z',
      tags: ['domestic', 'beverage']
    },
    {
      id: 'A002',
      description: 'A dinosaur appeared in my backyard for 5 minutes.',
      timestamp: '2024-07-19T10:30:00Z',
      tags: ['wildlife', 'temporal-shift']
    },
    {
      id: 'A003',
      description: 'The sky turned plaid for an hour.',
      timestamp: '2024-07-18T15:00:00Z',
      tags: ['celestial', 'visual']
    },
    {
      id: 'A004',
      description: 'My cat started speaking fluent Latin.',
      timestamp: '2024-07-20T11:00:00Z',
      tags: ['domestic', 'sentient']
    },
    {
      id: 'A005',
      description: 'A mild temporal ripple caused my toast to be perpetually untoasted.',
      timestamp: '2024-07-21T07:00:00Z',
      tags: ['domestic', 'temporal']
    }
  ];

  const mockRules: Rule[] = [
    { pattern: 'coffee|tea', category: 'Domestic Beverage Blip', priority: 'Mild Concern' },
    { pattern: 'dinosaur', category: 'Prehistoric Ponderance', priority: 'Urgent Intervention' },
    { pattern: 'plaid', category: 'Visual Vortex', priority: 'Medium Priority' },
    { pattern: 'cat.*Latin', category: 'Sentient Pet Phenomenon', priority: 'High Priority' },
    { pattern: 'temporal ripple', category: 'Temporal Tangle', priority: 'High Priority' }
  ];

  it('should categorize anomalies based on matching rules', () => {
    const result = sortAnomalies(mockAnomalies, mockRules);

    expect(result['Domestic Beverage Blip']).toBeDefined();
    expect(result['Domestic Beverage Blip'].length).toBe(1);
    expect(result['Domestic Beverage Blip'][0].id).toBe('A001');
    expect(result['Domestic Beverage Blip'][0].priority).toBe('Mild Concern');

    expect(result['Prehistoric Ponderance']).toBeDefined();
    expect(result['Prehistoric Ponderance'].length).toBe(1);
    expect(result['Prehistoric Ponderance'][0].id).toBe('A002');
    expect(result['Prehistoric Ponderance'][0].priority).toBe('Urgent Intervention');

    expect(result['Visual Vortex']).toBeDefined();
    expect(result['Visual Vortex'].length).toBe(1);
    expect(result['Visual Vortex'][0].id).toBe('A003');
    expect(result['Visual Vortex'][0].priority).toBe('Medium Priority');

    expect(result['Sentient Pet Phenomenon']).toBeDefined();
    expect(result['Sentient Pet Phenomenon'].length).toBe(1);
    expect(result['Sentient Pet Phenomenon'][0].id).toBe('A004');
    expect(result['Sentient Pet Phenomenon'][0].priority).toBe('High Priority');

    expect(result['Temporal Tangle']).toBeDefined();
    expect(result['Temporal Tangle'].length).toBe(1);
    expect(result['Temporal Tangle'][0].id).toBe('A005');
    expect(result['Temporal Tangle'][0].priority).toBe('High Priority');
  });

  it('should assign default category and priority if no rule matches', () => {
    const anomaliesWithNoMatch: Anomaly[] = [
      {
        id: 'A006',
        description: 'A strange hum emanated from my toaster.',
        timestamp: '2024-07-22T09:00:00Z',
        tags: ['domestic', 'auditory']
      }
    ];
    const result = sortAnomalies(anomaliesWithNoMatch, mockRules);

    expect(result['Unclassified Chronal Event']).toBeDefined();
    expect(result['Unclassified Chronal Event'].length).toBe(1);
    expect(result['Unclassified Chronal Event'][0].id).toBe('A006');
    expect(result['Unclassified Chronal Event'][0].priority).toBe('Low Priority');
  });

  it('should handle an empty list of anomalies', () => {
    const result = sortAnomalies([], mockRules);
    expect(Object.keys(result).length).toBe(0);
  });

  it('should handle an empty list of rules, assigning defaults to all', () => {
    const result = sortAnomalies(mockAnomalies, []);
    expect(Object.keys(result).length).toBe(1); // All should be in default category
    expect(result['Unclassified Chronal Event']).toBeDefined();
    expect(result['Unclassified Chronal Event'].length).toBe(mockAnomalies.length);
    result['Unclassified Chronal Event'].forEach(anomaly => {
      expect(anomaly.priority).toBe('Low Priority');
      expect(anomaly.category).toBe('Unclassified Chronal Event');
    });
  });

  it('should use the first matching rule if multiple rules could apply', () => {
    const specificRules: Rule[] = [
      { pattern: 'coffee', category: 'Coffee Anomaly', priority: 'High Priority' },
      { pattern: 'beverage', category: 'General Beverage Issue', priority: 'Low Priority' }
    ];
    const anomaly: Anomaly = {
      id: 'A007',
      description: 'My coffee tasted like existential dread.',
      timestamp: '2024-07-23T06:00:00Z',
      tags: ['domestic', 'beverage', 'coffee']
    };
    const result = sortAnomalies([anomaly], specificRules);
    expect(result['Coffee Anomaly']).toBeDefined();
    expect(result['Coffee Anomaly'][0].priority).toBe('High Priority');
    expect(result['General Beverage Issue']).toBeUndefined(); // Only the first rule should apply
  });

  it('should be case-insensitive for rule patterns', () => {
    const caseInsensitiveRules: Rule[] = [
      { pattern: 'DINOSAUR', category: 'Roaring Reptile', priority: 'Critical' }
    ];
    const anomaly: Anomaly = {
      id: 'A008',
      description: 'A small dinosaur was in my fridge.',
      timestamp: '2024-07-24T12:00:00Z',
      tags: ['domestic']
    };
    const result = sortAnomalies([anomaly], caseInsensitiveRules);
    expect(result['Roaring Reptile']).toBeDefined();
    expect(result['Roaring Reptile'][0].priority).toBe('Critical');
  });
});
