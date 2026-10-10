import { generateCosmicChoreChart } from './cosmicChoreGenerator';
import { CosmicGuidance } from './types';
import { format } from 'date-fns';

function run() {
  const today = new Date();
  const chart: CosmicGuidance = generateCosmicChoreChart(today);

  console.log(`\n--- Nightly Cosmic Chore Chart for ${format(today, 'PPP')} ---`);
  console.log(`Cosmic Influence: ${chart.influence}`);
  console.log(`Guidance: ${chart.message}`);
  console.log('\nYour Cosmic Tasks:');
  if (chart.suggestedChores.length === 0) {
    console.log('  No specific cosmic tasks today. Enjoy the void!');
  } else {
    chart.suggestedChores.forEach((chore, index) => {
      console.log(`  ${index + 1}. [${chore.category}] ${chore.description} (Effort: ${chore.effort})`);
    });
  }
  console.log('\nMay your efforts align with the stars!\n');
}

run();
