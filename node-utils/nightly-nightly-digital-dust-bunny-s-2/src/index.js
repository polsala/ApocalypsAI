const fs = require('fs').promises;
const path = require('path');

async function getFileStats(filePath) {
  try {
    return await fs.stat(filePath);
  } catch (error) {
    // Ignore files we can't access (e.g., permission denied, broken symlinks)
    return null;
  }
}

async function findDustBunnies(directoryPath, ageThresholdDays, sizeThresholdMB) {
  const dustBunnies = [];
  const now = Date.now();
  const ageThresholdMs = ageThresholdDays * 24 * 60 * 60 * 1000;
  const sizeThresholdBytes = sizeThresholdMB * 1024 * 1024;

  async function scanDirectory(currentPath) {
    let entries;
    try {
      entries = await fs.readdir(currentPath, { withFileTypes: true });
    } catch (error) {
      console.error(`Warning: Could not read directory ${currentPath}: ${error.message}`);
      return;
    }

    for (const entry of entries) {
      const fullPath = path.join(currentPath, entry.name);
      if (entry.isDirectory()) {
        await scanDirectory(fullPath);
      } else if (entry.isFile()) {
        const stats = await getFileStats(fullPath);
        if (stats) {
          const isOld = (now - stats.mtimeMs) > ageThresholdMs;
          const isLarge = stats.size > sizeThresholdBytes;

          if (isOld && isLarge) {
            dustBunnies.push({
              path: fullPath,
              size: (stats.size / (1024 * 1024)).toFixed(2) + ' MB',
              lastModified: new Date(stats.mtimeMs).toISOString()
            });
          }
        }
      }
    }
  }

  await scanDirectory(directoryPath);
  return dustBunnies;
}

async function main() {
  const args = process.argv.slice(2);
  let directoryPath = args[0];
  let ageThresholdDays = 365; // Default 1 year
  let sizeThresholdMB = 100;  // Default 100 MB

  if (!directoryPath) {
    console.error('Usage: node src/index.js <directory_path> [--age <days>] [--size <MB>]');
    process.exit(1);
  }

  // Parse optional arguments
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--age' && args[i + 1]) {
      ageThresholdDays = parseInt(args[i + 1], 10);
      i++;
    } else if (args[i] === '--size' && args[i + 1]) {
      sizeThresholdMB = parseInt(args[i + 1], 10);
      i++;
    }
  }

  if (isNaN(ageThresholdDays) || ageThresholdDays <= 0) {
    console.error('Error: --age must be a positive number.');
    process.exit(1);
  }
  if (isNaN(sizeThresholdMB) || sizeThresholdMB <= 0) {
    console.error('Error: --size must be a positive number.');
    process.exit(1);
  }

  try {
    const stats = await fs.stat(directoryPath);
    if (!stats.isDirectory()) {
      console.error(`Error: '${directoryPath}' is not a directory.`);
      process.exit(1);
    }
  } catch (error) {
    console.error(`Error: Directory '${directoryPath}' not found or inaccessible: ${error.message}`);
    process.exit(1);
  }

  console.log(`\nSweeping for Digital Dust Bunnies in: ${directoryPath}`);
  console.log(`Criteria: Older than ${ageThresholdDays} days AND Larger than ${sizeThresholdMB} MB\n`);

  const bunnies = await findDustBunnies(directoryPath, ageThresholdDays, sizeThresholdMB);

  if (bunnies.length === 0) {
    console.log('✨ No digital dust bunnies found! Your digital space is sparkling clean. ✨');
  } else {
    console.log('🧹 Found these digital dust bunnies:');
    bunnies.forEach(bunny => {
      console.log(`- Path: ${bunny.path}`);
      console.log(`  Size: ${bunny.size}`);
      console.log(`  Last Modified: ${bunny.lastModified}\n`);
    });
    console.log(`\nTotal: ${bunnies.length} digital dust bunnies found. Time to sweep!`);
  }
}

if (require.main === module) {
  main();
}

module.exports = { findDustBunnies, getFileStats, main }; // Export main for testing CLI behavior
