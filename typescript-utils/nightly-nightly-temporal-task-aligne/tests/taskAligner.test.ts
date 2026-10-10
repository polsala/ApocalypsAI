import { alignTasks, calculateTemporalAlignment } from '../src/taskAligner';
import { Task } from '../src/types';

describe('calculateTemporalAlignment', () => {
  it('should calculate alignment based on urgency, energy cost, and random factor', () => {
    const task: Task = { id: 't1', name: 'Test Task', urgency: 3, energyCost: 2 };
    const randomFactor = 5; // Mock rationale: Providing a fixed random factor for deterministic testing.

    // Expected: (3 * 3) + ((6 - 2) * 2) + (5 * 1) = 9 + (4 * 2) + 5 = 9 + 8 + 5 = 22
    expect(calculateTemporalAlignment(task, randomFactor)).toBe(22);
  });

  it('should prioritize higher urgency', () => {
    const taskHighUrgency: Task = { id: 't1', name: 'High Urgency', urgency: 5, energyCost: 3 };
    const taskLowUrgency: Task = { id: 't2', name: 'Low Urgency', urgency: 1, energyCost: 3 };
    const randomFactor = 0; // Mock rationale: Neutralizing random factor to test other weights.

    const scoreHigh = calculateTemporalAlignment(taskHighUrgency, randomFactor);
    const scoreLow = calculateTemporalAlignment(taskLowUrgency, randomFactor);

    expect(scoreHigh).toBeGreaterThan(scoreLow);
  });

  it('should prioritize lower energy cost', () => {
    const taskLowEnergy: Task = { id: 't1', name: 'Low Energy', urgency: 3, energyCost: 1 };
    const taskHighEnergy: Task = { id: 't2', name: 'High Energy', urgency: 3, energyCost: 5 };
    const randomFactor = 0; // Mock rationale: Neutralizing random factor to test other weights.

    const scoreLowEnergy = calculateTemporalAlignment(taskLowEnergy, randomFactor);
    const scoreHighEnergy = calculateTemporalAlignment(taskHighEnergy, randomFactor);

    expect(scoreLowEnergy).toBeGreaterThan(scoreHighEnergy);
  });
});

describe('alignTasks', () => {
  const mockTasks: Task[] = [
    { id: 't1', name: 'Task Alpha', urgency: 3, energyCost: 3 },
    { id: 't2', name: 'Task Beta', urgency: 5, energyCost: 1 },
    { id: 't3', name: 'Task Gamma', urgency: 1, energyCost: 5 }
  ];

  it('should return an empty array if no tasks are provided', () => {
    expect(alignTasks([])).toEqual([]);
    expect(alignTasks(null as any)).toEqual([]); // Mock rationale: Testing null input for robustness.
  });

  it('should sort tasks by temporal alignment in descending order', () => {
    // Mock rationale: Providing a fixed sequence of random numbers for deterministic testing.
    // This mock ensures that `Math.random()` always returns the same values in order.
    const mockRandomGenerator = jest.fn()
      .mockReturnValueOnce(0.1) // For Task Alpha
      .mockReturnValueOnce(0.9) // For Task Beta
      .mockReturnValueOnce(0.5); // For Task Gamma

    const aligned = alignTasks(mockTasks, mockRandomGenerator);

    // Calculate expected scores manually with mock random factors (scaled by 10):
    // Task Alpha: urgency=3, energyCost=3, randomFactor=0.1*10=1
    //   Score: (3*3) + ((6-3)*2) + (1*1) = 9 + (3*2) + 1 = 9 + 6 + 1 = 16
    // Task Beta: urgency=5, energyCost=1, randomFactor=0.9*10=9
    //   Score: (5*3) + ((6-1)*2) + (9*1) = 15 + (5*2) + 9 = 15 + 10 + 9 = 34
    // Task Gamma: urgency=1, energyCost=5, randomFactor=0.5*10=5
    //   Score: (1*3) + ((6-5)*2) + (5*1) = 3 + (1*2) + 5 = 3 + 2 + 5 = 10

    expect(aligned.length).toBe(3);
    expect(aligned[0].name).toBe('Task Beta'); // Score 34
    expect(aligned[1].name).toBe('Task Alpha'); // Score 16
    expect(aligned[2].name).toBe('Task Gamma'); // Score 10

    expect(aligned[0].temporalAlignment).toBeCloseTo(34);
    expect(aligned[1].temporalAlignment).toBeCloseTo(16);
    expect(aligned[2].temporalAlignment).toBeCloseTo(10);
  });

  it('should handle tasks with identical scores consistently (order might vary based on JS sort stability)', () => {
    const identicalTasks: Task[] = [
      { id: 't1', name: 'Task A', urgency: 3, energyCost: 3 },
      { id: 't2', name: 'Task B', urgency: 3, energyCost: 3 }
    ];
    // Mock rationale: Providing a fixed random factor for deterministic testing.
    const mockRandomGenerator = jest.fn(() => 0.5); // Both get same random factor (5)

    const aligned = alignTasks(identicalTasks, mockRandomGenerator);

    // Both tasks will have score: (3*3) + ((6-3)*2) + (5*1) = 9 + 6 + 5 = 20
    expect(aligned.length).toBe(2);
    expect(aligned[0].temporalAlignment).toBeCloseTo(20);
    expect(aligned[1].temporalAlignment).toBeCloseTo(20);
    // The order between A and B might not be guaranteed by sort() if scores are identical,
    // but for deterministic tests, we can expect the original order to be preserved if sort is stable.
    expect(aligned[0].name).toBe('Task A');
    expect(aligned[1].name).toBe('Task B');
  });
});
