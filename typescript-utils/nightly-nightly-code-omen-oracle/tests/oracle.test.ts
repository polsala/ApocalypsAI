import { interpretLintResults } from '../src/oracle';
import { LintResult, CodeOmen } from '../src/types';

describe('interpretLintResults', () => {
  // Mock rationale: We are testing the logic of interpreting lint results, not actual linting.
  // Providing mock LintResult objects allows us to simulate various scenarios deterministically
  // without needing to run an actual linter or access the filesystem.

  it('should return a "Serene Silence" omen if no lint results are provided', () => {
    const results: LintResult[] = [];
    const omens = interpretLintResults(results);
    expect(omens).toHaveLength(1);
    expect(omens[0].title).toBe('The Serene Silence');
    expect(omens[0].severity).toBe('prophecy');
  });

  it('should return a "Serene Silence" omen if lint results contain no messages', () => {
    const results: LintResult[] = [
      {
        filePath: 'src/file1.ts',
        messages: [],
        errorCount: 0,
        warningCount: 0,
        fixableErrorCount: 0,
        fixableWarningCount: 0,
        usedDeprecatedRules: [],
      },
    ];
    const omens = interpretLintResults(results);
    expect(omens).toHaveLength(1);
    expect(omens[0].title).toBe('The Serene Silence');
    expect(omens[0].severity).toBe('prophecy');
  });

  it('should correctly interpret a single "no-unused-vars" warning', () => {
    const results: LintResult[] = [
      {
        filePath: 'src/file1.ts',
        messages: [
          {
            ruleId: 'no-unused-vars',
            severity: 1, // Warning
            message: "'myVar' is defined but never used.",
            line: 1,
            column: 1,
            nodeType: 'Identifier',
          },
        ],
        errorCount: 0,
        warningCount: 1,
        fixableErrorCount: 0,
        fixableWarningCount: 0,
        usedDeprecatedRules: [],
      },
    ];
    const omens = interpretLintResults(results);
    expect(omens).toHaveLength(1);
    expect(omens[0].title).toBe('The Whispering Ghost of Unused Variables');
    expect(omens[0].severity).toBe('minor');
    expect(omens[0].description).toContain('Detected 0 errors, 1 warnings for rule: no-unused-vars');
  });

  it('should correctly interpret multiple "indent" errors', () => {
    const results: LintResult[] = [
      {
        filePath: 'src/file2.ts',
        messages: [
          { ruleId: 'indent', severity: 2, message: 'Expected 2 spaces, got 4.', line: 1, column: 1, nodeType: 'Program' },
          { ruleId: 'indent', severity: 2, message: 'Expected 2 spaces, got 0.', line: 2, column: 1, nodeType: 'Program' },
          { ruleId: 'indent', severity: 2, message: 'Expected 2 spaces, got 8.', line: 3, column: 1, nodeType: 'Program' },
        ],
        errorCount: 3,
        warningCount: 0,
        fixableErrorCount: 0,
        fixableWarningCount: 0,
        usedDeprecatedRules: [],
      },
    ];
    const omens = interpretLintResults(results);
    expect(omens).toHaveLength(1);
    expect(omens[0].title).toBe('The Shifting Sands of Indentation');
    expect(omens[0].severity).toBe('moderate'); // 3 errors, default is moderate
    expect(omens[0].description).toContain('Detected 3 errors, 0 warnings for rule: indent');
  });

  it('should correctly interpret a "no-explicit-any" error as severe', () => {
    const results: LintResult[] = [
      {
        filePath: 'src/file3.ts',
        messages: [
          { ruleId: 'no-explicit-any', severity: 2, message: 'Unexpected any. Specify a different type.', line: 5, column: 10, nodeType: 'TSTypeReference' },
        ],
        errorCount: 1,
        warningCount: 0,
        fixableErrorCount: 0,
        fixableWarningCount: 0,
        usedDeprecatedRules: [],
      },
    ];
    const omens = interpretLintResults(results);
    expect(omens).toHaveLength(1);
    expect(omens[0].title).toBe('The Veil of Any');
    expect(omens[0].severity).toBe('severe'); // Matched rule has severe
    expect(omens[0].description).toContain('Detected 1 errors, 0 warnings for rule: no-explicit-any');
  });

  it('should aggregate omens for different rules', () => {
    const results: LintResult[] = [
      {
        filePath: 'src/file4.ts',
        messages: [
          { ruleId: 'no-unused-vars', severity: 1, message: 'unused', line: 1, column: 1, nodeType: 'Identifier' },
          { ruleId: 'semi', severity: 2, message: 'Missing semicolon', line: 2, column: 5, nodeType: 'ExpressionStatement' },
        ],
        errorCount: 1,
        warningCount: 1,
        fixableErrorCount: 0,
        fixableWarningCount: 0,
        usedDeprecatedRules: [],
      },
    ];
    const omens = interpretLintResults(results);
    expect(omens).toHaveLength(2);
    expect(omens.some(o => o.title === 'The Whispering Ghost of Unused Variables')).toBe(true);
    expect(omens.some(o => o.title === 'The Forgotten Semicolon')).toBe(true);
  });

  it('should use default error omen for unmatched error rule', () => {
    const results: LintResult[] = [
      {
        filePath: 'src/file5.ts',
        messages: [
          { ruleId: 'unknown-error-rule', severity: 2, message: 'Something went wrong.', line: 1, column: 1, nodeType: 'Program' },
        ],
        errorCount: 1,
        warningCount: 0,
        fixableErrorCount: 0,
        fixableWarningCount: 0,
        usedDeprecatedRules: [],
      },
    ];
    const omens = interpretLintResults(results);
    expect(omens).toHaveLength(1);
    expect(omens[0].title).toBe('The Unseen Rift');
    expect(omens[0].severity).toBe('severe');
    expect(omens[0].description).toContain('Detected 1 errors, 0 warnings for rule: unknown-error-rule');
  });

  it('should use default warning omen for unmatched warning rule', () => {
    const results: LintResult[] = [
      {
        filePath: 'src/file6.ts',
        messages: [
          { ruleId: 'unknown-warning-rule', severity: 1, message: 'Consider this.', line: 1, column: 1, nodeType: 'Program' },
        ],
        errorCount: 0,
        warningCount: 1,
        fixableErrorCount: 0,
        fixableWarningCount: 0,
        usedDeprecatedRules: [],
      },
    ];
    const omens = interpretLintResults(results);
    expect(omens).toHaveLength(1);
    expect(omens[0].title).toBe('The Faint Echo');
    expect(omens[0].severity).toBe('moderate');
    expect(omens[0].description).toContain('Detected 0 errors, 1 warnings for rule: unknown-warning-rule');
  });

  it('should handle regex matching for rules', () => {
    const results: LintResult[] = [
      {
        filePath: 'src/file7.ts',
        messages: [
          { ruleId: 'no-unsafe-member-access', severity: 2, message: 'Unsafe access.', line: 1, column: 1, nodeType: 'MemberExpression' },
        ],
        errorCount: 1,
        warningCount: 0,
        fixableErrorCount: 0,
        fixableWarningCount: 0,
        usedDeprecatedRules: [],
      },
    ];
    const omens = interpretLintResults(results);
    expect(omens).toHaveLength(1);
    expect(omens[0].title).toBe('The Burden of Excess'); // Matches /no-(unsafe|unnecessary|redundant)/
    expect(omens[0].severity).toBe('moderate');
    expect(omens[0].description).toContain('Detected 1 errors, 0 warnings for rule: no-unsafe-member-access');
  });

  it('should escalate severity for many errors of a rule', () => {
    const results: LintResult[] = [
      {
        filePath: 'src/file8.ts',
        messages: Array(6).fill({ ruleId: 'no-unused-vars', severity: 2, message: 'unused', line: 1, column: 1, nodeType: 'Identifier' }),
        errorCount: 6,
        warningCount: 0,
        fixableErrorCount: 0,
        fixableWarningCount: 0,
        usedDeprecatedRules: [],
      },
    ];
    const omens = interpretLintResults(results);
    expect(omens).toHaveLength(1);
    expect(omens[0].title).toBe('The Whispering Ghost of Unused Variables');
    expect(omens[0].severity).toBe('severe'); // Escalated due to > 5 errors
  });

  it('should escalate severity for many warnings of a rule', () => {
    const results: LintResult[] = [
      {
        filePath: 'src/file9.ts',
        messages: Array(11).fill({ ruleId: 'max-len', severity: 1, message: 'Line too long', line: 1, column: 81, nodeType: 'Program' }),
        errorCount: 0,
        warningCount: 11,
        fixableErrorCount: 0,
        fixableWarningCount: 0,
        usedDeprecatedRules: [],
      },
    ];
    const omens = interpretLintResults(results);
    expect(omens).toHaveLength(1);
    expect(omens[0].title).toBe('The Endless Scroll');
    expect(omens[0].severity).toBe('moderate'); // Escalated due to > 10 warnings
  });
});
