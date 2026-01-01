import { detectTemporalParadoxes } from '../src/index';
import { Task, ParadoxType } from '../src/types';

describe('detectTemporalParadoxes', () => {
  // Mock rationale: Date objects are mutable and depend on system time.
  // Using fixed Date objects ensures deterministic tests regardless of when they run.

  it('should detect no paradoxes for a clear, sequential schedule', () => {
    const schedule: Task[] = [
      { id: "1", name: "Task Alpha", startTime: new Date("2024-01-01T09:00:00Z"), endTime: new Date("2024-01-01T10:00:00Z") },
      { id: "2", name: "Task Beta", startTime: new Date("2024-01-01T10:00:00Z"), endTime: new Date("2024-01-01T11:00:00Z") },
      { id: "3", name: "Task Gamma", startTime: new Date("2024-01-01T11:00:00Z"), endTime: new Date("2024-01-01T12:00:00Z") },
    ];
    const paradoxes = detectTemporalParadoxes(schedule);
    expect(paradoxes).toHaveLength(0);
  });

  it('should detect an overlap paradox', () => {
    const schedule: Task[] = [
      { id: "1", name: "Task A", startTime: new Date("2024-01-01T09:00:00Z"), endTime: new Date("2024-01-01T10:30:00Z") },
      { id: "2", name: "Task B", startTime: new Date("2024-01-01T10:00:00Z"), endTime: new Date("2024-01-01T11:00:00Z") },
    ];
    const paradoxes = detectTemporalParadoxes(schedule);
    expect(paradoxes).toHaveLength(1);
    expect(paradoxes[0].type).toBe(ParadoxType.OVERLAP);
    expect(paradoxes[0].taskA.id).toBe("1");
    expect(paradoxes[0].taskB?.id).toBe("2");
  });

  it('should detect an invalid time order paradox (end before start)', () => {
    const schedule: Task[] = [
      { id: "1", name: "Task C", startTime: new Date("2024-01-01T11:00:00Z"), endTime: new Date("2024-01-01T10:00:00Z") },
    ];
    const paradoxes = detectTemporalParadoxes(schedule);
    expect(paradoxes).toHaveLength(1);
    expect(paradoxes[0].type).toBe(ParadoxType.INVALID_TIME_ORDER);
    expect(paradoxes[0].taskA.id).toBe("1");
  });

  it('should detect a negative duration paradox (start equals end)', () => {
    const schedule: Task[] = [
      { id: "1", name: "Task D", startTime: new Date("2024-01-01T12:00:00Z"), endTime: new Date("2024-01-01T12:00:00Z") },
    ];
    const paradoxes = detectTemporalParadoxes(schedule);
    expect(paradoxes).toHaveLength(1);
    expect(paradoxes[0].type).toBe(ParadoxType.NEGATIVE_DURATION);
    expect(paradoxes[0].taskA.id).toBe("1");
  });

  it('should detect a contained task paradox', () => {
    const schedule: Task[] = [
      { id: "1", name: "Parent Task", startTime: new Date("2024-01-01T09:00:00Z"), endTime: new Date("2024-01-01T12:00:00Z") },
      { id: "2", name: "Child Task", startTime: new Date("2024-01-01T09:30:00Z"), endTime: new Date("2024-01-01T10:30:00Z") },
    ];
    const paradoxes = detectTemporalParadoxes(schedule);
    expect(paradoxes).toHaveLength(1);
    expect(paradoxes[0].type).toBe(ParadoxType.CONTAINED_TASK);
    expect(paradoxes[0].taskA.id).toBe("1");
    expect(paradoxes[0].taskB?.id).toBe("2");
  });

  it('should detect multiple paradoxes in a complex schedule', () => {
    const schedule: Task[] = [
      { id: "1", name: "Task X", startTime: new Date("2024-01-01T08:00:00Z"), endTime: new Date("2024-01-01T12:00:00Z") }, // Parent
      { id: "2", name: "Task Y", startTime: new Date("2024-01-01T09:00:00Z"), endTime: new Date("2024-01-01T10:00:00Z") }, // Contained in X
      { id: "3", name: "Task Z", startTime: new Date("2024-01-01T11:00:00Z"), endTime: new Date("2024-01-01T13:00:00Z") }, // Overlaps X
      { id: "4", name: "Task W", startTime: new Date("2024-01-01T14:00:00Z"), endTime: new Date("2024-01-01T13:00:00Z") }, // Invalid time order
    ];
    const paradoxes = detectTemporalParadoxes(schedule);
    expect(paradoxes).toHaveLength(3); // One CONTAINED_TASK, one OVERLAP, one INVALID_TIME_ORDER

    const types = paradoxes.map(p => p.type).sort();
    expect(types).toEqual([ParadoxType.CONTAINED_TASK, ParadoxType.INVALID_TIME_ORDER, ParadoxType.OVERLAP]);
  });

  it('should handle tasks with identical start/end times but different IDs (not contained)', () => {
    const schedule: Task[] = [
      { id: "1", name: "Task E", startTime: new Date("2024-01-01T10:00:00Z"), endTime: new Date("2024-01-01T11:00:00Z") },
      { id: "2", name: "Task F", startTime: new Date("2024-01-01T10:00:00Z"), endTime: new Date("2024-01-01T11:00:00Z") },
    ];
    const paradoxes = detectTemporalParadoxes(schedule);
    expect(paradoxes).toHaveLength(1); // Should detect an overlap
    expect(paradoxes[0].type).toBe(ParadoxType.OVERLAP);
  });

  it('should handle an empty schedule', () => {
    const schedule: Task[] = [];
    const paradoxes = detectTemporalParadoxes(schedule);
    expect(paradoxes).toHaveLength(0);
  });

  it('should handle a schedule with a single valid task', () => {
    const schedule: Task[] = [
      { id: "1", name: "Solo Mission", startTime: new Date("2024-01-01T08:00:00Z"), endTime: new Date("2024-01-01T09:00:00Z") },
    ];
    const paradoxes = detectTemporalParadoxes(schedule);
    expect(paradoxes).toHaveLength(0);
  });
});
