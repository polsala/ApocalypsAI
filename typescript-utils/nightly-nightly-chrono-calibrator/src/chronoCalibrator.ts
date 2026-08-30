import { TemporalChunk, TemporalChunkType } from './types';

/**
 * Calibrates a task by breaking it down into a series of whimsical temporal chunks.
 * Uses a modified Pomodoro-like technique with cosmic flair.
 *
 * @param taskName The name of the task to calibrate.
 * @param totalMinutes The total estimated duration of the task in minutes.
 * @returns An array of TemporalChunk objects representing the calibrated plan.
 */
export function calibrateTask(taskName: string, totalMinutes: number): TemporalChunk[] {
  const chunks: TemporalChunk[] = [];
  let remainingMinutes = totalMinutes;

  const WORK_CHUNK_DURATION = 25; // minutes
  const SHORT_BREAK_DURATION = 5; // minutes
  const LONG_BREAK_DURATION = 15; // minutes (after 4 work chunks)

  let workChunkCount = 0;

  while (remainingMinutes > 0) {
    // Add a work chunk
    const workDuration = Math.min(remainingMinutes, WORK_CHUNK_DURATION);
    if (workDuration > 0) {
      chunks.push({
        name: 'Stardust Sprint',
        durationMinutes: workDuration,
        type: 'work',
        description: `Focused work on '${taskName}'`,
      });
      remainingMinutes -= workDuration;
      workChunkCount++;
    }

    // Add a break if there's still time and a work chunk was just completed
    if (remainingMinutes > 0) {
      if (workChunkCount % 4 === 0 && workChunkCount > 0) {
        // Long break after every 4 work chunks
        const longBreakDuration = Math.min(remainingMinutes, LONG_BREAK_DURATION);
        if (longBreakDuration > 0) {
          chunks.push({
            name: 'Cosmic Contemplation',
            durationMinutes: longBreakDuration,
            type: 'long-break',
            description: 'Review, plan next steps, or a longer recharge',
          });
          remainingMinutes -= longBreakDuration;
        }
      } else {
        // Short break
        const shortBreakDuration = Math.min(remainingMinutes, SHORT_BREAK_DURATION);
        if (shortBreakDuration > 0) {
          chunks.push({
            name: 'Nebula Nudge',
            durationMinutes: shortBreakDuration,
            type: 'short-break',
            description: 'Quick break, refocus',
          });
          remainingMinutes -= shortBreakDuration;
        }
      }
    }
  }

  return chunks;
}
