import { scanForTemporalEchoes } from './scanner';
import { ChronoCleanerConfig, TemporalEcho } from './types';
import * as path from 'path';
import * as minimist from 'minimist';

function printHelp() {
  console.log(`
Nightly Chrono-Cleaner - Tidy Your Project's Timeline

Usage: npx nightly-chrono-cleaner [options]

Options:
  --path <dir>        The directory to scan (default: current working directory).
  --stale-days <num>  Number of days after which a file is considered stale (default: 365).
  --ignore <pattern>  Comma-separated patterns to ignore (e.g., node_modules,dist).
  --format <type>     Output format: 'text' or 'json' (default: text).
  --help              Display this help message.

Examples:
  npx nightly-chrono-cleaner --path ./src --stale-days 180
  npx nightly-chrono-cleaner --ignore "node_modules,dist,.git" --format json
`);
}

async function main() {
  const argv = minimist(process.argv.slice(2));

  if (argv.help) {
    printHelp();
    process.exit(0);
  }

  const config: ChronoCleanerConfig = {
    scanPath: path.resolve(argv.path || '.'),
    staleDays: parseInt(argv['stale-days'] || '365', 10),
    ignorePatterns: (argv.ignore ? String(argv.ignore).split(',') : []).map(p => p.trim()),
    reportFormat: argv.format === 'json' ? 'json' : 'text',
  };

  if (isNaN(config.staleDays) || config.staleDays <= 0) {
    console.error('Error: --stale-days must be a positive number.');
    printHelp();
    process.exit(1);
  }

  console.log(`Scanning for temporal echoes in: ${config.scanPath}`);
  console.log(`Considering files stale after: ${config.staleDays} days`);
  if (config.ignorePatterns.length > 0) {
    console.log(`Ignoring patterns: ${config.ignorePatterns.join(', ')}`);
  }
  console.log('---');

  try {
    const echoes = await scanForTemporalEchoes(config);

    if (echoes.length === 0) {
      console.log('No temporal echoes detected. Your timeline is pristine!');
      return;
    }

    if (config.reportFormat === 'json') {
      console.log(JSON.stringify(echoes, null, 2));
    } else {
      console.log(`Detected ${echoes.length} temporal echo(es):`);
      echoes.forEach(echo => {
        let details = '';
        if (echo.reason === 'stale') {
          details = `(Stale for ${echo.ageDays} days, last modified: ${echo.lastModified?.toLocaleDateString()})`;
        } else if (echo.reason === 'deprecated-marker') {
          details = `(Contains marker: "${echo.markerContent}")`;
        }
        console.log(`- ${echo.filePath} ${details}`);
      });
      console.log('\nRecommendation: Review these echoes. Consider archiving or deleting them to prevent timeline distortions.');
    }
  } catch (error: any) {
    console.error(`An error occurred during the scan: ${error.message}`);
    process.exit(1);
  }
}

main();
