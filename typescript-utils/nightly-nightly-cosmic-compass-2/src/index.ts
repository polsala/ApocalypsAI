import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { Command } from 'commander';
import chalk from 'chalk';
import { PackageJson, OutdatedPackage, AuditReport } from './types';

export const program = new Command(); // Export program for testing

program
  .name('cosmic-compass')
  .description('A CLI tool that scans package.json dependencies for outdated, insecure, or unused packages and suggests alignment.')
  .version('1.0.0');

program.action(async () => {
  console.log(chalk.magenta('\n🌌 Initiating Cosmic Compass Scan...'));
  console.log(chalk.magenta('-------------------------------------\n'));

  try {
    const packageJsonPath = './package.json';
    const packageJsonContent = readFileSync(packageJsonPath, 'utf8');
    const packageJson: PackageJson = JSON.parse(packageJsonContent);

    console.log(chalk.cyan(`🔭 Scanning project: ${packageJson.name}@${packageJson.version}\n`));

    // --- Drift Detection: Outdated Dependencies ---
    console.log(chalk.yellow('🌠 Detecting Dependency Drift (Outdated Packages):\n'));
    let outdatedOutput: string;
    try {
      outdatedOutput = execSync('npm outdated --json', { stdio: 'pipe' }).toString();
    } catch (error: any) {
      // npm outdated exits with non-zero code if outdated packages are found, but still provides JSON stdout
      outdatedOutput = error.stdout ? error.stdout.toString() : '{}';
    }
    const outdatedPackages: Record<string, OutdatedPackage> = JSON.parse(outdatedOutput);

    const outdatedCount = Object.keys(outdatedPackages).length;
    if (outdatedCount > 0) {
      console.log(chalk.red(`  ${outdatedCount} packages are drifting out of alignment!\n`));
      Object.entries(outdatedPackages).forEach(([pkgName, details]) => {
        console.log(
          `  - ${chalk.blue(pkgName)}: ${chalk.gray(details.current)} -> ${chalk.green(details.latest)} (wanted: ${details.wanted})`
        );
      });
      console.log(chalk.yellow('\n  Consider running `npm update` or `npm install <package>@latest` to realign.\n'));
    } else {
      console.log(chalk.green('  All dependencies are perfectly aligned with the latest cosmic currents. No drift detected.\n'));
    }

    // --- Temporal Anomalies: Security Vulnerabilities ---
    console.log(chalk.yellow('🚨 Scanning for Temporal Anomalies (Security Vulnerabilities):\n'));
    let auditOutput: string;
    try {
      auditOutput = execSync('npm audit --json', { stdio: 'pipe' }).toString();
    } catch (error: any) {
      // npm audit exits with non-zero code if vulnerabilities are found
      auditOutput = error.stdout ? error.stdout.toString() : '{}';
    }
    const auditReport: AuditReport = JSON.parse(auditOutput);

    const vulnerabilities = auditReport.metadata.vulnerabilities;
    const totalVulnerabilities = Object.values(vulnerabilities).reduce((sum, count) => sum + count, 0);

    if (totalVulnerabilities > 0) {
      console.log(chalk.red(`  ${totalVulnerabilities} security anomalies detected!\n`));
      for (const advisoryId in auditReport.advisories) {
        const advisory = auditReport.advisories[advisoryId];
        console.log(
          `  - ${chalk.red(advisory.severity.toUpperCase())}: ${chalk.blue(advisory.module_name)} - ${advisory.title}`
        );
        console.log(`    Vulnerable: ${advisory.vulnerable_versions}, Patched: ${advisory.patched_versions}`);
        console.log(`    More info: ${advisory.url}\n`);
      }
      console.log(chalk.yellow('  Run `npm audit fix` to attempt to resolve these anomalies.\n'));
    } else {
      console.log(chalk.green('  No security anomalies detected. Your cosmic vessel is secure.\n'));
    }

    console.log(chalk.magenta('✨ Cosmic Compass Scan Complete. May your journey be stable and secure! ✨\n'));

  } catch (error: any) {
    if (error.code === 'ENOENT' && error.path === 'package.json') {
      console.error(chalk.red('❌ Error: No package.json found in the current directory. Are you in a Node.js project?'));
    } else if (error.stderr) {
      console.error(chalk.red(`❌ Cosmic disturbance detected: ${error.stderr.toString()}`));
    } else {
      console.error(chalk.red(`❌ An unexpected cosmic event occurred: ${error.message}`));
    }
    process.exit(1);
  }
});

// Only parse if not in a test environment to avoid issues with Jest
if (process.env.NODE_ENV !== 'test') {
  program.parse(process.argv);
}
