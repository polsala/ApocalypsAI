import { Anomaly, Rule, PrioritizedAnomaly, CategorizedAnomalies } from './types';

const DEFAULT_CATEGORY = "Unclassified Chronal Event";
const DEFAULT_PRIORITY = "Low Priority";

/**
 * Sorts and categorizes a list of anomalies based on a set of rules.
 * @param anomalies The list of anomalies to sort.
 * @param rules The list of rules to apply for categorization and prioritization.
 * @returns An object where keys are categories and values are arrays of prioritized anomalies.
 */
export function sortAnomalies(anomalies: Anomaly[], rules: Rule[]): CategorizedAnomalies {
  const categorized: CategorizedAnomalies = {};

  anomalies.forEach(anomaly => {
    let matchedRule: Rule | undefined;

    // Find the first matching rule
    for (const rule of rules) {
      const regex = new RegExp(rule.pattern, 'i'); // Case-insensitive match
      if (regex.test(anomaly.description)) {
        matchedRule = rule;
        break; // Use the first matching rule
      }
    }

    const priority = matchedRule ? matchedRule.priority : DEFAULT_PRIORITY;
    const category = matchedRule ? matchedRule.category : DEFAULT_CATEGORY;

    const prioritizedAnomaly: PrioritizedAnomaly = {
      ...anomaly,
      priority,
      category,
    };

    if (!categorized[category]) {
      categorized[category] = [];
    }
    categorized[category].push(prioritizedAnomaly);
  });

  return categorized;
}
