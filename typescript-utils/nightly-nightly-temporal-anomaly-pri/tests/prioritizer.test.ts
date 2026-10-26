import { prioritizeAnomalies } from '../src/prioritizer';
import { Anomaly, PrioritizationRule, PrioritizedAnomaly } from '../src/types';

describe('prioritizeAnomalies', () => {
    // Mock rationale: File system operations are external dependencies.
    // We mock the input data (anomalies and rules) directly in the test
    // to ensure determinism and avoid relying on actual file existence or content.

    const mockAnomalies: Anomaly[] = [
        {
            id: 'ANOMALY-001', timestamp: '2023-10-27T10:00:00Z', type: 'temporal-drift',
            severity: 'moderate', location: 'Sector 7G', description: 'Minor time dilation detected.',
            status: 'detected', detectedBy: 'Sentry-Alpha', dataPoints: 15
        },
        {
            id: 'ANOMALY-002', timestamp: '2023-10-27T10:05:00Z', type: 'rift-signature',
            severity: 'critical', location: 'Void Edge', description: 'Large rift opening detected.',
            status: 'detected', detectedBy: 'Watcher-Omega', dataPoints: 100
        },
        {
            id: 'ANOMALY-003', timestamp: '2023-10-27T10:10:00Z', type: 'echo-chamber',
            severity: 'minor', location: 'Old Library', description: 'Repeated historical echoes.',
            status: 'detected', detectedBy: 'Archivist-Beta', dataPoints: 5
        },
        {
            id: 'ANOMALY-004', timestamp: '2023-10-27T10:15:00Z', type: 'void-whisper',
            severity: 'severe', location: 'Deep Chasm', description: 'Unintelligible whispers from the void.',
            status: 'detected', detectedBy: 'Whisper-Listener', dataPoints: 30
        },
        {
            id: 'ANOMALY-005', timestamp: '2023-10-27T10:20:00Z', type: 'temporal-drift',
            severity: 'severe', location: 'Central Hub', description: 'Significant time distortion.',
            status: 'detected', detectedBy: 'Sentry-Gamma', dataPoints: 50
        },
        {
            id: 'ANOMALY-006', timestamp: '2023-10-27T10:25:00Z', type: 'unknown',
            severity: 'moderate', location: 'Outskirts', description: 'Unclassified anomaly.',
            status: 'detected', detectedBy: 'Scout-Delta', dataPoints: 10
        },
        {
            id: 'ANOMALY-007', timestamp: '2023-10-27T10:30:00Z', type: 'temporal-drift',
            severity: 'minor', location: 'Sector 7G', description: 'Resolved minor drift.',
            status: 'resolved', detectedBy: 'Sentry-Alpha', dataPoints: 12
        }
    ];

    const mockRules: PrioritizationRule[] = [
        {
            name: 'Critical Rift Alert',
            condition: { type: 'rift-signature', severity: 'critical' },
            action: 'critical',
            priorityBoost: 20
        },
        {
            name: 'Severe Temporal Drift in Hub',
            condition: { type: 'temporal-drift', severity: 'severe', locationContains: 'Central Hub' },
            action: 'high',
            priorityBoost: 10
        },
        {
            name: 'Void Whisper Protocol',
            condition: { type: 'void-whisper', minDataPoints: 25 },
            action: 'high',
            priorityBoost: 8
        },
        {
            name: 'Minor Echo Chamber Ignore',
            condition: { type: 'echo-chamber', severity: 'minor' },
            action: 'ignore'
        },
        {
            name: 'General Severe Anomaly',
            condition: { severity: 'severe' },
            action: 'medium',
            priorityBoost: 5
        }
    ];

    it('should prioritize anomalies correctly based on rules and severity', () => {
        const prioritized = prioritizeAnomalies(mockAnomalies, mockRules);

        // Expected order based on calculated scores:
        // ANOMALY-002 (Rift, Critical): Base 5 + Rule 'Critical Rift Alert' (action critical, boost 20) = 25. Final assigned 'critical' adds 10. Total = 35.
        // ANOMALY-004 (Void Whisper, Severe): Base 3 + Rule 'Void Whisper Protocol' (action high, boost 8) = 11. Also matches 'General Severe Anomaly' (action medium, boost 5) = 16. Highest action is 'high'. Final assigned 'high' adds 5. Total = 21.
        // ANOMALY-005 (Temporal Drift, Severe, Central Hub): Base 3 + Rule 'Severe Temporal Drift in Hub' (action high, boost 10) = 13. Highest action is 'high'. Final assigned 'high' adds 5. Total = 18.
        // ANOMALY-001 (Temporal Drift, Moderate): Base 2. No specific rules. Final assigned 'low' adds 1. Total = 3.
        // ANOMALY-006 (Unknown, Moderate): Base 2. No specific rules. Final assigned 'low' adds 1. Total = 3.
        // ANOMALY-007 (Temporal Drift, Minor, Resolved): Base 1. No specific rules. Final assigned 'low' adds 1. Total = 2. Suggested action should reflect 'resolved'.
        // ANOMALY-003 (Echo Chamber, Minor): Base 1 + Rule 'Minor Echo Chamber Ignore' (action ignore). Final assigned 'ignore' sets score to 0. Total = 0.

        expect(prioritized[0].id).toBe('ANOMALY-002'); // Score 35
        expect(prioritized[0].assignedPriority).toBe('critical');
        expect(prioritized[0].priorityScore).toBe(35);
        expect(prioritized[0].matchedRules).toContain('Critical Rift Alert');
        expect(prioritized[0].suggestedAction).toContain('CRITICAL');

        expect(prioritized[1].id).toBe('ANOMALY-004'); // Score 21
        expect(prioritized[1].assignedPriority).toBe('high');
        expect(prioritized[1].priorityScore).toBe(21);
        expect(prioritized[1].matchedRules).toEqual(expect.arrayContaining(['Void Whisper Protocol', 'General Severe Anomaly']));
        expect(prioritized[1].suggestedAction).toContain('Immediate investigation');

        expect(prioritized[2].id).toBe('ANOMALY-005'); // Score 18
        expect(prioritized[2].assignedPriority).toBe('high');
        expect(prioritized[2].priorityScore).toBe(18);
        expect(prioritized[2].matchedRules).toContain('Severe Temporal Drift in Hub');
        expect(prioritized[2].suggestedAction).toContain('Immediate investigation');

        // Anomalies with same score should maintain relative order or be stable (Jest doesn't guarantee this, but scores are distinct here)
        expect(prioritized[3].id).toBe('ANOMALY-001'); // Score 3
        expect(prioritized[3].assignedPriority).toBe('low');
        expect(prioritized[3].priorityScore).toBe(3);

        expect(prioritized[4].id).toBe('ANOMALY-006'); // Score 3
        expect(prioritized[4].assignedPriority).toBe('low');
        expect(prioritized[4].priorityScore).toBe(3);

        expect(prioritized[5].id).toBe('ANOMALY-007'); // Score 2
        expect(prioritized[5].assignedPriority).toBe('low');
        expect(prioritized[5].priorityScore).toBe(2);
        expect(prioritized[5].suggestedAction).toContain('already resolved');

        expect(prioritized[6].id).toBe('ANOMALY-003'); // Score 0
        expect(prioritized[6].assignedPriority).toBe('ignore');
        expect(prioritized[6].priorityScore).toBe(0);
        expect(prioritized[6].suggestedAction).toContain('no immediate action');

        // Ensure all anomalies are present in the output
        expect(prioritized.length).toBe(mockAnomalies.length);
    });

    it('should handle an empty anomalies list', () => {
        const prioritized = prioritizeAnomalies([], mockRules);
        expect(prioritized).toEqual([]);
    });

    it('should handle an empty rules list', () => {
        const prioritized = prioritizeAnomalies(mockAnomalies, []);
        // With no rules, only base severity scores and default 'low' priority apply
        expect(prioritized.length).toBe(mockAnomalies.length);

        // Check highest priority (ANOMALY-002: Critical, base 5 + low 1 = 6)
        expect(prioritized[0].id).toBe('ANOMALY-002');
        expect(prioritized[0].priorityScore).toBe(6);
        expect(prioritized[0].assignedPriority).toBe('low');
        expect(prioritized[0].matchedRules).toEqual([]);

        // Check lowest priority (ANOMALY-003: Minor, base 1 + low 1 = 2)
        expect(prioritized[6].id).toBe('ANOMALY-003');
        expect(prioritized[6].priorityScore).toBe(2);
        expect(prioritized[6].assignedPriority).toBe('low');
        expect(prioritized[6].matchedRules).toEqual([]);
    });

    it('should correctly apply "ignore" action and set score to 0', () => {
        const anomaliesToIgnore: Anomaly[] = [
            {
                id: 'IGNORE-ME', timestamp: '2023-10-27T11:00:00Z', type: 'echo-chamber',
                severity: 'minor', location: 'Quiet Corner', description: 'Faint echoes.',
                status: 'detected', detectedBy: 'Sentry-Epsilon', dataPoints: 2
            }
        ];
        const rulesToIgnore: PrioritizationRule[] = [
            {
                name: 'Ignore Faint Echoes',
                condition: { type: 'echo-chamber', severity: 'minor' },
                action: 'ignore'
            }
        ];
        const prioritized = prioritizeAnomalies(anomaliesToIgnore, rulesToIgnore);
        expect(prioritized[0].id).toBe('IGNORE-ME');
        expect(prioritized[0].assignedPriority).toBe('ignore');
        expect(prioritized[0].priorityScore).toBe(0);
        expect(prioritized[0].suggestedAction).toContain('no immediate action');
    });

    it('should ensure higher action overrides lower action for assignedPriority, while scores accumulate', () => {
        const anomaly: Anomaly = {
            id: 'OVERRIDE-TEST', timestamp: '2023-10-27T12:00:00Z', type: 'temporal-drift',
            severity: 'moderate', location: 'Test Zone', description: 'Test drift.',
            status: 'detected', detectedBy: 'Test-Agent', dataPoints: 10
        };
        const rules: PrioritizationRule[] = [
            { name: 'Low Priority Rule', condition: { type: 'temporal-drift' }, action: 'low', priorityBoost: 1 },
            { name: 'High Priority Rule', condition: { locationContains: 'Test Zone' }, action: 'high', priorityBoost: 5 }
        ];
        const prioritized = prioritizeAnomalies([anomaly], rules);
        expect(prioritized[0].assignedPriority).toBe('high');
        expect(prioritized[0].matchedRules).toEqual(expect.arrayContaining(['Low Priority Rule', 'High Priority Rule']));
        // Calculation: Base 2 (moderate) + Low Rule boost 1 + High Rule boost 5 = 8. Final assigned 'high' adds 5. Total = 13.
        expect(prioritized[0].priorityScore).toBe(13);
    });

    it('should correctly suggest action for resolved anomalies', () => {
        const resolvedAnomaly: Anomaly = {
            id: 'ANOMALY-RESOLVED', timestamp: '2023-10-27T10:30:00Z', type: 'temporal-drift',
            severity: 'minor', location: 'Sector 7G', description: 'Resolved minor drift.',
            status: 'resolved', detectedBy: 'Sentry-Alpha', dataPoints: 12
        };
        const prioritized = prioritizeAnomalies([resolvedAnomaly], []); // No rules, default low priority
        expect(prioritized[0].suggestedAction).toContain('Anomaly already resolved, verify stability');
        expect(prioritized[0].assignedPriority).toBe('low'); // Still assigned a priority, but action is specific
    });
});
