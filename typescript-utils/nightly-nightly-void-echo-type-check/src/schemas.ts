import { VoidEchoTypeChecker } from './index';

/**
 * Registers a set of default schemas with the provided VoidEchoTypeChecker instance.
 * @param checker The VoidEchoTypeChecker instance to register schemas with.
 */
export function registerDefaultSchemas(checker: VoidEchoTypeChecker) {
  checker.registerSchema('simple-status', {
    type: 'string',
    pattern: '^VOID ECHO: (INFO|WARNING|ERROR): .+$'
  });

  checker.registerSchema('structured-log', {
    type: 'json',
    properties: {
      timestamp: { type: 'number', required: true },
      level: { type: 'string', required: true, enum: ['INFO', 'WARN', 'ERROR'] },
      message: { type: 'string', required: true },
      source: { type: 'string', required: false }
    }
  });

  checker.registerSchema('anomaly-report', {
    type: 'json',
    properties: {
      anomalyId: { type: 'string', required: true },
      severity: { type: 'number', required: true, enum: [1, 2, 3, 4, 5] },
      description: { type: 'string', required: true },
      detectedAt: { type: 'string', required: true }, // ISO string format expected
      resolutionSteps: { type: 'array', required: false } // Simplified: just checks if it's an array
    }
  });
}
