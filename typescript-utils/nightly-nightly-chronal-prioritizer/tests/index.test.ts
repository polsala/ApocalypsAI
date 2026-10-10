import { prioritizeTasks, Task, PrioritizedTask } from '../src/index';

// Mock rationale: Math.random() is non-deterministic. To ensure tests are repeatable,
// we mock it to return a fixed value. This allows us to predict the 'temporal distortion'
// and thus the final priority scores.
const mockMathRandom = jest.spyOn(Math, 'random').mockReturnValue(0.5); // Always returns 0.5

describe('prioritizeTasks', () => {
  beforeEach(() => {
    // Reset the mock before each test to ensure isolation
    mockMathRandom.mockClear();
    mockMathRandom.mockReturnValue(0.5); // Default mock value
  });

  afterAll(() => {
    // Restore original Math.random after all tests
    mockMathRandom.mockRestore();
  });

  it('should prioritize tasks correctly based on urgency, importance, and whimsy', () => {
    const tasks: Task[] = [
      { name: 'High Urgency, High Importance', urgency: 5, importance: 5, whimsyFactor: 0.1 },
      { name: 'Medium Urgency, High Importance', urgency: 3, importance: 5, whimsyFactor: 0.8 },
      { name: 'Low Urgency, Low Importance', urgency: 1, importance: 1, whimsyFactor: 0.9 },
      { name: 'High Urgency, Low Importance', urgency: 5, importance: 1, whimsyFactor: 0.2 },
      { name: 'No Whimsy Factor', urgency: 3, importance: 3 }, // whimsyFactor defaults to 0.5
    ];

    // With Math.random() mocked to 0.5, temporalDistortion will be 0.5 * 0.5 + 0.75 = 0.25 + 0.75 = 1.0
    // Scores:
    // Task 1: (5*3) + (5*2) + (0.1*1*1.0) = 15 + 10 + 0.1 = 25.1
    // Task 2: (3*3) + (5*2) + (0.8*1*1.0) = 9 + 10 + 0.8 = 19.8
    // Task 3: (1*3) + (1*2) + (0.9*1*1.0) = 3 + 2 + 0.9 = 5.9
    // Task 4: (5*3) + (1*2) + (0.2*1*1.0) = 15 + 2 + 0.2 = 17.2
    // Task 5: (3*3) + (3*2) + (0.5*1*1.0) = 9 + 6 + 0.5 = 15.5

    const prioritized = prioritizeTasks(tasks);

    expect(prioritized.length).toBe(5);
    expect(prioritized[0].name).toBe('High Urgency, High Importance');
    expect(prioritized[0].priorityScore).toBeCloseTo(25.1);
    expect(prioritized[1].name).toBe('Medium Urgency, High Importance');
    expect(prioritized[1].priorityScore).toBeCloseTo(19.8);
    expect(prioritized[2].name).toBe('High Urgency, Low Importance');
    expect(prioritized[2].priorityScore).toBeCloseTo(17.2);
    expect(prioritized[3].name).toBe('No Whimsy Factor');
    expect(prioritized[3].priorityScore).toBeCloseTo(15.5);
    expect(prioritized[4].name).toBe('Low Urgency, Low Importance');
    expect(prioritized[4].priorityScore).toBeCloseTo(5.9);
  });

  it('should handle tasks with only urgency and importance (default whimsyFactor)', () => {
    const tasks: Task[] = [
      { name: 'Task A', urgency: 4, importance: 3 },
      { name: 'Task B', urgency: 2, importance: 5 },
    ];

    // With Math.random() mocked to 0.5, temporalDistortion will be 1.0
    // Task A: (4*3) + (3*2) + (0.5*1*1.0) = 12 + 6 + 0.5 = 18.5
    // Task B: (2*3) + (5*2) + (0.5*1*1.0) = 6 + 10 + 0.5 = 16.5

    const prioritized = prioritizeTasks(tasks);

    expect(prioritized.length).toBe(2);
    expect(prioritized[0].name).toBe('Task A');
    expect(prioritized[0].priorityScore).toBeCloseTo(18.5);
    expect(prioritized[1].name).toBe('Task B');
    expect(prioritized[1].priorityScore).toBeCloseTo(16.5);
  });

  it('should return an empty array if no tasks are provided', () => {
    const tasks: Task[] = [];
    const prioritized = prioritizeTasks(tasks);
    expect(prioritized).toEqual([]);
  });

  it('should sort tasks correctly when whimsyFactor is 0', () => {
    const tasks: Task[] = [
      { name: 'Task X', urgency: 5, importance: 5, whimsyFactor: 0 },
      { name: 'Task Y', urgency: 4, importance: 4, whimsyFactor: 0 },
    ];

    // With Math.random() mocked to 0.5, temporalDistortion will be 1.0
    // Task X: (5*3) + (5*2) + (0*1*1.0) = 15 + 10 + 0 = 25.0
    // Task Y: (4*3) + (4*2) + (0*1*1.0) = 12 + 8 + 0 = 20.0

    const prioritized = prioritizeTasks(tasks);

    expect(prioritized[0].name).toBe('Task X');
    expect(prioritized[0].priorityScore).toBeCloseTo(25.0);
    expect(prioritized[1].name).toBe('Task Y');
    expect(prioritized[1].priorityScore).toBeCloseTo(20.0);
  });

  it('should sort tasks correctly when whimsyFactor is 1', () => {
    const tasks: Task[] = [
      { name: 'Task P', urgency: 1, importance: 1, whimsyFactor: 1 },
      { name: 'Task Q', urgency: 1, importance: 1, whimsyFactor: 0.5 },
    ];

    // With Math.random() mocked to 0.5, temporalDistortion will be 1.0
    // Task P: (1*3) + (1*2) + (1*1*1.0) = 3 + 2 + 1 = 6.0
    // Task Q: (1*3) + (1*2) + (0.5*1*1.0) = 3 + 2 + 0.5 = 5.5

    const prioritized = prioritizeTasks(tasks);

    expect(prioritized[0].name).toBe('Task P');
    expect(prioritized[0].priorityScore).toBeCloseTo(6.0);
    expect(prioritized[1].name).toBe('Task Q');
    expect(prioritized[1].priorityScore).toBeCloseTo(5.5);
  });
});
