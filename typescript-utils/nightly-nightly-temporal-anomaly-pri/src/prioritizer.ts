import { Anomaly, PrioritizationRule, PrioritizedAnomaly, RuleAction, AnomalySeverity } from './types';

/**
 * Maps AnomalySeverity to a base numerical score.
 */
const SEVERITY_SCORES: Record<AnomalySeverity, number> = {
    'minor': 1,
    'moderate': 2,
    'severe': 3,
    'critical': 5
};

/**
 * Maps RuleAction to an additional score boost for the final priorityScore.
 */
const ACTION_SCORE_BOOST: Record<RuleAction, number> = {
    'ignore': 0,
    'low': 1,
    'medium': 3,
    'high': 5,
    'critical': 10
};

/**
 * Prioritizes a list of temporal anomalies based on a set of predefined rules.
 *
 * @param anomalies An array of Anomaly objects to be prioritized.
 * @param rules An array of PrioritizationRule objects to apply.
 * @returns An array of PrioritizedAnomaly objects, sorted by priorityScore in descending order.
 */
export function prioritizeAnomalies(anomalies: Anomaly[], rules: PrioritizationRule[]): PrioritizedAnomaly[] {
    return anomalies.map(anomaly => {
        let priorityScore = SEVERITY_SCORES[anomaly.severity] || 0;
        let assignedPriority: RuleAction = 'low'; // Default priority
        const matchedRules: string[] = [];

        // Apply rules to the anomaly
        for (const rule of rules) {
            let ruleMatches = true;

            // Check all conditions for the rule
            if (rule.condition.type && anomaly.type !== rule.condition.type) {
                ruleMatches = false;
            }
            if (rule.condition.severity && anomaly.severity !== rule.condition.severity) {
                ruleMatches = false;
            }
            if (rule.condition.locationContains && !anomaly.location.includes(rule.condition.locationContains)) {
                ruleMatches = false;
            }
            if (rule.condition.minDataPoints !== undefined && anomaly.dataPoints < rule.condition.minDataPoints) {
                ruleMatches = false;
            }

            if (ruleMatches) {
                matchedRules.push(rule.name);
                priorityScore += rule.priorityBoost || 0;

                // Update assignedPriority if the current rule's action is higher
                assignedPriority = getHigherPriorityAction(assignedPriority, rule.action);
            }
        }

        // If assignedPriority is 'ignore', override score to 0
        if (assignedPriority === 'ignore') {
            priorityScore = 0;
        } else {
            // Add a final boost based on the highest assigned priority
            priorityScore += ACTION_SCORE_BOOST[assignedPriority];
        }

        const suggestedAction = getSuggestedAction(assignedPriority, anomaly);

        return {
            ...anomaly,
            priorityScore,
            assignedPriority,
            matchedRules,
            suggestedAction
        };
    }).sort((a, b) => b.priorityScore - a.priorityScore); // Sort by highest priority first
}

/**
 * Determines the higher priority between two RuleAction values.
 * @param current The current assigned priority.
 * @param newAction The new action from a matching rule.
 * @returns The higher priority action.
 */
function getHigherPriorityAction(current: RuleAction, newAction: RuleAction): RuleAction {
    const priorityOrder: RuleAction[] = ['ignore', 'low', 'medium', 'high', 'critical'];
    const currentIndex = priorityOrder.indexOf(current);
    const newIndex = priorityOrder.indexOf(newAction);
    return newIndex > currentIndex ? newAction : current;
}

/**
 * Generates a human-readable suggested action based on the assigned priority and anomaly details.
 * @param priority The assigned priority level.
 * @param anomaly The original anomaly object.
 * @returns A string describing the suggested action.
 */
function getSuggestedAction(priority: RuleAction, anomaly: Anomaly): string {
    if (anomaly.status === 'resolved') {
        return `Anomaly already resolved, verify stability of ${anomaly.type} at ${anomaly.location}.`;
    }

    switch (priority) {
        case 'ignore':
            return 'Monitor passively, no immediate action required.';
        case 'low':
            return `Log and monitor ${anomaly.type} at ${anomaly.location}.`;
        case 'medium':
            return `Investigate ${anomaly.type} at ${anomaly.location}, prepare for minor intervention.`;
        case 'high':
            return `Immediate investigation required for ${anomaly.type} at ${anomaly.location}. Prepare for significant intervention.`;
        case 'critical':
            return `CRITICAL: Full team deployment to ${anomaly.location} for ${anomaly.type}. Containment protocols initiated.`;
        default:
            return 'No specific action suggested, review manually.';
    }
}
