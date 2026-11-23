#!/usr/bin/env node
import { Command } from 'commander';
import * as fs from 'fs';
import { sortAnomalies } from './sorter';
import { Anomaly, Rule, CategorizedAnomalies } from './types';

const program = new Command();

program
  .name('chronal-sorter')
  .description('CLI tool to categorize and prioritize temporal anomalies.')
  .version('1.0.0');

program
  .requiredOption('-a, --anomalies <file>', 'Path to a JSON file containing a list of anomalies.')
  .option('-r, --rules <file>', 'Path to a JSON file containing a list of categorization rules.', './rules.json')
  .action(async (options) => {
    try {
      const anomaliesPath = options.anomalies;
      const rulesPath = options.rules;

      // # Mock rationale: In a real-world scenario, fs.readFileSync would be mocked
      // # in tests to avoid actual file system access and ensure determinism.
      // # For this utility, we assume valid JSON files are provided via CLI.
      const anomaliesContent = fs.readFileSync(anomaliesPath, 'utf-8');
      const anomalies: Anomaly[] = JSON.parse(anomaliesContent);

      let rules: Rule[] = [];
      if (fs.existsSync(rulesPath)) {
        const rulesContent = fs.readFileSync(rulesPath, 'utf-8');
        rules = JSON.parse(rulesContent);
      } else {
        console.warn(`Warning: Rules file not found at ${rulesPath}. Using default categorization for all anomalies.`);
      }

      const sortedAnomalies: CategorizedAnomalies = sortAnomalies(anomalies, rules);

      console.log(JSON.stringify(sortedAnomalies, null, 2));
    } catch (error: any) {
      console.error(`Error: ${error.message}`);
      process.exit(1);
    }
  });

program.parse(process.argv);
