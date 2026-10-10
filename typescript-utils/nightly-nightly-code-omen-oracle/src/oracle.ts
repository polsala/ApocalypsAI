import { LintResult, LintMessage, CodeOmen, OmenRule } from './types';
import { OMEN_RULES } from './rules';

export function interpretLintResults(results: LintResult[]): CodeOmen[] {
  const omens: CodeOmen[] = [];
  const ruleCounts: { [key: string]: { errors: number, warnings: number } } = {};

  for (const result of results) {
    for (const message of result.messages) {
      const ruleId = message.ruleId || 'unknown-rule';
      if (!ruleCounts[ruleId]) {
        ruleCounts[ruleId] = { errors: 0, warnings: 0 };
      }
      if (message.severity === 2) { // Error
        ruleCounts[ruleId].errors++;
      } else if (message.severity === 1) { // Warning
        ruleCounts[ruleId].warnings++;
      }
    }
  }

  for (const ruleId in ruleCounts) {
    const counts = ruleCounts[ruleId];
    let matchedRule: OmenRule | undefined;

    // Try to find a specific match first
    for (const omenRule of OMEN_RULES) {
      if (typeof omenRule.match === 'string' && omenRule.match === ruleId) {
        matchedRule = omenRule;
        break;
      }
      if (omenRule.match instanceof RegExp && omenRule.match.test(ruleId)) {
        matchedRule = omenRule;
        break;
      }
    }

    // If no specific match, use defaults
    if (!matchedRule) {
      if (counts.errors > 0) {
        matchedRule = OMEN_RULES.find(r => r.match === 'default-error');
      } else if (counts.warnings > 0) {
        matchedRule = OMEN_RULES.find(r => r.match === 'default-warning');
      }
    }

    if (matchedRule) {
      let severity: CodeOmen['severity'] = matchedRule.severity;
      if (counts.errors > 5 || (counts.errors > 0 && matchedRule.severity === 'severe')) {
        severity = 'severe';
      } else if (counts.errors > 0 || counts.warnings > 10) {
        severity = 'moderate';
      } else if (counts.warnings > 0) {
        severity = 'minor';
      }

      omens.push({
        title: matchedRule.omenTitle,
        description: `${matchedRule.omenDescription} (Detected ${counts.errors} errors, ${counts.warnings} warnings for rule: ${ruleId})`,
        advice: matchedRule.advice,
        severity: severity,
      });
    }
  }

  if (omens.length === 0) {
    omens.push({
      title: 'The Serene Silence',
      description: 'No disturbances found. The cosmic alignment is harmonious.',
      advice: 'Maintain vigilance, for even in tranquility, the seeds of chaos may lie dormant.',
      severity: 'prophecy',
    });
  }

  return omens;
}
