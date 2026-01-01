export interface Task {
  id: string;
  name: string;
  startTime: Date;
  endTime: Date;
}

export enum ParadoxType {
  OVERLAP = "OVERLAP",
  NEGATIVE_DURATION = "NEGATIVE_DURATION",
  INVALID_TIME_ORDER = "INVALID_TIME_ORDER",
  CONTAINED_TASK = "CONTAINED_TASK",
}

export interface TemporalParadox {
  type: ParadoxType;
  taskA: Task;
  taskB?: Task; // Relevant for OVERLAP and CONTAINED_TASK
  message: string;
  suggestedFix?: string;
}
