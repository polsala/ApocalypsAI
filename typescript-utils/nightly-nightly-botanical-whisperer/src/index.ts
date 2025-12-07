import { Command } from 'commander';
import { PlantState, WhisperData, interpretWhispers, suggestAction } from './plantWhisperer';

const program = new Command();

program
  .name('botanical-whisperer')
  .description('Interpret simulated plant whispers and suggest care actions.')
  .version('1.0.0');

program
  .option('-m, --moisture <number>', 'Soil moisture level (0-100%)', parseFloat)
  .option('-l, --light <number>', 'Light intensity (0-100%)', parseFloat)
  .option('-t, --temperature <number>', 'Ambient temperature (Celsius)', parseFloat)
  .option('-v, --vibration <number>', 'Vibration frequency (Hz)', parseFloat)
  .action((options) => {
    let data: WhisperData;

    if (Object.keys(options).length === 0) {
      // Generate random data if no options provided
      console.log("No whisper data provided. Generating random plant whispers...");
      data = {
        moisture: Math.floor(Math.random() * 100),
        light: Math.floor(Math.random() * 100),
        temperature: Math.floor(Math.random() * (35 - 5 + 1)) + 5, // 5-35 C
        vibrationFrequency: Math.floor(Math.random() * 20), // 0-20 Hz
      };
    } else {
      // Validate and use provided data
      const { moisture, light, temperature, vibration } = options;
      if (
        typeof moisture !== 'number' || moisture < 0 || moisture > 100 ||
        typeof light !== 'number' || light < 0 || light > 100 ||
        typeof temperature !== 'number' || temperature < -10 || temperature > 50 || // Broader range for input
        typeof vibration !== 'number' || vibration < 0 || vibration > 100
      ) {
        console.error("Invalid input. Please ensure moisture, light, and vibration are 0-100, and temperature is a reasonable Celsius value.");
        process.exit(1);
      }
      data = {
        moisture: moisture,
        light: light,
        temperature: temperature,
        vibrationFrequency: vibration,
      };
    }

    console.log("\n--- Plant Whisper Analysis ---");
    console.log(`Moisture: ${data.moisture}%`);
    console.log(`Light: ${data.light}%`);
    console.log(`Temperature: ${data.temperature}°C`);
    console.log(`Vibration: ${data.vibrationFrequency} Hz`);

    const state = interpretWhispers(data);
    const action = suggestAction(state);

    console.log(`\nDetected State: ${state}`);
    console.log(`Suggested Action: ${action}`);
    console.log("-----------------------------\n");
  });

program.parse(process.argv);
