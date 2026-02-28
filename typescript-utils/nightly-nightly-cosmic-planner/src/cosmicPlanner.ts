import { CosmicEvent, AlignmentRule, Task, TaskAlignmentResult, RuleAction } from './types';

export class CosmicPlanner {
  private events: CosmicEvent[];
  private rules: AlignmentRule[];

  constructor(events: CosmicEvent[], rules: AlignmentRule[]) {
    this.events = events;
    this.rules = rules;
  }

  /**
   * Checks if a given date falls within the range of a cosmic event.
   * @param date The date to check (YYYY-MM-DD).
   * @param event The cosmic event.
   * @returns True if the date is within the event's range, false otherwise.
   */
  private isEventActive(date: string, event: CosmicEvent): boolean {
    const checkDate = new Date(date);
    const startDate = new Date(event.startDate);
    const endDate = new Date(event.endDate);
    // Normalize dates to start of day to avoid time zone issues
    checkDate.setUTCHours(0, 0, 0, 0);
    startDate.setUTCHours(0, 0, 0, 0);
    endDate.setUTCHours(0, 0, 0, 0);
    return checkDate >= startDate && checkDate <= endDate;
  }

  /**
   * Gets all active cosmic events for a given date.
   * @param date The date to check (YYYY-MM-DD).
   * @returns An array of active CosmicEvent objects.
   */
  public getActiveEvents(date: string): CosmicEvent[] {
    return this.events.filter(event => this.isEventActive(date, event));
  }

  /**
   * Checks a single task against all active rules for a given date.
   * @param date The date to check (YYYY-MM-DD).
   * @param task The task to evaluate.
   * @returns A TaskAlignmentResult indicating the task's status.
   */
  public checkTaskAlignment(date: string, task: Task): TaskAlignmentResult {
    const activeEvents = this.getActiveEvents(date);
    let finalStatus: RuleAction = 'ALLOW';
    const activeRulesForTask: AlignmentRule[] = [];

    for (const rule of this.rules) {
      // Check if the rule applies to the task based on targetTasks keywords
      const taskMatchesRule = rule.targetTasks.some(keyword =>
        task.description.toLowerCase().includes(keyword.toLowerCase())
      );

      if (!taskMatchesRule) {
        continue; // Rule does not apply to this task
      }

      // Check if the rule's condition is met by any active event
      const conditionMet = activeEvents.some(event => {
        const eventNameMatches = rule.condition.eventName && event.name === rule.condition.eventName;
        const eventImpactsMatch = rule.condition.eventImpacts && rule.condition.eventImpacts.some(impact =>
          event.impacts.includes(impact)
        );
        return eventNameMatches || eventImpactsMatch;
      });

      if (conditionMet) {
        activeRulesForTask.push(rule);
        // Prioritize AVOID > RECOMMEND > ALLOW
        if (rule.action === 'AVOID') {
          finalStatus = 'AVOID';
          break; // AVOID is the strongest, no need to check further for this task
        } else if (rule.action === 'RECOMMEND' && finalStatus === 'ALLOW') {
          finalStatus = 'RECOMMEND'; // Only upgrade from ALLOW to RECOMMEND
        }
      }
    }

    return {
      task,
      status: finalStatus,
      reason: activeRulesForTask.length > 0 ? activeRulesForTask[0].description : 'No conflicting rules',
      activeRules: activeRulesForTask.length > 0 ? activeRulesForTask : undefined,
    };
  }

  /**
   * Checks a list of tasks against all active rules for a given date.
   * @param date The date to check (YYYY-MM-DD).
   * @param tasks An array of tasks to evaluate.
   * @returns An array of TaskAlignmentResult objects.
   */
  public planTasks(date: string, tasks: Task[]): TaskAlignmentResult[] {
    return tasks.map(task => this.checkTaskAlignment(date, task));
  }
}
