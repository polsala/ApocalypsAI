import { convertToCosmicDate } from './cosmicConverter';

/**
 * Main function for the CLI utility.
 * Parses command-line arguments and prints the cosmic date.
 */
function main() {
  const args = process.argv.slice(2);
  const dateString = args[0];

  if (!dateString) {
    console.error("Usage: npm start <YYYY-MM-DD>");
    process.exit(1);
  }

  const cosmicDate = convertToCosmicDate(dateString);

  if (cosmicDate) {
    console.log(cosmicDate.fullCosmicString);
  } else {
    console.error(`Error: Could not convert "${dateString}". Please use YYYY-MM-DD format.`);
    process.exit(1);
  }
}

main();
