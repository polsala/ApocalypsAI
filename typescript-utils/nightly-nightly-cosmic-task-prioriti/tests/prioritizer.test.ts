import { prioritizeTasks, Task, CosmicUrgency, FocusConstellation, PrioritizedTask } from '../src/prioritizer';

describe('prioritizeTasks', () => {
  // Mock rationale: The prioritization logic is deterministic based on a simple hash.
  // No external dependencies or random numbers are used, so direct testing of the function
  // with predefined inputs is sufficient and ensures determinism.
  it('should prioritize a single task deterministically', () => {
    const tasks: Task[] = [
      { id: 'task-1', description: 'Write a cosmic haiku' },
    ];

    const prioritized = prioritizeTasks(tasks);

    expect(prioritized).toHaveLength(1);
    const pTask = prioritized[0];

    expect(pTask.task).toEqual(tasks[0]);
    expect(pTask.urgency).toBe("Void Voyage");
    expect(pTask.constellation).toBe("Orion's Hour");
    expect(pTask.suggestedDurationMinutes).toBe(30);
  });

  it('should prioritize multiple tasks deterministically', () => {
    const tasks: Task[] = [
      { id: 'task-a', description: 'Align the stellar compass' },
      { id: 'task-b', description: 'Calibrate the temporal flux capacitor', tags: ['urgent', 'tech'] },
      { id: 'task-c', description: 'Gather stardust for the weekly ritual' },
    ];

    const prioritized = prioritizeTasks(tasks);

    expect(prioritized).toHaveLength(3);

    // Check task-a
    expect(prioritized[0].task.id).toBe('task-a');
    expect(prioritized[0].urgency).toBe("Galactic Grind");
    expect(prioritized[0].constellation).toBe("Cygnus' Cycle");
    expect(prioritized[0].suggestedDurationMinutes).toBe(15);

    // Check task-b
    expect(prioritized[1].task.id).toBe('task-b');
    expect(prioritized[1].urgency).toBe("Stellar Sprint");
    expect(prioritized[1].constellation).toBe("Andromeda's Apex");
    expect(prioritized[1].suggestedDurationMinutes).toBe(120);

    // Check task-c
    expect(prioritized[2].task.id).toBe('task-c');
    expect(prioritized[2].urgency).toBe("Galactic Grind");
    expect(prioritized[2].constellation).toBe("Cygnus' Cycle");
    expect(prioritized[2].suggestedDurationMinutes).toBe(15);
  });

  it('should handle empty task list', () => {
    const tasks: Task[] = [];
    const prioritized = prioritizeTasks(tasks);
    expect(prioritized).toHaveLength(0);
  });

  it('should produce consistent output for identical inputs', () => {
    const tasks1: Task[] = [{ id: 'test-id', description: 'Test description' }];
    const tasks2: Task[] = [{ id: 'test-id', description: 'Test description' }];

    const prioritized1 = prioritizeTasks(tasks1);
    const prioritized2 = prioritizeTasks(tasks2);

    expect(prioritized1).toEqual(prioritized2);
  });

  it('should produce different output for different inputs', () => {
    const tasks1: Task[] = [{ id: 'test-id-1', description: 'Test description A' }];
    const tasks2: Task[] = [{ id: 'test-id-2', description: 'Test description B' }];

    const prioritized1 = prioritizeTasks(tasks1);
    const prioritized2 = prioritizeTasks(tasks2);

    expect(prioritized1).not.toEqual(prioritized2);
  });
});
