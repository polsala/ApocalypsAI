import { alignTasks, calculateTaskScore } from '../src/index';
import { Task, ALIGNMENT_PRESETS, AlignmentType } from '../src/types';

// Mock rationale: These tests are unit tests for the core logic.
// They do not interact with external systems or file I/O.
// The `uuid` generation is not mocked as it's only used in the CLI part,
// and the `alignTasks` function directly takes Task objects.
// The CLI parsing itself is not directly tested here, but the underlying
// functions it calls are.

describe('calculateTaskScore', () => {
  const task: Task = { id: '1', name: 'Test Task', urgency: 3, effort: 2, reward: 4 };

  it('should calculate score correctly for Aggressive alignment', () => {
    const weights = ALIGNMENT_PRESETS.Aggressive;
    // (3 * 3) + (4 * 2) - (2 * 1) = 9 + 8 - 2 = 15
    expect(calculateTaskScore(task, weights)).toBe(15);
  });

  it('should calculate score correctly for Balanced alignment', () => {
    const weights = ALIGNMENT_PRESETS.Balanced;
    // (3 * 2) + (4 * 2) - (2 * 2) = 6 + 8 - 4 = 10
    expect(calculateTaskScore(task, weights)).toBe(10);
  });

  it('should calculate score correctly for Relaxed alignment', () => {
    const weights = ALIGNMENT_PRESETS.Relaxed;
    // (3 * 1) + (4 * 3) - (2 * 3) = 3 + 12 - 6 = 9
    expect(calculateTaskScore(task, weights)).toBe(9);
  });

  it('should calculate score correctly for Strategic alignment', () => {
    const weights = ALIGNMENT_PRESETS.Strategic;
    // (3 * 2) + (4 * 3) - (2 * 1) = 6 + 12 - 2 = 16
    expect(calculateTaskScore(task, weights)).toBe(16);
  });
});

describe('alignTasks', () => {
  const tasks: Task[] = [
    { id: 't1', name: 'Scavenge for water', urgency: 5, effort: 3, reward: 4, cosmicInfluence: 'Moon' },
    { id: 't2', name: 'Repair solar panel', urgency: 4, effort: 5, reward: 5, cosmicInfluence: 'Sun' },
    { id: 't3', name: 'Barter with nomads', urgency: 3, effort: 2, reward: 3, cosmicInfluence: 'Jupiter' },
    { id: 't4', name: 'Organize supplies', urgency: 2, effort: 1, reward: 2, cosmicInfluence: 'Venus' },
  ];

  it('should prioritize tasks correctly with Aggressive alignment', () => {
    // Aggressive: urgencyWeight: 3, effortWeight: 1, rewardWeight: 2
    // t1: (5*3) + (4*2) - (3*1) = 15 + 8 - 3 = 20
    // t2: (4*3) + (5*2) - (5*1) = 12 + 10 - 5 = 17
    // t3: (3*3) + (3*2) - (2*1) = 9 + 6 - 2 = 13
    // t4: (2*3) + (2*2) - (1*1) = 6 + 4 - 1 = 9
    const aligned = alignTasks(tasks, 'Aggressive');
    expect(aligned.map(t => t.name)).toEqual([
      'Scavenge for water',
      'Repair solar panel',
      'Barter with nomads',
      'Organize supplies'
    ]);
  });

  it('should prioritize tasks correctly with Balanced alignment', () => {
    // Balanced: urgencyWeight: 2, effortWeight: 2, rewardWeight: 2
    // t1: (5*2) + (4*2) - (3*2) = 10 + 8 - 6 = 12
    // t2: (4*2) + (5*2) - (5*2) = 8 + 10 - 10 = 8
    // t3: (3*2) + (3*2) - (2*2) = 6 + 6 - 4 = 8
    // t4: (2*2) + (2*2) - (1*2) = 4 + 4 - 2 = 6
    const aligned = alignTasks(tasks, 'Balanced');
    expect(aligned.map(t => t.name)).toEqual([
      'Scavenge for water',
      'Repair solar panel', // Scores are equal, original order maintained by stable sort
      'Barter with nomads',
      'Organize supplies'
    ]);
  });

  it('should prioritize tasks correctly with Relaxed alignment', () => {
    // Relaxed: urgencyWeight: 1, effortWeight: 3, rewardWeight: 3
    // t1: (5*1) + (4*3) - (3*3) = 5 + 12 - 9 = 8
    // t2: (4*1) + (5*3) - (5*3) = 4 + 15 - 15 = 4
    // t3: (3*1) + (3*3) - (2*3) = 3 + 9 - 6 = 6
    // t4: (2*1) + (2*3) - (1*3) = 2 + 6 - 3 = 5
    const aligned = alignTasks(tasks, 'Relaxed');
    expect(aligned.map(t => t.name)).toEqual([
      'Scavenge for water',
      'Barter with nomads',
      'Organize supplies',
      'Repair solar panel'
    ]);
  });

  it('should prioritize tasks correctly with Strategic alignment', () => {
    // Strategic: urgencyWeight: 2, effortWeight: 1, rewardWeight: 3
    // t1: (5*2) + (4*3) - (3*1) = 10 + 12 - 3 = 19
    // t2: (4*2) + (5*3) - (5*1) = 8 + 15 - 5 = 18
    // t3: (3*2) + (3*3) - (2*1) = 6 + 9 - 2 = 13
    // t4: (2*2) + (2*3) - (1*1) = 4 + 6 - 1 = 9
    const aligned = alignTasks(tasks, 'Strategic');
    expect(aligned.map(t => t.name)).toEqual([
      'Scavenge for water',
      'Repair solar panel',
      'Barter with nomads',
      'Organize supplies'
    ]);
  });

  it('should handle empty task list', () => {
    expect(alignTasks([], 'Balanced')).toEqual([]);
  });

  it('should throw error for unknown alignment type', () => {
    expect(() => alignTasks(tasks, 'Unknown' as AlignmentType)).toThrow('Unknown alignment type: Unknown');
  });
});
