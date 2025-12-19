const { getCosmicAlignment } = require('./compass');

/**
 * Runs the Nightly Cosmic Compass CLI utility.
 * Parses command-line arguments for date and location, then prints the cosmic alignment.
 */
function run() {
  const args = process.argv.slice(2);
  let dateInput = null;
  let locationInput = "the known universe";

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--date' && args[i + 1]) {
      dateInput = args[i + 1];
      i++;
    } else if (args[i] === '--location' && args[i + 1]) {
      locationInput = args[i + 1];
      i++;
    } else if (args[i] === '-h' || args[i] === '--help') {
      console.log(`
Usage: nightly-cosmic-compass [options]

Options:
  --date <YYYY-MM-DD>  Specify a date (defaults to today).
  --location <string>  Specify a location (defaults to "the known universe").
  -h, --help           Display this help message.
      `);
      process.exit(0);
    }
  }

  let date;
  if (dateInput) {
    date = new Date(dateInput);
    if (isNaN(date.getTime())) {
      console.error("Error: Invalid date format. Please use YYYY-MM-DD.");
      process.exit(1);
    }
  } else {
    date = new Date();
  }

  const result = getCosmicAlignment(date, locationInput);

  console.log(`
🌌 Nightly Cosmic Compass Reading 🌌

Date:      ${result.date}
Location:  ${result.location}

Today's Alignment: ✨ ${result.alignment} ✨
Influence:         "${result.influence}"

May your journey through the cosmos be guided by starlight!
  `);
}

// Only run the CLI if this file is executed directly
if (require.main === module) {
  run();
}
