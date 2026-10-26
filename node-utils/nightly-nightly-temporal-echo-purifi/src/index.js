const fs = require('fs');
const path = require('path');

function parseArgs() {
  const args = {};
  process.argv.slice(2).forEach((arg, i, arr) => {
    if (arg.startsWith('--')) {
      const key = arg.substring(2);
      const value = arr[i + 1];
      if (value && !value.startsWith('--')) {
        args[key] = value;
      } else {
        args[key] = true; // Handle boolean flags if any, though not used here yet
      }
    }
  });
  return args;
}

function getFileAgeInDays(filePath) {
  try {
    const stats = fs.statSync(filePath);
    const now = new Date();
    const mtime = new Date(stats.mtime);
    const diffTime = Math.abs(now.getTime() - mtime.getTime());
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  } catch (error) {
    console.error(`Error getting stats for ${filePath}: ${error.message}`);
    return -1; // Indicate error
  }
}

function scanDirectoryForEchoes(dirPath, maxAgeDays) {
  const echoes = [];
  if (!fs.existsSync(dirPath)) {
    console.error(`Error: Directory not found at '${dirPath}'`);
    return echoes;
  }
  if (!fs.lstatSync(dirPath).isDirectory()) {
    console.error(`Error: Path '${dirPath}' is not a directory.`);
    return echoes;
  }

  try {
    const files = fs.readdirSync(dirPath);
    for (const file of files) {
      const filePath = path.join(dirPath, file);
      const age = getFileAgeInDays(filePath);
      if (age > maxAgeDays) {
        echoes.push({ filePath, age });
      }
    }
  } catch (error) {
    console.error(`Error scanning directory '${dirPath}': ${error.message}`);
  }
  return echoes;
}

function reportEchoes(echoes) {
  if (echoes.length === 0) {
    console.log("\n[Temporal Echo Purifier] No significant temporal echoes detected. Your digital realm is pristine... for now.");
    return;
  }

  console.log("\n[Temporal Echo Purifier] Initiating Echo Scan Report...");
  console.log("------------------------------------------------------");
  console.log(`Detected ${echoes.length} temporal echoes requiring purification consideration:\n`);

  echoes.sort((a, b) => b.age - a.age).forEach(echo => {
    console.log(`  - Echo: ${echo.filePath} (Age: ${echo.age} days)`);
    console.log(`    Suggested Purification: Consider archiving to the Void, or perhaps a gentle deletion.`);
  });

  console.log("\n------------------------------------------------------");
  console.log("Purification Protocol: Dry Run Complete. No files were altered.");
  console.log("Proceed with manual purification at your discretion, wanderer.");
}

function main() {
  const args = parseArgs();
  const dirPath = args.path;
  const maxAgeDays = parseInt(args.age, 10);

  if (!dirPath || isNaN(maxAgeDays)) {
    console.error("Usage: node src/index.js --path <directory> --age <days>");
    process.exit(1);
  }

  console.log(`[Temporal Echo Purifier] Scanning '${dirPath}' for echoes older than ${maxAgeDays} days...`);
  const echoes = scanDirectoryForEchoes(dirPath, maxAgeDays);
  reportEchoes(echoes);
}

// Export for testing
if (process.env.NODE_ENV === 'test') {
  module.exports = {
    parseArgs,
    getFileAgeInDays,
    scanDirectoryForEchoes,
    reportEchoes,
    main
  };
} else {
  main();
}
