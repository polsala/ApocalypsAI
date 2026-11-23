import { Command } from 'commander';
import { v4 as uuidv4 } from 'uuid';

// --- Type Definitions ---

enum RippleType {
  Temporal = 'Temporal',
  Spatial = 'Spatial',
  Causal = 'Causal',
  Echo = 'Echo',
  RealityDistortion = 'RealityDistortion',
}

enum Severity {
  Minor = 'Minor',
  Moderate = 'Moderate',
  Severe = 'Severe',
  Critical = 'Critical',
}

enum Priority {
  Low = 'Low',
  Medium = 'Medium',
  High = 'High',
  Urgent = 'Urgent',
}

interface RippleReport {
  id: string;
  type: RippleType;
  severity: Severity;
  description: string;
  location: string;
  observedAt: Date;
  assignedPriority?: Priority; // Optional, will be set by prioritization logic
}

// --- Core Logic ---

/**
 * Assigns a priority to a given RippleReport based on its type and severity.
 * @param ripple The ripple report to prioritize.
 * @returns The calculated Priority.
 */
export function prioritizeRipple(ripple: RippleReport): Priority {
  switch (ripple.severity) {
    case Severity.Critical:
      return Priority.Urgent;
    case Severity.Severe:
      if (ripple.type === RippleType.Causal || ripple.type === RippleType.Temporal) {
        return Priority.High;
      }
      return Priority.Medium;
    case Severity.Moderate:
      if (ripple.type === RippleType.Temporal || ripple.type === RippleType.RealityDistortion) {
        return Priority.Medium;
      }
      return Priority.Low;
    case Severity.Minor:
    default:
      return Priority.Low;
  }
}

// --- CLI Setup ---

const program = new Command();

program
  .name('reality-ripple-reporter')
  .description('CLI tool to report and prioritize reality ripples.')
  .version('1.0.0');

program.command('report')
  .description('Report a new reality ripple.')
  .requiredOption('--type <type>', 'Type of the ripple (Temporal, Spatial, Causal, Echo, RealityDistortion)')
  .requiredOption('--severity <severity>', 'Severity of the ripple (Minor, Moderate, Severe, Critical)')
  .requiredOption('--description <description>', 'A brief description of the ripple')
  .requiredOption('--location <location>', 'Observed location of the ripple')
  .action((options) => {
    const { type, severity, description, location } = options;

    // Validate enums
    if (!Object.values(RippleType).includes(type as RippleType)) {
      console.error(`Error: Invalid ripple type '${type}'. Allowed types: ${Object.values(RippleType).join(', ')}`);
      process.exit(1);
    }
    if (!Object.values(Severity).includes(severity as Severity)) {
      console.error(`Error: Invalid severity '${severity}'. Allowed severities: ${Object.values(Severity).join(', ')}`);
      process.exit(1);
    }

    const newRipple: RippleReport = {
      id: uuidv4(),
      type: type as RippleType,
      severity: severity as Severity,
      description,
      location,
      observedAt: new Date(),
    };

    newRipple.assignedPriority = prioritizeRipple(newRipple);

    console.log('Reporting Reality Ripple:');
    console.log(`  ID: ${newRipple.id}`);
    console.log(`  Type: ${newRipple.type}`);
    console.log(`  Severity: ${newRipple.severity}`);
    console.log(`  Description: ${newRipple.description}`);
    console.log(`  Location: ${newRipple.location}`);
    console.log(`  Observed At: ${newRipple.observedAt.toISOString()}`);
    console.log(`  Assigned Priority: ${newRipple.assignedPriority}`);
  });

program.parse(process.argv);

// If no command is provided, show help
if (!process.argv.slice(2).length) {
  program.outputHelp();
}
