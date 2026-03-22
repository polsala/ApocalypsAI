import { calibrateTask } from './chronoCalibrator';
import { TemporalChunk } from './types';

function displayCalibration(taskName: string, totalMinutes: number, chunks: TemporalChunk[]): void {
  console.log(`\n🌌 Chrono-Compass Calibration for: ${taskName} (${totalMinutes} minutes) 🌌\n`);

  chunks.forEach(chunk => {
    let icon = '';
    switch (chunk.type) {
      case 'work':
        icon = '🚀';
        break;
      case 'short-break':
        icon = '✨';
        break;
      case 'long-break':
        icon = '🧘';
        break;
    }
    console.log(`-   [${String(chunk.durationMinutes).padStart(2, ' ')} min] ${icon} ${chunk.name}: ${chunk.description}`);
  });
  console.log('\n');
}

function main(): void {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.error('Usage: npm start <task_name> <total_minutes>');
    console.error('Example: npm start "Write ApocalypsAI Report" 60');
    process.exit(1);
  }

  const taskName = args[0];
  const totalMinutes = parseInt(args[1], 10);

  if (isNaN(totalMinutes) || totalMinutes <= 0) {
    console.error('Error: <total_minutes> must be a positive number.');
    process.exit(1);
  }

  const calibratedChunks = calibrateTask(taskName, totalMinutes);
  displayCalibration(taskName, totalMinutes, calibratedChunks);
}

// Ensure main is called only when the script is executed directly
if (require.main === module) {
  main();
}
