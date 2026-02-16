import { RegretManager } from './regretManager';
import path from 'path';

const DATA_FILE = path.join(process.cwd(), 'temporal_echoes.json');
const manager = new RegretManager(DATA_FILE);

function printHelp() {
  console.log(`\n  Temporal Regret Resolver CLI\n\n  Usage:\n    npm run cli add <description>   - Add a new temporal echo (regret).\n    npm run cli list active         - List all active (unresolved) temporal echoes.\n    npm run cli list resolved       - List all resolved temporal echoes.\n    npm run cli resolve <id>        - Resolve a temporal echo by its ID.\n    npm run cli help                - Show this help message.\n  `);
}

async function main() {
  const args = process.argv.slice(2); // Remove 'node' and 'index.js'

  if (args.length === 0 || args[0] === 'help') {
    printHelp();
    return;
  }

  const command = args[0];
  const value = args.slice(1).join(' ');

  switch (command) {
    case 'add':
      if (!value) {
        console.error('Error: Description is required for "add" command.');
        printHelp();
        return;
      }
      const newRegret = manager.addRegret(value);
      console.log(`Added new temporal echo: "${newRegret.description}" (ID: ${newRegret.id})`);
      break;

    case 'list':
      if (value === 'active') {
        const activeRegrets = manager.listActiveRegrets();
        if (activeRegrets.length === 0) {
          console.log('No active temporal echoes found. The future is bright!');
        } else {
          console.log('\n--- Active Temporal Echoes ---');
          activeRegrets.forEach(r => {
            console.log(`ID: ${r.id}`);
            console.log(`  Description: "${r.description}"`);
            console.log(`  Logged: ${new Date(r.timestamp).toLocaleString()}`);
            console.log('------------------------------');
          });
        }
      } else if (value === 'resolved') {
        const resolvedRegrets = manager.listResolvedRegrets();
        if (resolvedRegrets.length === 0) {
          console.log('No resolved temporal echoes found. Keep up the good work!');
        } else {
          console.log('\n--- Resolved Temporal Echoes ---');
          resolvedRegrets.forEach(r => {
            console.log(`ID: ${r.id}`);
            console.log(`  Description: "${r.description}"`);
            console.log(`  Logged: ${new Date(r.timestamp).toLocaleString()}`);
            console.log(`  Resolved: ${new Date(r.resolvedAt!).toLocaleString()}`);
            console.log('--------------------------------');
          });
        }
      } else {
        console.error('Error: Invalid list subcommand. Use "active" or "resolved".');
        printHelp();
      }
      break;

    case 'resolve':
      if (!value) {
        console.error('Error: Regret ID is required for "resolve" command.');
        printHelp();
        return;
      }
      const resolved = manager.resolveRegret(value);
      if (resolved) {
        console.log(`Temporal echo "${resolved.description}" (ID: ${resolved.id}) resolved!`);
      } else {
        console.error(`Error: Temporal echo with ID "${value}" not found in active list.`);
      }
      break;

    default:
      console.error(`Error: Unknown command "${command}"`);
      printHelp();
      break;
  }
}

main();
