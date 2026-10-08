import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

// Define the structure for a configuration rule
interface Rule {
  name: string;
  description: string;
  // The check function takes the configuration object and returns an array of errors
  check: (config: any) => string[];
}

// Basic rules for configuration linting
const defaultRules: Rule[] = [
  {
    name: "require-app-name",
    description: "Configuration must have an 'appName' field.",
    check: (config) => {
      if (!config.appName) {
        return ["'appName' field is missing."];
      }
      return [];
    }
  },
  {
    name: "valid-log-level",
    description: "'logLevel' must be one of INFO, WARN, ERROR, DEBUG.",
    check: (config) => {
      const validLevels = ["INFO", "WARN", "ERROR", "DEBUG"];
      if (config.logLevel && !validLevels.includes(config.logLevel.toUpperCase())) {
        return [`Invalid logLevel: ${config.logLevel}. Must be one of ${validLevels.join(', ')}.`];
      }
      return [];
    }
  },
  {
    name: "features-object",
    description: "The 'features' field should be an object.",
    check: (config) => {
      if (config.features && typeof config.features !== 'object') {
        return ["'features' field must be an object."];
      }
      return [];
    }
  }
];

// Linter class to manage rules and perform checks
class Linter {
  private rules: Rule[];

  constructor(rules: Rule[] = defaultRules) {
    this.rules = rules;
  }

  addRule(rule: Rule): void {
    this.rules.push(rule);
  }

  lint(configPath: string): string[] {
    let configContent;
    try {
      const fileExtension = path.extname(configPath).toLowerCase();
      const rawContent = fs.readFileSync(configPath, 'utf-8');

      if (fileExtension === '.json') {
        configContent = JSON.parse(rawContent);
      } else if (fileExtension === '.yaml' || fileExtension === '.yml') {
        configContent = yaml.load(rawContent);
      } else {
        throw new Error(`Unsupported file extension: ${fileExtension}. Only JSON and YAML are supported.`);
      }

    } catch (error: any) {
      return [`Error reading or parsing file ${configPath}: ${error.message}`];
    }

    const errors: string[] = [];
    for (const rule of this.rules) {
      const ruleErrors = rule.check(configContent);
      if (ruleErrors.length > 0) {
        errors.push(`Rule '${rule.name}': ${ruleErrors.join('; ')}`);
      }
    }
    return errors;
  }
}

// Main execution logic
async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: nightly-ts-config-linter <path_to_config_file>");
    process.exit(1);
  }

  const configPath = args[0];
  const linter = new Linter();
  const lintErrors = linter.lint(configPath);

  if (lintErrors.length > 0) {
    console.error("Configuration linting failed:");
    lintErrors.forEach(err => console.error(`- ${err}`));
    process.exit(1);
  } else {
    console.log("Configuration linting passed successfully!");
    process.exit(0);
  }
}

main();
