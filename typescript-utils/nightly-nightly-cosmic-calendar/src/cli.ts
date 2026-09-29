import { earthToCosmic, cosmicToEarth } from './index';

function printHelp() {
  console.log("Nightly Cosmic Calendar Converter");
  console.log("---------------------------------");
  console.log("Usage:");
  console.log("  cosmic-calendar earth-to-cosmic <YYYY-MM-DD>");
  console.log("  cosmic-calendar cosmic-to-earth <cosmicYear> <phaseName> <cycle>");
  console.log("\nExamples:");
  console.log("  cosmic-calendar earth-to-cosmic 2024-04-23");
  console.log("  cosmic-calendar cosmic-to-earth 25 Nebula Bloom 1");
  console.log("\nCosmic Phases:");
  console.log("  Nebula Bloom, Void Gaze, Stellar Drift, Comet's Kiss, Dark Matter Harvest,");
  console.log("  Galactic Whisper, Quantum Ripple, Echoing Singularity, Celestial Alignment,");
  console.log("  Cosmic Dustfall, Event Horizon, Astral Rebirth, Interstellar Drift");
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    printHelp();
    process.exit(0);
  }

  const command = args[0];

  try {
    if (command === 'earth-to-cosmic') {
      if (args.length !== 2) {
        console.error("Error: Missing Earth date. Usage: cosmic-calendar earth-to-cosmic <YYYY-MM-DD>");
        process.exit(1);
      }
      const earthDateString = args[1];
      const cosmicDate = earthToCosmic(earthDateString);
      console.log(`Earth Date: ${earthDateString}`);
      console.log(`Cosmic Date: Cosmic Year ${cosmicDate.cosmicYear}, Phase of the ${cosmicDate.phase}, Cycle ${cosmicDate.cycle}`);
    } else if (command === 'cosmic-to-earth') {
      if (args.length !== 4) {
        console.error("Error: Missing cosmic date components. Usage: cosmic-calendar cosmic-to-earth <cosmicYear> <phaseName> <cycle>");
        process.exit(1);
      }
      const cosmicYear = parseInt(args[1], 10);
      const phaseName = args[2];
      const cycle = parseInt(args[3], 10);

      if (isNaN(cosmicYear) || isNaN(cycle)) {
        console.error("Error: Cosmic Year and Cycle must be valid numbers.");
        process.exit(1);
      }

      const earthDateString = cosmicToEarth(cosmicYear, phaseName, cycle);
      console.log(`Cosmic Date: Cosmic Year ${cosmicYear}, Phase of the ${phaseName}, Cycle ${cycle}`);
      console.log(`Earth Date: ${earthDateString}`);
    } else {
      console.error(`Error: Unknown command "${command}".`);
      printHelp();
      process.exit(1);
    }
  } catch (error: any) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

main();
