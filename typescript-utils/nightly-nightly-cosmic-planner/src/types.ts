export type RuleAction = 'ALLOW' | 'AVOID' | 'RECOMMEND';

export interface CosmicEvent {
  name: string;
  startDate: string; // YYYY-MM-DD
  endDate: string;   // YYYY-MM-DD
  impacts: string[]; // Keywords describing the event's influence
}

export interface AlignmentRule {
  description: string;
  condition: {
    eventImpacts?: string[]; // Event impacts that trigger this rule (OR logic)
    eventName?: string;      // Specific event name that triggers this rule (OR logic)
  };
  action: RuleAction;
  targetTasks: string[]; // Keywords in task descriptions that this rule applies to (OR logic)
}

export interface Task {
  description: string;
}

export interface TaskAlignmentResult {
  task: Task;
  status: RuleAction;
  reason?: string;
  activeRules?: AlignmentRule[];
}
