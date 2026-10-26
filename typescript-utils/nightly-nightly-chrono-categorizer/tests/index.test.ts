import { categorizeTask, sortTasks, processTasks } from '../src/index';
import { UrgencyCategory, Task } from '../src/types';

describe('categorizeTask', () => {
  it('should categorize "urgent" tasks as IMMEDIATE_IMPLOSION', () => {
    const task = "Fix the reactor core - urgent!";
    const result = categorizeTask(task);
    expect(result.description).toBe(task);
    expect(result.category).toBe(UrgencyCategory.IMMEDIATE_IMPLOSION);
  });

  it('should categorize "critical" tasks as IMMEDIATE_IMPLOSION', () => {
    const task = "Critical system failure detected.";
    const result = categorizeTask(task);
    expect(result.category).toBe(UrgencyCategory.IMMEDIATE_IMPLOSION);
  });

  it('should categorize "soon" tasks as NEAR_TERM_NUISANCE', () => {
    const task = "Scavenge for supplies soon.";
    const result = categorizeTask(task);
    expect(result.category).toBe(UrgencyCategory.NEAR_TERM_NUISANCE);
  });

  it('should categorize "repair" tasks as NEAR_TERM_NUISANCE', () => {
    const task = "Repair the shelter's ventilation.";
    const result = categorizeTask(task);
    expect(result.category).toBe(UrgencyCategory.NEAR_TERM_NUISANCE);
  });

  it('should categorize "plan" tasks as FUTURE_FOLLY', () => {
    const task = "Plan for the next solar flare.";
    const result = categorizeTask(task);
    expect(result.category).toBe(UrgencyCategory.FUTURE_FOLLY);
  });

  it('should categorize "dream" tasks as FUTURE_FOLLY', () => {
    const task = "Dream about a world without mutants.";
    const result = categorizeTask(task);
    expect(result.category).toBe(UrgencyCategory.FUTURE_FOLLY);
  });

  it('should categorize "ponder" tasks as COSMIC_CONTEMPLATION', () => {
    const task = "Ponder the vastness of the void.";
    const result = categorizeTask(task);
    expect(result.category).toBe(UrgencyCategory.COSMIC_CONTEMPLATION);
  });

  it('should categorize tasks without specific keywords as COSMIC_CONTEMPLATION', () => {
    const task = "Just exist for a bit.";
    const result = categorizeTask(task);
    expect(result.category).toBe(UrgencyCategory.COSMIC_CONTEMPLATION);
  });

  it('should prioritize IMMEDIATE_IMPLOSION over other categories if multiple keywords exist', () => {
    const task = "Urgent: plan for immediate collapse!";
    const result = categorizeTask(task);
    expect(result.category).toBe(UrgencyCategory.IMMEDIATE_IMPLOSION);
  });

  it('should prioritize NEAR_TERM_NUISANCE over FUTURE_FOLLY', () => {
    const task = "Soon, we will plan for the future.";
    const result = categorizeTask(task);
    expect(result.category).toBe(UrgencyCategory.NEAR_TERM_NUISANCE);
  });
});

describe('sortTasks', () => {
  const tasks: Task[] = [
    { description: "Task C", category: UrgencyCategory.FUTURE_FOLLY },
    { description: "Task A", category: UrgencyCategory.IMMEDIATE_IMPLOSION },
    { description: "Task D", category: UrgencyCategory.COSMIC_CONTEMPLATION },
    { description: "Task B", category: UrgencyCategory.NEAR_TERM_NUISANCE }
  ];

  it('should sort tasks by urgency category', () => {
    const sorted = sortTasks(tasks);
    expect(sorted[0].category).toBe(UrgencyCategory.IMMEDIATE_IMPLOSION);
    expect(sorted[1].category).toBe(UrgencyCategory.NEAR_TERM_NUISANCE);
    expect(sorted[2].category).toBe(UrgencyCategory.FUTURE_FOLLY);
    expect(sorted[3].category).toBe(UrgencyCategory.COSMIC_CONTEMPLATION);
  });

  it('should maintain relative order for tasks within the same category', () => {
    const tasksWithSameCategory: Task[] = [
      { description: "Task X", category: UrgencyCategory.NEAR_TERM_NUISANCE },
      { description: "Task Y", category: UrgencyCategory.IMMEDIATE_IMPLOSION },
      { description: "Task Z", category: UrgencyCategory.NEAR_TERM_NUISANCE }
    ];
    const sorted = sortTasks(tasksWithSameCategory);
    expect(sorted[0].description).toBe("Task Y");
    expect(sorted[1].description).toBe("Task X"); // X comes before Z in original, should remain
    expect(sorted[2].description).toBe("Task Z");
  });
});

describe('processTasks', () => {
  it('should categorize and sort a list of task descriptions', () => {
    const taskDescriptions = [
      "Ponder the meaning of the void",
      "Fix the temporal rift - urgent!",
      "Scavenge for more sprockets (soon)",
      "Repair the shelter's roof",
      "Plan for next week's scavenging run"
    ];

    const processed = processTasks(taskDescriptions);

    expect(processed.length).toBe(5);
    expect(processed[0].description).toBe("Fix the temporal rift - urgent!");
    expect(processed[0].category).toBe(UrgencyCategory.IMMEDIATE_IMPLOSION);
    expect(processed[1].description).toBe("Scavenge for more sprockets (soon)");
    expect(processed[1].category).toBe(UrgencyCategory.NEAR_TERM_NUISANCE);
    expect(processed[2].description).toBe("Repair the shelter's roof");
    expect(processed[2].category).toBe(UrgencyCategory.NEAR_TERM_NUISANCE);
    expect(processed[3].description).toBe("Plan for next week's scavenging run");
    expect(processed[3].category).toBe(UrgencyCategory.FUTURE_FOLLY);
    expect(processed[4].description).toBe("Ponder the meaning of the void");
    expect(processed[4].category).toBe(UrgencyCategory.COSMIC_CONTEMPLATION);
  });
});
