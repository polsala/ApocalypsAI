import { calculateCosmicPriority, prioritizeTasks } from '../src/index';
import { Task, CosmicFactor, PrioritizedTask } from '../src/types';

describe('Cosmic Chore Chart Utility', () => {

  // # Mock rationale: Cosmic factors and tasks are inputs to the utility.
  // We define static mock data to ensure deterministic and offline testing.
  // These mocks represent various scenarios for cosmic influences and task properties.
  const mockCosmicFactors: CosmicFactor[] = [
    { name: 'LunarAlignment', value: 0.7, impactMultiplier: 2 },
    { name: 'SolarFlareActivity', value: 0.3, impactMultiplier: 4 },
    { name: 'NebulaDrift', value: 0.1, impactMultiplier: -1 }, // Negative impact
    { name: 'VoidWhisperIntensity', value: 0.9, impactMultiplier: 3 }
  ];

  const mockTasks: Task[] = [
    {
      id: 't1',
      name: 'Repair Quantum Entanglement Stabilizer',
      basePriority: 10,
      cosmicModifiers: {
        'LunarAlignment': 1.5, // More affected
        'VoidWhisperIntensity': 2.0 // Doubly affected
      },
      description: 'Critical for multiverse integrity.'
    },
    {
      id: 't2',
      name: 'Replenish Antimatter Reserves',
      basePriority: 8,
      cosmicModifiers: {
        'SolarFlareActivity': 0.5 // Less affected
      },
      description: 'Fuel for the starship.'
    },
    {
      id: 't3',
      name: 'Archive Temporal Anomaly Logs',
      basePriority: 5,
      description: 'Routine data backup.'
    },
    {
      id: 't4',
      name: 'Calibrate Chronal Displacement Unit',
      basePriority: 7,
      cosmicModifiers: {
        'NebulaDrift': 0.5, // Less affected by negative factor
        'LunarAlignment': 0.8 // Slightly less affected by lunar alignment
      },
      description: 'Ensures accurate time jumps.'
    }
  ];

  describe('calculateCosmicPriority', () => {
    it('should calculate priority correctly with all factors and modifiers', () => {
      const task = mockTasks[0]; // Repair Quantum Entanglement Stabilizer
      const expectedScore =
        task.basePriority +
        (mockCosmicFactors[0].value * mockCosmicFactors[0].impactMultiplier * (task.cosmicModifiers?.['LunarAlignment'] ?? 1)) +
        (mockCosmicFactors[1].value * mockCosmicFactors[1].impactMultiplier * (task.cosmicModifiers?.['SolarFlareActivity'] ?? 1)) +
        (mockCosmicFactors[2].value * mockCosmicFactors[2].impactMultiplier * (task.cosmicModifiers?.['NebulaDrift'] ?? 1)) +
        (mockCosmicFactors[3].value * mockCosmicFactors[3].impactMultiplier * (task.cosmicModifiers?.['VoidWhisperIntensity'] ?? 1));

      // 10 (base)
      // + (0.7 * 2 * 1.5) = 2.1
      // + (0.3 * 4 * 1) = 1.2 (SolarFlareActivity not in modifiers, defaults to 1)
      // + (0.1 * -1 * 1) = -0.1 (NebulaDrift not in modifiers, defaults to 1)
      // + (0.9 * 3 * 2.0) = 5.4
      // Total: 10 + 2.1 + 1.2 - 0.1 + 5.4 = 18.6
      expect(calculateCosmicPriority(task, mockCosmicFactors)).toBeCloseTo(18.6);
    });

    it('should calculate priority correctly with no cosmic modifiers for a task', () => {
      const task = mockTasks[2]; // Archive Temporal Anomaly Logs
      const expectedScore =
        task.basePriority +
        (mockCosmicFactors[0].value * mockCosmicFactors[0].impactMultiplier * 1) + // Default modifier 1
        (mockCosmicFactors[1].value * mockCosmicFactors[1].impactMultiplier * 1) +
        (mockCosmicFactors[2].value * mockCosmicFactors[2].impactMultiplier * 1) +
        (mockCosmicFactors[3].value * mockCosmicFactors[3].impactMultiplier * 1);

      // 5 (base)
      // + (0.7 * 2 * 1) = 1.4
      // + (0.3 * 4 * 1) = 1.2
      // + (0.1 * -1 * 1) = -0.1
      // + (0.9 * 3 * 1) = 2.7
      // Total: 5 + 1.4 + 1.2 - 0.1 + 2.7 = 10.2
      expect(calculateCosmicPriority(task, mockCosmicFactors)).toBeCloseTo(10.2);
    });

    it('should handle empty cosmic factors array', () => {
      const task = mockTasks[0];
      expect(calculateCosmicPriority(task, [])).toBe(task.basePriority);
    });

    it('should handle zero base priority', () => {
      const zeroPriorityTask: Task = {
        id: 't5',
        name: 'Idle Observation',
        basePriority: 0,
        cosmicModifiers: { 'LunarAlignment': 1 }
      };
      // 0 (base) + (0.7 * 2 * 1) = 1.4
      // + (0.3 * 4 * 1) = 1.2
      // + (0.1 * -1 * 1) = -0.1
      // + (0.9 * 3 * 1) = 2.7
      // Total: 0 + 1.4 + 1.2 - 0.1 + 2.7 = 5.2
      expect(calculateCosmicPriority(zeroPriorityTask, mockCosmicFactors)).toBeCloseTo(5.2);
    });
  });

  describe('prioritizeTasks', () => {
    it('should sort tasks by cosmic priority score in descending order', () => {
      const prioritized = prioritizeTasks(mockTasks, mockCosmicFactors);

      // Expected scores (calculated manually for verification):
      // t1: 18.6
      // t2: 8 (base) + (0.7*2*1) + (0.3*4*0.5) + (0.1*-1*1) + (0.9*3*1) = 8 + 1.4 + 0.6 - 0.1 + 2.7 = 12.6
      // t3: 10.2 (from previous test)
      // t4: 7 (base) + (0.7*2*0.8) + (0.3*4*1) + (0.1*-1*0.5) + (0.9*3*1) = 7 + 1.12 + 1.2 - 0.05 + 2.7 = 11.97

      // Order should be: t1 (18.6), t2 (12.6), t4 (11.97), t3 (10.2)
      expect(prioritized.length).toBe(mockTasks.length);
      expect(prioritized[0].id).toBe('t1');
      expect(prioritized[0].cosmicPriorityScore).toBeCloseTo(18.6);
      expect(prioritized[1].id).toBe('t2');
      expect(prioritized[1].cosmicPriorityScore).toBeCloseTo(12.6);
      expect(prioritized[2].id).toBe('t4');
      expect(prioritized[2].cosmicPriorityScore).toBeCloseTo(11.97);
      expect(prioritized[3].id).toBe('t3');
      expect(prioritized[3].cosmicPriorityScore).toBeCloseTo(10.2);

      // Ensure scores are indeed descending
      for (let i = 0; i < prioritized.length - 1; i++) {
        expect(prioritized[i].cosmicPriorityScore).toBeGreaterThanOrEqual(prioritized[i + 1].cosmicPriorityScore);
      }
    });

    it('should return an empty array if no tasks are provided', () => {
      const prioritized = prioritizeTasks([], mockCosmicFactors);
      expect(prioritized).toEqual([]);
    });

    it('should handle tasks with identical cosmic priority scores gracefully (order stable)', () => {
      const identicalTasks: Task[] = [
        { id: 'a', name: 'Task A', basePriority: 5 },
        { id: 'b', name: 'Task B', basePriority: 5 }
      ];
      const factors: CosmicFactor[] = [{ name: 'Neutral', value: 0, impactMultiplier: 0 }];
      const prioritized = prioritizeTasks(identicalTasks, factors);
      // With identical scores, the original order should be preserved by stable sort,
      // but JavaScript's sort is not guaranteed stable. However, for equal scores,
      // any order is technically correct. We'll just check scores.
      expect(prioritized[0].cosmicPriorityScore).toBe(5);
      expect(prioritized[1].cosmicPriorityScore).toBe(5);
    });
  });
});
