export interface TimeInput {
  actualTime: string; // ISO 8601 string
  perceivedTime: string; // ISO 8601 string
}

export interface DriftResult {
  driftMs: number;
  mantra: string;
}
