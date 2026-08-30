export interface Task {
  id: string;
  description: string;
  tags?: string[];
  dueDate?: string; // YYYY-MM-DD
}

export interface PrioritizedTask extends Task {
  cosmicScore: number;
  rationale: string;
}
