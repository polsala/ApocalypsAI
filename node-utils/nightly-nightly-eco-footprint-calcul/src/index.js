#!/usr/bin/env node

// nightly-eco-footprint-calculator
// Estimate annual CO₂ emissions from simple activity inputs.

const args = process.argv.slice(2);

function printHelp() {
  console.log(`Usage: eco-footprint [options]
Options:
  --miles <number>        Miles driven by car (default 0)
  --kwh <number>          Electricity usage in kWh (default 0)
  --flight-hours <number> Flight hours (default 0)
  -h, --help              Show help`);
}

let miles = 0;
let kwh = 0;
let flightHours = 0;

for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === '-h' || a === '--help') {
    printHelp();
    process.exit(0);
  }
  if (a === '--miles') {
    miles = parseFloat(args[++i]) || 0;
  } else if (a === '--kwh') {
    kwh = parseFloat(args[++i]) || 0;
  } else if (a === '--flight-hours') {
    flightHours = parseFloat(args[++i]) || 0;
  }
}

const CO2_PER_MILE = 0.411; // kg CO₂ per mile
const CO2_PER_KWH = 0.475; // kg CO₂ per kWh
const CO2_PER_FLIGHT_HOUR = 90; // kg CO₂ per flight hour

const total = miles * CO2_PER_MILE + kwh * CO2_PER_KWH + flightHours * CO2_PER_FLIGHT_HOUR;

console.log(`Estimated annual CO₂ emissions: ${total.toFixed(2)} kg`);
