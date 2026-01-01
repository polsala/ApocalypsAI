import { Task, TemporalParadox, ParadoxType } from './types';

/**
 * Detects temporal paradoxes within a given schedule of tasks.
 * @param schedule An array of tasks, each with an ID, name, start time, and end time.
 * @returns An array of detected TemporalParadoxes.
 */
export function detectTemporalParadoxes(schedule: Task[]): TemporalParadox[] {
  const paradoxes: TemporalParadox[] = [];

  // Sort tasks by start time to simplify overlap detection
  const sortedSchedule = [...schedule].sort((a, b) => a.startTime.getTime() - b.startTime.getTime());

  for (let i = 0; i < sortedSchedule.length; i++) {
    const taskA = sortedSchedule[i];

    // 1. Check for negative duration or invalid time order
    if (taskA.startTime.getTime() > taskA.endTime.getTime()) {
      paradoxes.push({
        type: ParadoxType.INVALID_TIME_ORDER,
        taskA,
        message: `Task '${taskA.name}' (ID: ${taskA.id}) defies causality: its end precedes its beginning!`,
        suggestedFix: `Adjust '${taskA.name}' to ensure startTime is before endTime. Perhaps a temporal realignment is in order?`,
      });
    } else if (taskA.startTime.getTime() === taskA.endTime.getTime()) {
      paradoxes.push({
        type: ParadoxType.NEGATIVE_DURATION, // Using this for zero duration too, as it's often an error
        taskA,
        message: `Task '${taskA.name}' (ID: ${taskA.id}) exists in a single, fleeting moment. Is it truly a task, or a temporal echo?`,
        suggestedFix: `Extend the duration of '${taskA.name}' or confirm it's an instantaneous event.`,
      });
    }

    // 2. Check for overlaps and contained tasks with subsequent tasks
    for (let j = i + 1; j < sortedSchedule.length; j++) {
      const taskB = sortedSchedule[j];

      // Check for overlap
      if (taskA.endTime.getTime() > taskB.startTime.getTime() && taskA.startTime.getTime() < taskB.endTime.getTime()) {
        paradoxes.push({
          type: ParadoxType.OVERLAP,
          taskA,
          taskB,
          message: `Temporal collision detected! Task '${taskA.name}' (ID: ${taskA.id}) and '${taskB.name}' (ID: ${taskB.id}) occupy the same spacetime.`,
          suggestedFix: `Reschedule one of the tasks, '${taskA.name}' or '${taskB.name}', to avoid temporal overlap. Perhaps a quantum shift in priorities?`,
        });
      }

      // Check if taskB is completely contained within taskA
      if (taskA.startTime.getTime() <= taskB.startTime.getTime() && taskA.endTime.getTime() >= taskB.endTime.getTime() && taskA.id !== taskB.id) {
        paradoxes.push({
          type: ParadoxType.CONTAINED_TASK,
          taskA,
          taskB,
          message: `Task '${taskB.name}' (ID: ${taskB.id}) is entirely engulfed by '${taskA.name}' (ID: ${taskA.id}). A temporal black hole?`,
          suggestedFix: `Consider if '${taskB.name}' is a sub-task of '${taskA.name}' or if its timing needs to be adjusted to exist independently.`,
        });
      }
    }
  }

  return paradoxes;
}

// CLI entry point (optional, but good for a standalone utility)
if (require.main === module) {
  // This block would typically read from stdin or a file, parse JSON, and then call detectTemporalParadoxes.
  // For simplicity in this example, we'll just show a basic usage.
  console.log("Nightly Temporal Schedule Fixer - CLI Mode");
  console.log("Provide a JSON array of tasks to stdin, or implement file parsing.");

  // Example usage:
  const exampleSchedule: Task[] = [
    { id: "1", name: "Gather Scraps", startTime: new Date("2024-04-20T10:00:00Z"), endTime: new Date("2024-04-20T11:00:00Z") },
    { id: "2", name: "Repair Drone", startTime: new Date("2024-04-20T10:30:00Z"), endTime: new Date("2024-04-20T12:00:00Z") }, // Overlap with 1
    { id: "3", name: "Scout Sector 7", startTime: new Date("2024-04-20T13:00:00Z"), endTime: new Date("2024-04-20T12:00:00Z") }, // Invalid time order
    { id: "4", name: "Meditate on Void", startTime: new Date("2024-04-20T14:00:00Z"), endTime: new Date("2024-04-20T14:00:00Z") }, // Zero duration
    { id: "5", name: "Prepare for Anomaly", startTime: new Date("2024-04-20T15:00:00Z"), endTime: new Date("2024-04-20T17:00:00Z") },
    { id: "6", name: "Check Anomaly Readings", startTime: new Date("2024-04-20T15:30:00Z"), endTime: new Date("2024-04-20T16:00:00Z") }, // Contained in 5
  ];

  const detectedParadoxes = detectTemporalParadoxes(exampleSchedule);

  if (detectedParadoxes.length > 0) {
    console.log("\n--- Detected Temporal Paradoxes ---");
    detectedParadoxes.forEach((p, index) => {
      console.log(`\nParadox ${index + 1}:`);
      console.log(`  Type: ${p.type}`);
      console.log(`  Message: ${p.message}`);
      if (p.suggestedFix) {
        console.log(`  Suggested Fix: ${p.suggestedFix}`);
      }
      console.log(`  Involving Task A: '${p.taskA.name}' (ID: ${p.taskA.id}) from ${p.taskA.startTime.toISOString()} to ${p.taskA.endTime.toISOString()}`);
      if (p.taskB) {
        console.log(`  Involving Task B: '${p.taskB.name}' (ID: ${p.taskB.id}) from ${p.taskB.startTime.toISOString()} to ${p.taskB.endTime.toISOString()}`);
      }
    });
  } else {
    console.log("\nNo temporal paradoxes detected. Your schedule is causally sound!");
  }
}
