import { Command } from 'commander';
import { RippleManager } from './rippleManager';
import { RippleType } from './types';

const program = new Command();
const rippleManager = new RippleManager();

program
  .name('rrr')
  .description('CLI for logging and managing reality ripples and temporal anomalies.')
  .version('1.0.0');

program.command('add <type> <description>')
  .description('Add a new reality ripple.')
  .action(async (type: string, description: string) => {
    if (!(Object.values(RippleType) as string[]).includes(type)) {
      console.error(`Error: Invalid ripple type. Must be one of: ${Object.values(RippleType).join(', ')}`);
      process.exit(1);
    }
    try {
      const newRipple = await rippleManager.addRipple(type as RippleType, description);
      console.log(`
New Reality Ripple Logged:
  ID: ${newRipple.id}
  Type: ${newRipple.type}
  Description: ${newRipple.description}
  Timestamp: ${newRipple.timestamp}
`);
    } catch (error) {
      console.error(`Failed to add ripple: ${error instanceof Error ? error.message : String(error)}`);
      process.exit(1);
    }
  });

program.command('list')
  .description('List all recorded reality ripples.')
  .action(async () => {
    try {
      const ripples = await rippleManager.listRipples();
      if (ripples.length === 0) {
        console.log('No reality ripples recorded yet.');
        return;
      }
      console.log('\n--- Reality Ripple Log ---');
      ripples.forEach(ripple => {
        console.log(`
  ID: ${ripple.id}
  Type: ${ripple.type}
  Description: ${ripple.description}
  Timestamp: ${ripple.timestamp}`);
      });
      console.log('--------------------------\n');
    } catch (error) {
      console.error(`Failed to list ripples: ${error instanceof Error ? error.message : String(error)}`);
      process.exit(1);
    }
  });

program.command('filter <type>')
  .description('Filter reality ripples by type.')
  .action(async (type: string) => {
    if (!(Object.values(RippleType) as string[]).includes(type)) {
      console.error(`Error: Invalid ripple type. Must be one of: ${Object.values(RippleType).join(', ')}`);
      process.exit(1);
    }
    try {
      const filteredRipples = await rippleManager.filterRipples(type as RippleType);
      if (filteredRipples.length === 0) {
        console.log(`No '${type}' reality ripples found.`);
        return;
      }
      console.log(`\n--- Filtered Reality Ripples (${type}) ---`);
      filteredRipples.forEach(ripple => {
        console.log(`
  ID: ${ripple.id}
  Type: ${ripple.type}
  Description: ${ripple.description}
  Timestamp: ${ripple.timestamp}`);
      });
      console.log('------------------------------------------\n');
    } catch (error) {
      console.error(`Failed to filter ripples: ${error instanceof Error ? error.message : String(error)}`);
      process.exit(1);
    }
  });

program.parse(process.argv);
