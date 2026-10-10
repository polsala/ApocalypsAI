import { Chore, ChoreCategory, CosmicInfluence, CosmicGuidance } from './types';

const ALL_CHORES: Chore[] = [
  { id: '1', description: 'Dust the cosmic shelves', category: 'Daily', effort: 'low' },
  { id: '2', description: 'Recharge the temporal crystals', category: 'Daily', effort: 'medium' },
  { id: '3', description: 'Sweep away astral dust bunnies', category: 'Daily', effort: 'low' },
  { id: '4', description: 'Polish the star-gazing lens', category: 'Weekly', effort: 'medium' },
  { id: '5', description: 'Organize the galaxy map fragments', category: 'Weekly', effort: 'high' },
  { id: '6', description: 'Fetch quantum fuel from the market', category: 'Errand', effort: 'medium' },
  { id: '7', description: 'Meditate on the void', category: 'Self-Care', effort: 'low' },
  { id: '8', description: 'Align your chakras with the constellations', category: 'Self-Care', effort: 'medium' },
  { id: '9', description: 'Repair the reality fabric tear in sector 7', category: 'Weekly', effort: 'high' },
  { id: '10', description: 'Water the space succulents', category: 'Daily', effort: 'low' },
  { id: '11', description: 'Calibrate the universal translator', category: 'Daily', effort: 'medium' },
  { id: '12', description: 'Archive ancient stellar charts', category: 'Weekly', effort: 'high' }
];

// Deterministic selection based on day of the month
function getCosmicInfluenceForDate(date: Date): CosmicInfluence {
  const day = date.getDate();
  const influences: CosmicInfluence[] = ['LunarLull', 'MartianMomentum', 'VenusianVibe', 'JovianJolt', 'SolarSurge'];
  return influences[day % influences.length];
}

export function generateCosmicChoreChart(date: Date = new Date()): CosmicGuidance {
  const influence = getCosmicInfluenceForDate(date);
  let message: string;
  let suggestedChores: Chore[];

  switch (influence) {
    case 'LunarLull':
      message = "The moon whispers secrets of gentle tidiness. Focus on quiet, reflective tasks.";
      suggestedChores = ALL_CHORES.filter(c => c.effort === 'low' || c.category === 'Self-Care');
      break;
    case 'MartianMomentum':
      message = "Mars ignites your drive! Tackle those high-energy, impactful chores.";
      suggestedChores = ALL_CHORES.filter(c => c.effort === 'high' || c.category === 'Errand');
      break;
    case 'VenusianVibe':
      message = "Venus brings harmony and beauty. Organize, beautify, and nurture your space.";
      suggestedChores = ALL_CHORES.filter(c => c.category === 'Weekly' || c.description.includes('polish') || c.description.includes('organize'));
      break;
    case 'JovianJolt':
      message = "Jupiter's expansive energy encourages grand gestures! Take on a big project.";
      suggestedChores = ALL_CHORES.filter(c => c.effort === 'high' || c.category === 'Weekly');
      break;
    case 'SolarSurge':
      message = "The sun energizes all! A balanced day for a mix of essential tasks.";
      suggestedChores = ALL_CHORES.filter(c => c.category === 'Daily' || c.effort === 'medium');
      break;
    default:
      // Fallback, though with current logic, this should not be reached
      message = "The cosmos is in a neutral state. Pick any chore that calls to you.";
      suggestedChores = ALL_CHORES.filter(c => c.effort === 'medium');
      break;
  }

  // Ensure unique chores and a reasonable number
  const uniqueChores = Array.from(new Set(suggestedChores.map(c => c.id)))
    .map(id => suggestedChores.find(c => c.id === id)!);
  
  // Limit to a manageable number, e.g., 3-5 chores
  const finalChores = uniqueChores.slice(0, Math.min(uniqueChores.length, 5));

  return {
    influence,
    message,
    suggestedChores: finalChores,
  };
}
