import { calculatePriority } from '../src/main';

// Mock rationale: Using hardcoded test data ensures deterministic results
// without external dependencies

describe('Task Prioritization', () => {
  test('Prioritizes tasks with available resources', () => {
    const task = {
      name: 'Test Task',
      urgency: 7,
      resources_needed: ['tool']
    };

    const resources = { tool: 1 };
    const result = calculatePriority(task, resources);

    expect(result.feasible).toBe(true);
    expect(result.priorityScore).toBe(7);
  });

  test('Penalizes missing resources', () => {
    const task = {
      name: 'Test Task',
      urgency: 5,
      resources_needed: ['tool', 'material']
    };

    const resources = { tool: 1 };
    const result = calculatePriority(task, resources);

    expect(result.feasible).toBe(false);
    expect(result.priorityScore).toBe(3); // 5 urgency - 2 missing resources
  });
});
