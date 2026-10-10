import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import * as toml from 'toml';

// Define a type for linting rules
interface LintRule {
  name: string;
  description: string;
  check: (content: any, filePath: string) => LintError[];
}

// Define a type for linting errors
interface LintError {
  rule: string;
  message: string;
  filePath: string;
  line?: number;
  column?: number;
}

// --- Sample Linting Rules ---

// Rule to check for empty configuration files
const emptyFileRule: LintRule = {
  name: 'empty-file',
  description: 'Configuration file should not be empty.',
  check: (content: any, filePath: string): LintError[] => {
    if (content === null || content === undefined || (typeof content === 'object' && Object.keys(content).length === 0)) {
      return [{ rule: 'empty-file', message: 'Configuration file is empty.', filePath }];
    }
    return [];
  }
};

// Rule to check for specific keys in JSON files (example)
const jsonKeyCheckRule: LintRule = {
  name: 'json-required-key',
  description: 'JSON files should contain a specific key (e.g., "version").',
  check: (content: any, filePath: string): LintError[] => {
    if (path.extname(filePath) === '.json') {
      if (!content || typeof content !== 'object' || !('version' in content)) {
        return [{ rule: 'json-required-key', message: 'JSON file is missing the required "version" key.', filePath }];
      }
    }
    return [];
  }
};

// Rule to check for common YAML indentation issues (basic check)
const yamlIndentationRule: LintRule = {
  name: 'yaml-indentation',
  description: 'Basic check for YAML indentation consistency.',
  check: (content: string, filePath: string): LintError[] => {
    if (path.extname(filePath) === '.yaml' || path.extname(filePath) === '.yml') {
      const lines = content.split('\n');
      let previousIndent = -1;
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        if (line.trim() === '') continue;
        const leadingSpaces = line.match(/^\s*/)?.[0].length || 0;
        if (previousIndent !== -1 && leadingSpaces <= previousIndent && !line.trim().startsWith('#')) {
          // This is a very basic check, real YAML parsers are more robust
          // For demonstration, we flag if indentation doesn't increase or stay same for non-comment lines
          // A more sophisticated rule would track parent-child relationships.
          // We'll focus on a simple case: if a line is less indented than the previous non-empty line, it's suspicious.
          if (leadingSpaces < previousIndent) {
             return [{ rule: 'yaml-indentation', message: `Potential indentation issue: line ${i + 1} has less indentation than expected.`, filePath, line: i + 1, column: leadingSpaces + 1 }];
          }
        }
        previousIndent = leadingSpaces;
      }
    }
    return [];
  }
};

// Combine all rules
const allRules: LintRule[] = [
  emptyFileRule,
  jsonKeyCheckRule,
  yamlIndentationRule
];

/**
 * Parses configuration content based on file extension.
 * @param content The raw file content.
 * @param filePath The path to the file.
 * @returns Parsed content or null if unsupported.
 */
function parseConfig(content: string, filePath: string): any | null {
  const ext = path.extname(filePath).toLowerCase();
  try {
    if (ext === '.json') {
      return JSON.parse(content);
    } else if (ext === '.yaml' || ext === '.yml') {
      return yaml.load(content);
    } else if (ext === '.toml') {
      return toml.parse(content);
    }
    return null; // Unsupported format
  } catch (error: any) {
    throw new Error(`Failed to parse ${filePath}: ${error.message}`);
  }
}

/**
 * Lints a given configuration file.
 * @param filePath The path to the configuration file.
 * @returns An array of LintError objects.
 */
export function lintConfigFile(filePath: string): LintError[] {
  if (!fs.existsSync(filePath)) {
    throw new Error(`File not found: ${filePath}`);
  }

  const content = fs.readFileSync(filePath, 'utf-8');
  const errors: LintError[] = [];

  // Parse content first to catch syntax errors
  let parsedContent: any;
  try {
    parsedContent = parseConfig(content, filePath);
  } catch (e: any) {
    errors.push({
      rule: 'syntax-error',
      message: e.message,
      filePath: filePath
    });
    return errors; // Stop if parsing fails
  }

  // Apply all rules
  for (const rule of allRules) {
    try {
      const ruleErrors = rule.check(parsedContent, filePath);
      errors.push(...ruleErrors);
    } catch (e: any) {
      // Catch errors within rule execution itself
      errors.push({
        rule: `rule-execution-error:${rule.name}`,
        message: `Error executing rule '${rule.name}': ${e.message}`,
        filePath: filePath
      });
    }
  }

  return errors;
}

// --- CLI Entry Point ---

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: nightly-ts-config-linter <path-to-config-file>');
    process.exit(1);
  }

  const filePath = path.resolve(args[0]);
  try {
    const lintErrors = lintConfigFile(filePath);
    if (lintErrors.length > 0) {
      console.error(`Linting failed for ${filePath}:`);
      lintErrors.forEach(err => {
        let errorMsg = `  - [${err.rule}] ${err.message} (${err.filePath})`;
        if (err.line !== undefined) {
          errorMsg += ` at line ${err.line}`;
          if (err.column !== undefined) {
            errorMsg += `, column ${err.column}`;
          }
        }
        console.error(errorMsg);
      });
      process.exit(1);
    } else {
      console.log(`Linting successful for ${filePath}. No issues found.`);
      process.exit(0);
    }
  } catch (error: any) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

// Execute main function if this script is run directly
if (require.main === module) {
  main();
}
