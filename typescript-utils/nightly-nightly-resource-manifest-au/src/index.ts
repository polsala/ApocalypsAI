import * as fs from 'fs';
import { ResourceManifest, AuditReport, AuditReportItem } from './types';
import { getResourceUnit } from './resources';

export function auditManifests(
  desiredManifest: ResourceManifest,
  currentManifest: ResourceManifest
): AuditReport {
  const report: AuditReport = [];

  // Check desired resources against current
  for (const resourceName in desiredManifest) {
    const needed = desiredManifest[resourceName];
    const current = currentManifest[resourceName] || 0;
    const difference = current - needed;
    const unit = getResourceUnit(resourceName);

    let status: AuditReportItem['status'];
    let message: string;

    if (difference < 0) {
      status = 'shortage';
      message = `Critical Shortage! You need ${Math.abs(difference)} more ${resourceName} (${unit}s).`;
    } else if (difference > 0) {
      status = 'surplus';
      message = `Unexpected Surplus! You have ${difference} more ${resourceName} (${unit}s) than desired.`;
    } else {
      status = 'ok';
      message = `Optimal Balance Achieved for ${resourceName}.`;
    }

    report.push({
      resourceName,
      status,
      needed,
      current,
      difference,
      message,
    });
  }

  // Check current resources not in desired manifest (pure surplus)
  for (const resourceName in currentManifest) {
    if (!(resourceName in desiredManifest)) {
      const current = currentManifest[resourceName];
      const unit = getResourceUnit(resourceName);
      report.push({
        resourceName,
        status: 'surplus',
        needed: 0,
        current,
        difference: current,
        message: `Unexpected Surplus! ${resourceName} is not in your desired manifest, but you have ${current} (${unit}s).`,
      });
    }
  }

  return report;
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length !== 2) {
    console.error('Usage: ts-node src/index.ts <path/to/desired.json> <path/to/current.json>');
    process.exit(1);
  }

  const desiredManifestPath = args[0];
  const currentManifestPath = args[1];

  try {
    const desiredManifest: ResourceManifest = JSON.parse(fs.readFileSync(desiredManifestPath, 'utf8'));
    const currentManifest: ResourceManifest = JSON.parse(fs.readFileSync(currentManifestPath, 'utf8'));

    const auditReport = auditManifests(desiredManifest, currentManifest);
    console.log(JSON.stringify(auditReport, null, 2));
  } catch (error: any) {
    console.error(`Error auditing manifests: ${error.message}`);
    process.exit(1);
  }
}
