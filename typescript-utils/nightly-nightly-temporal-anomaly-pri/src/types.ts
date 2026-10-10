/**
 * Defines the possible severity levels for a temporal anomaly.
 */
export type AnomalySeverity = 'minor' | 'moderate' | 'severe' | 'critical';

/**
 * Defines the possible types of temporal anomalies.
 */
export type AnomalyType = 'temporal-drift' | 'echo-chamber' | 'rift-signature' | 'void-whisper' | 'unknown';

/**
 * Defines the current status of a detected anomaly.
 */
export type AnomalyStatus = 'detected' | 'investigating' | 'resolved';

/**
 * Represents a detected temporal anomaly.
 */
export interface Anomaly {
    id: string;
    timestamp: string; // ISO 8601 format
    type: AnomalyType;
    severity: AnomalySeverity;
    location: string;
    description: string;
    status: AnomalyStatus;
    detectedBy: string;
    dataPoints: number; // Quantitative measure of anomaly strength/frequency
}

/**
 * Defines the action to be taken or priority level assigned by a rule.
 */
export type RuleAction = 'ignore' | 'low' | 'medium' | 'high' | 'critical';

/**
 * Represents a rule for prioritizing anomalies.
 */
export interface PrioritizationRule {
    name: string;
    condition: {
        type?: AnomalyType; // Optional: match by anomaly type
        severity?: AnomalySeverity; // Optional: match by anomaly severity
        locationContains?: string; // Optional: match if location string contains this substring
        minDataPoints?: number; // Optional: match if dataPoints are at least this value
    };
    action: RuleAction; // The priority level or action to assign if rule matches
    priorityBoost?: number; // Optional: additional score points for matching this rule
}

/**
 * Represents an anomaly after it has been processed and prioritized.
 */
export interface PrioritizedAnomaly extends Anomaly {
    priorityScore: number; // A numerical score indicating overall priority
    assignedPriority: RuleAction; // The highest priority action assigned by any matching rule
    matchedRules: string[]; // Names of rules that matched this anomaly
    suggestedAction: string; // A human-readable suggested action based on assigned priority
}
