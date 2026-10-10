export interface LintMessage {
  ruleId: string | null;
  severity: number; // 1 for warning, 2 for error
  message: string;
  line: number;
  column: number;
  nodeType: string;
  endLine?: number;
  endColumn?: number;
}

export interface LintResult {
  filePath: string;
  messages: LintMessage[];
  errorCount: number;
  warningCount: number;
  fixableErrorCount: number;
  fixableWarningCount: number;
  usedDeprecatedRules: any[]; // Simplified for this example
}

export interface CodeOmen {
  title: string;
  description: string;
  advice: string;
  severity: 'minor' | 'moderate' | 'severe' | 'prophecy';
}

export interface OmenRule {
  match: string | RegExp; // RuleId or pattern to match
  omenTitle: string;
  omenDescription: string;
  advice: string;
  severity: 'minor' | 'moderate' | 'severe';
}
