import { UrgencyCategory, Task, CategorizationRule } from './types';

const CATEGORIZATION_RULES: CategorizationRule[] = [
  {
    category: UrgencyCategory.IMMEDIATE_IMPLOSION,
    keywords: ["urgent", "now", "critical", "collapse", "fire", "emergency", "immediate", "danger"]
  },
  {
    category: UrgencyCategory.NEAR_TERM_NUISANCE,
    keywords: ["soon", "next", "important", "alert", "warning", "repair", "fix", "prepare"]
  },
  {
    category: UrgencyCategory.FUTURE_FOLLY,
    keywords: ["later", "eventually", "plan", "dream", "idea", "research", "develop", "consider"]
  },
  {
    category: UrgencyCategory.COSMIC_CONTEMPLATION,
    keywords: ["someday", "never", "ponder", "meditate", "void", "existential", "philosophize", "wonder"]
  }
];

export function categorizeTask(taskDescription: string): Task {
  const lowerCaseDescription = taskDescription.toLowerCase();
  let assignedCategory: UrgencyCategory = UrgencyCategory.COSMIC_CONTEMPLATION; // Default to least urgent

  // Iterate through rules from most urgent to least urgent.
  // The first rule whose keywords match will determine the category.
  for (const rule of CATEGORIZATION_RULES) {
    if (rule.keywords.some(keyword => lowerCaseDescription.includes(keyword))) {
      assignedCategory = rule.category;
      break; // Found the highest priority match, so stop checking
    }
  }

  return { description: taskDescription, category: assignedCategory };
}

export function sortTasks(tasks: Task[]): Task[] {
  const categoryOrder: Record<UrgencyCategory, number> = {
    [UrgencyCategory.IMMEDIATE_IMPLOSION]: 0,
    [UrgencyCategory.NEAR_TERM_NUISANCE]: 1,
    [UrgencyCategory.FUTURE_FOLLY]: 2,
    [UrgencyCategory.COSMIC_CONTEMPLATION]: 3
  };

  return [...tasks].sort((a, b) => {
    return categoryOrder[a.category] - categoryOrder[b.category];
  });
}

export function processTasks(taskDescriptions: string[]): Task[] {
  const categorized = taskDescriptions.map(categorizeTask);
  return sortTasks(categorized);
}
