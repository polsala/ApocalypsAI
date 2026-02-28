import { CosmicPlanner } from '../src/cosmicPlanner';
import { CosmicEvent, AlignmentRule, Task, TaskAlignmentResult } from '../src/types';

describe('CosmicPlanner', () => {
  // # Mock rationale: Using fixed, simple cosmic events and rules for deterministic testing.
  // This avoids reliance on external data sources or complex date calculations.
  const mockEvents: CosmicEvent[] = [
    {
      name: 'Mercury in Retrograde',
      startDate: '2024-04-01',
      endDate: '2024-04-30',
      impacts: ['Communication', 'Technology'],
    },
    {
      name: 'Full Moon in Pisces',
      startDate: '2024-09-17',
      endDate: '2024-09-18',
      impacts: ['Intuition', 'Dreams'],
    },
    {
      name: 'Mars Direct', // A positive event
      startDate: '2024-01-01',
      endDate: '2024-12-31',
      impacts: ['Action', 'Energy'],
    },
  ];

  const mockRules: AlignmentRule[] = [
    {
      description: 'Avoid tech deployments during Mercury Retrograde',
      condition: { eventImpacts: ['Technology'] },
      action: 'AVOID',
      targetTasks: ['Deploy', 'Release'],
    },
    {
      description: 'Communication tasks are tricky during Mercury Retrograde',
      condition: { eventImpacts: ['Communication'] },
      action: 'AVOID',
      targetTasks: ['Communicate', 'Present'],
    },
    {
      description: 'Intuitive tasks are recommended during Full Moon in Pisces',
      condition: { eventName: 'Full Moon in Pisces' },
      action: 'RECOMMEND',
      targetTasks: ['Meditate', 'Reflect'],
    },
    {
      description: 'High energy tasks are recommended when Mars is Direct',
      condition: { eventName: 'Mars Direct' },
      action: 'RECOMMEND',
      targetTasks: ['Execute', 'Launch'],
    },
  ];

  let planner: CosmicPlanner;

  beforeEach(() => {
    planner = new CosmicPlanner(mockEvents, mockRules);
  });

  describe('getActiveEvents', () => {
    test('should return active events for a date within an event range', () => {
      const activeEvents = planner.getActiveEvents('2024-04-15');
      expect(activeEvents).toHaveLength(2); // Mercury Retrograde and Mars Direct
      expect(activeEvents.some(e => e.name === 'Mercury in Retrograde')).toBe(true);
      expect(activeEvents.some(e => e.name === 'Mars Direct')).toBe(true);
    });

    test('should return no active events for a date outside all event ranges', () => {
      const activeEvents = planner.getActiveEvents('2024-05-01');
      expect(activeEvents).toHaveLength(1); // Only Mars Direct
      expect(activeEvents.some(e => e.name === 'Mars Direct')).toBe(true);
    });

    test('should return multiple active events if ranges overlap', () => {
      const activeEvents = planner.getActiveEvents('2024-09-17');
      expect(activeEvents).toHaveLength(2); // Full Moon in Pisces and Mars Direct
      expect(activeEvents.some(e => e.name === 'Full Moon in Pisces')).toBe(true);
      expect(activeEvents.some(e => e.name === 'Mars Direct')).toBe(true);
    });
  });

  describe('checkTaskAlignment', () => {
    const tasks: Task[] = [
      { description: 'Deploy new feature to production' }, // Matches 'Deploy' and 'Technology' impact
      { description: 'Communicate Q3 results' },          // Matches 'Communicate' and 'Communication' impact
      { description: 'Meditate on project goals' },       // Matches 'Meditate' and 'Full Moon in Pisces' event
      { description: 'Write documentation' },             // No matching rules
      { description: 'Launch new marketing campaign' },   // Matches 'Launch' and 'Mars Direct' event
    ];

    test('should correctly identify AVOID status for Mercury Retrograde and tech deployment', () => {
      const result = planner.checkTaskAlignment('2024-04-15', tasks[0]); // Mercury Retrograde active
      expect(result.status).toBe('AVOID');
      expect(result.reason).toContain('Avoid tech deployments during Mercury Retrograde');
      expect(result.activeRules).toHaveLength(1);
    });

    test('should correctly identify AVOID status for Mercury Retrograde and communication', () => {
      const result = planner.checkTaskAlignment('2024-04-15', tasks[1]); // Mercury Retrograde active
      expect(result.status).toBe('AVOID');
      expect(result.reason).toContain('Communication tasks are tricky during Mercury Retrograde');
      expect(result.activeRules).toHaveLength(1);
    });

    test('should correctly identify RECOMMEND status for Full Moon and intuitive task', () => {
      const result = planner.checkTaskAlignment('2024-09-17', tasks[2]); // Full Moon in Pisces active
      expect(result.status).toBe('RECOMMEND');
      expect(result.reason).toContain('Intuitive tasks are recommended during Full Moon in Pisces');
      expect(result.activeRules).toHaveLength(1);
    });

    test('should correctly identify ALLOW status when no rules apply', () => {
      const result = planner.checkTaskAlignment('2024-04-15', tasks[3]); // No rules for 'Write documentation'
      expect(result.status).toBe('ALLOW');
      expect(result.reason).toBe('No conflicting rules');
      expect(result.activeRules).toBeUndefined();
    });

    test('should correctly identify RECOMMEND status for Mars Direct and launch task', () => {
      const result = planner.checkTaskAlignment('2024-07-01', tasks[4]); // Mars Direct active
      expect(result.status).toBe('RECOMMEND');
      expect(result.reason).toContain('High energy tasks are recommended when Mars is Direct');
      expect(result.activeRules).toHaveLength(1);
    });

    test('should prioritize AVOID over RECOMMEND if both apply', () => {
      // Create a scenario where both AVOID and RECOMMEND rules could apply
      const conflictingRules: AlignmentRule[] = [
        {
          description: 'AVOID all tasks during critical period',
          condition: { eventName: 'Critical Period' },
          action: 'AVOID',
          targetTasks: ['Any Task'],
        },
        {
          description: 'RECOMMEND creative tasks during Critical Period',
          condition: { eventName: 'Critical Period' },
          action: 'RECOMMEND',
          targetTasks: ['Creative Task'],
        },
      ];
      const conflictingEvents: CosmicEvent[] = [
        {
          name: 'Critical Period',
          startDate: '2024-06-01',
          endDate: '2024-06-01',
          impacts: ['All'],
        },
      ];
      const conflictingPlanner = new CosmicPlanner(conflictingEvents, conflictingRules);
      const task: Task = { description: 'Creative Task: Any Task' }; // Matches both
      const result = conflictingPlanner.checkTaskAlignment('2024-06-01', task);
      expect(result.status).toBe('AVOID'); // AVOID should win
      expect(result.reason).toContain('AVOID all tasks during critical period');
      expect(result.activeRules).toHaveLength(2); // Both rules are active, but AVOID takes precedence
    });
  });

  describe('planTasks', () => {
    test('should process multiple tasks and return results', () => {
      const tasksToPlan: Task[] = [
        { description: 'Deploy hotfix' },
        { description: 'Meditate on next steps' },
        { description: 'Prepare presentation' },
      ];
      const date = '2024-04-15'; // Mercury Retrograde active

      const results = planner.planTasks(date, tasksToPlan);

      expect(results).toHaveLength(3);

      // Deploy hotfix -> AVOID (Technology impact)
      expect(results[0].task.description).toBe('Deploy hotfix');
      expect(results[0].status).toBe('AVOID');

      // Meditate on next steps -> ALLOW (no specific rule, Full Moon in Pisces not active)
      expect(results[1].task.description).toBe('Meditate on next steps');
      expect(results[1].status).toBe('ALLOW');

      // Prepare presentation -> AVOID (Communication impact)
      expect(results[2].task.description).toBe('Prepare presentation');
      expect(results[2].status).toBe('AVOID');
    });

    test('should handle a date with no active events gracefully', () => {
      const tasksToPlan: Task[] = [
        { description: 'General task 1' },
        { description: 'General task 2' },
      ];
      const date = '2025-01-01'; // No mock events active on this date except Mars Direct

      const results = planner.planTasks(date, tasksToPlan);

      expect(results).toHaveLength(2);
      expect(results[0].status).toBe('ALLOW');
      expect(results[1].status).toBe('ALLOW');
    });
  });
});
