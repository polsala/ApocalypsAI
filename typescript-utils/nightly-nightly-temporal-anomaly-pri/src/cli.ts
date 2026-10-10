import { readFileSync } from 'fs';
import { Anomaly, PrioritizationRule } from './types';
import { prioritizeAnomalies } from './prioritizer';

/**
 * Displays the help message for the CLI tool.
 */
function displayHelp(): void {
    console.log(`
Nightly Temporal Anomaly Prioritizer (Nightly-TAP)

Usage:
  nightly-tap prioritize <anomalies_file.json> <rules_file.json>
  nightly-tap help

Description:
  Categorizes and prioritizes temporal anomalies based on user-defined rules.

Arguments:
  <anomalies_file.json>  Path to a JSON file containing an array of Anomaly objects.
  <rules_file.json>      Path to a JSON file containing an array of PrioritizationRule objects.
            `);
}

/**
 * Runs the prioritization process, reads files, and outputs results.
 * @param anomaliesPath Path to the anomalies JSON file.
 * @param rulesPath Path to the rules JSON file.
 */
function runPrioritize(anomaliesPath: string, rulesPath: string): void {
    try {
        const anomaliesContent = readFileSync(anomaliesPath, 'utf8');
        const rulesContent = readFileSync(rulesPath, 'utf8');

        const anomalies: Anomaly[] = JSON.parse(anomaliesContent);
        const rules: PrioritizationRule[] = JSON.parse(rulesContent);

        const prioritized = prioritizeAnomalies(anomalies, rules);

        console.log(JSON.stringify(prioritized, null, 2));
    } catch (error: any) {
        console.error(`Error: ${error.message}`);
        process.exit(1);
    }
}

/**
 * Main function to handle CLI arguments and dispatch commands.
 * @param args Command-line arguments (excluding 'node' and script path).
 */
export function main(args: string[]): void {
    const command = args[0];

    if (command === 'prioritize' && args.length === 3) {
        runPrioritize(args[1], args[2]);
    } else if (command === 'help' || !command) {
        displayHelp();
    } else {
        console.error('Invalid command or arguments. Use "nightly-tap help" for usage.');
        process.exit(1);
    }
}
