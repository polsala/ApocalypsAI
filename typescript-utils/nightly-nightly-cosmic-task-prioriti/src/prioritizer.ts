export type Task = {
  id: string;
  description: string;
  tags?: string[];
};

export type CosmicUrgency = "Nebula Nudge" | "Stellar Sprint" | "Galactic Grind" | "Void Voyage";
export type FocusConstellation = "Orion's Hour" | "Pleiades' Pause" | "Andromeda's Apex" | "Cygnus' Cycle";

export type PrioritizedTask = {
  task: Task;
  urgency: CosmicUrgency;
  constellation: FocusConstellation;
  suggestedDurationMinutes: number;
};

const COSMIC_URGENCIES: CosmicUrgency[] = ["Nebula Nudge", "Stellar Sprint", "Galactic Grind", "Void Voyage"];
const FOCUS_CONSTELLATIONS: FocusConstellation[] = ["Orion's Hour", "Pleiades' Pause", "Andromeda's Apex", "Cygnus' Cycle"];
const BASE_DURATIONS_MINUTES: number[] = [15, 30, 60, 120]; // Corresponds to urgency levels

/**
 * A simple, deterministic hash function for strings.
 * @param s The string to hash.
 * @returns A numeric hash.
 */
function simpleHash(s: string): number {
  let hash = 0;
  for (let i = 0; i < s.length; i++) {
    const char = s.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0; // Convert to 32bit integer
  }
  return Math.abs(hash);
}

/**
 * Prioritizes a list of tasks with cosmic flair.
 * @param tasks An array of Task objects.
 * @returns An array of PrioritizedTask objects.
 */
export function prioritizeTasks(tasks: Task[]): PrioritizedTask[] {
  return tasks.map(task => {
    const taskHash = simpleHash(task.description + task.id + (task.tags ? task.tags.join(',') : ''));

    const urgencyIndex = taskHash % COSMIC_URGENCIES.length;
    const constellationIndex = (taskHash + 1) % FOCUS_CONSTELLATIONS.length; // Offset to get different index
    const durationIndex = (taskHash + 2) % BASE_DURATIONS_MINUTES.length; // Offset again

    const urgency = COSMIC_URGENCIES[urgencyIndex];
    const constellation = FOCUS_CONSTELLATIONS[constellationIndex];
    const suggestedDurationMinutes = BASE_DURATIONS_MINUTES[durationIndex];

    return {
      task,
      urgency,
      constellation,
      suggestedDurationMinutes,
    };
  });
}
