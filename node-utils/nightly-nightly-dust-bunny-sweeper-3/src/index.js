const { program } = require('commander');
const { promises: fs } = require('fs');
const path = require('path');

// Whimsical patterns for digital dust bunnies
const DUST_BUNNY_PATTERNS = [
  'node_modules',
  'dist',
  'build',
  '.next',
  '.cache',
  'coverage',
  'temp',
  'tmp',
  '.DS_Store',
  'Thumbs.db',
  '.log$', // Matches files ending with .log
  '.bak$', // Matches files ending with .bak
  '.swp$', // Matches files ending with .swp
  '.swo$', // Matches files ending with .swo
  '.vscode-test',
  '.nyc_output',
  // '.git/objects', // Git objects can be large, but usually managed by git itself. For extreme cases.
  // '.git/refs/remotes', // Similar to above.
];

// Function to check if a path matches any dust bunny pattern
function isDustBunny(itemPath, stats) {
  const basename = path.basename(itemPath);

  for (const pattern of DUST_BUNNY_PATTERNS) {
    if (pattern.startsWith('.') && basename === pattern) {
      return true; // Exact match for hidden files/dirs like .DS_Store, .next
    }
    if (!pattern.startsWith('.') && basename === pattern) {
      return true; // Exact match for common dirs like node_modules, dist
    }
    if (pattern.endsWith('$') && basename.match(new RegExp(pattern))) {
      return true; // Regex match for file extensions like .log
    }
  }

  return false;
}

// Recursive function to find dust bunnies
async function findDustBunnies(dir, foundBunnies = []) {
  let items;
  try {
    items = await fs.readdir(dir, { withFileTypes: true });
  } catch (error) {
    if (error.code === 'ENOENT' || error.code === 'EACCES') {
      // console.warn(`Skipping inaccessible directory: ${dir}`); // Suppress for cleaner output
      return foundBunnies;
    }
    throw error;
  }

  for (const item of items) {
    const itemPath = path.join(dir, item.name);

    // Skip symbolic links to prevent infinite loops and external deletions
    if (item.isSymbolicLink()) {
      continue;
    }

    if (isDustBunny(itemPath, item)) {
      foundBunnies.push(itemPath);
      // If it's a directory dust bunny, no need to traverse inside it
      continue;
    }

    if (item.isDirectory()) {
      await findDustBunnies(itemPath, foundBunnies);
    }
  }

  // After traversing, check if the directory itself is empty
  // This check should happen after all children are processed
  const remainingItems = await fs.readdir(dir);
  if (remainingItems.length === 0 && dir !== process.cwd()) { // Don't mark the root as empty unless it truly is after all operations
    foundBunnies.push(dir + ' (empty directory)'); // Mark as empty directory
  }

  return foundBunnies;
}

async function sweep(targetPath, dryRun, deleteFiles) {
  console.log(`\n🧹 Starting the Nightly Digital Dust Bunny Sweeper in '${targetPath}'...\n`);

  const foundBunnies = await findDustBunnies(targetPath);

  if (foundBunnies.length === 0) {
    console.log('✨ No digital dust bunnies found! Your space is sparkling clean.');
    return;
  }

  console.log(`🔍 Found ${foundBunnies.length} digital dust bunnies:\n`);
  foundBunnies.forEach(bunny => console.log(`  - ${bunny}`));
  console.log('\n');

  if (dryRun) {
    console.log('👀 This was a dry run. No files were actually deleted.');
    console.log('To sweep them away for real, run with the `--delete` flag.');
  } else if (deleteFiles) {
    console.log('🌪️ Sweeping away the digital fluff... Stand by!');
    for (const bunny of foundBunnies) {
      try {
        // Handle empty directory special case
        if (bunny.endsWith(' (empty directory)')) {
          const dirToDelete = bunny.replace(' (empty directory)', '');
          await fs.rm(dirToDelete, { recursive: false, force: true }); // Use fs.rm for empty dir
          console.log(`  ✅ Swept away empty directory: ${dirToDelete}`);
        } else {
          await fs.rm(bunny, { recursive: true, force: true });
          console.log(`  ✅ Swept away: ${bunny}`);
        }
      } catch (error) {
        console.error(`  ❌ Failed to sweep ${bunny}: ${error.message}`);
      }
    }
    console.log('\n✨ Your project space feels lighter and tidier! Happy coding!');
  } else {
    console.log('👀 No action specified. Use `--dry-run` to preview or `--delete` to sweep.');
  }
}

async function main() {
  program
    .name('nightly-dust-bunny-sweeper')
    .description('A whimsical utility to sweep away digital clutter.')
    .option('-p, --path <path>', 'The directory to scan.', process.cwd())
    .option('-d, --delete', 'Enable deletion of identified dust bunnies. Use with caution!')
    .option('-r, --dry-run', 'Perform a dry run, reporting what would be deleted.', true) // Default to true
    .action(async (options) => {
      // If --delete is present, then --dry-run should be false
      const dryRun = options.delete ? false : options.dryRun;
      await sweep(options.path, dryRun, options.delete);
    });

  program.parse(process.argv);
}

if (require.main === module) {
  main();
}

// Export for testing
module.exports = { sweep, findDustBunnies, isDustBunny, DUST_BUNNY_PATTERNS };
