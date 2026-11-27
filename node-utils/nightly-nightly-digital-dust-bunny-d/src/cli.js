#!/usr/bin/env node
const { indexDirectory, searchIndex } = require('./index');
const path = require('path');

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command) {
    console.log('Usage: dust-bunny-duster <command> [options]');
    console.log('Commands:');
    console.log('  index <path/to/directory> [output/path/to/index.json]');
    console.log('  search <keyword> [path/to/index.json]');
    process.exit(1);
  }

  switch (command) {
    case 'index':
      const dirPath = args[1];
      const outputPath = args[2] || 'dust-bunny-index.json';
      if (!dirPath) {
        console.error('Error: Directory path is required for indexing.');
        process.exit(1);
      }
      try {
        // Resolve to absolute path for consistency, especially in tests
        const absoluteDirPath = path.resolve(dirPath);
        const absoluteOutputPath = path.resolve(outputPath);
        await indexDirectory(absoluteDirPath, absoluteOutputPath);
      } catch (error) {
        process.exit(1);
      }
      break;
    case 'search':
      const keyword = args[1];
      const indexPath = args[2] || 'dust-bunny-index.json';
      if (!keyword) {
        console.error('Error: Keyword is required for searching.');
        process.exit(1);
      }
      try {
        const absoluteIndexPath = path.resolve(indexPath);
        await searchIndex(keyword, absoluteIndexPath);
      } catch (error) {
        process.exit(1);
      }
      break;
    default:
      console.error(`Unknown command: ${command}`);
      process.exit(1);
  }
}

main();
