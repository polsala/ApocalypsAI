#!/usr/bin/env node
const emissionFactors = {
  car: 0.21,
  bus: 0.105,
  train: 0.041,
  plane: 0.254,
};

function printUsage() {
  console.error('Usage: node src/main.js <distance_km> <mode>');
  console.error('Modes: car, bus, train, plane');
}

function main() {
  const args = process.argv.slice(2);
  if (args.length !== 2) {
    printUsage();
    process.exit(1);
  }
  const distance = parseFloat(args[0]);
  const mode = args[1].toLowerCase();
  if (isNaN(distance) || distance < 0) {
    console.error('Error: distance must be a non-negative number');
    process.exit(1);
  }
  const factor = emissionFactors[mode];
  if (factor === undefined) {
    console.error(`Error: unknown mode '${mode}'.`);
    printUsage();
    process.exit(1);
  }
  const emission = distance * factor;
  console.log(`Estimated CO2 emission: ${emission.toFixed(1)} kg`);
}

if (require.main === module) {
  main();
}
