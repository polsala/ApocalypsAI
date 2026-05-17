export interface Task {
  name: string;
  urgency: number; // 1-5
  importance: number; // 1-5
  whimsyFactor?: number; // 0-1, optional
}

export interface PrioritizedTask extends Task {
  priorityScore: number;
}
