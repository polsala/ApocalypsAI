import { CosmicGuidance, CosmicFocus } from './types';
import { createSeededRandom, formatDate, generateSeedFromDate } from './utils';

// --- Data for Cosmic Guidance ---
const FOCUS_OPTIONS: CosmicFocus[] = [
  'Deep Dive',
  'Collaborative Current',
  'Reflective Ripple',
  'Chaotic Creativity',
  'Strategic Scavenge',
  'Harmonic Integration',
  'Void Exploration',
];

const MESSAGE_OPTIONS: string[] = [
  "The echoes of the past hold lessons for the future. Listen closely to the void's whispers.",
  "Connect with your fellow survivors. Strength in numbers, even in the desolation.",
  "Take a moment to observe the shifting sands. Inner peace can be found amidst the chaos.",
  "Embrace the unexpected. Innovation often sparks from the most unlikely anomalies.",
  "Prioritize your resources. Every scrap counts in the grand scheme of survival.",
  "Seek balance in the cosmic energies. Align your actions with the universal flow.",
  "Dare to peer into the unknown. Discoveries await beyond the familiar horizons.",
  "Even in the darkest void, a spark of hope can ignite. Nurture it.",
  "The universe is vast and indifferent. Find your own meaning within its expanse.",
  "Adaptability is your greatest tool. Flow like water, reshape like clay.",
  "Observe the patterns of the stars. They hold ancient wisdom, if you know how to read them.",
  "Your inner compass is true. Trust your instincts when the path is unclear.",
  "Acknowledge the impermanence of all things. Embrace change as the only constant.",
  "Find beauty in the decay. New life often springs from the remnants of the old.",
  "The silence of the cosmos can be a powerful teacher. Listen to its profound stillness."
];

const COLOR_PALETTE_OPTIONS: string[][] = [
  ['#2F4F4F', '#708090', '#B0C4DE', '#E6E6FA'], // Dark Slate Gray to Lavender
  ['#4A2C5E', '#8B4513', '#D2B48C', '#F5DEB3'], // Deep Purple to Pale Goldenrod
  ['#000000', '#36454F', '#707070', '#D3D3D3'], // Black to Light Gray (Void)
  ['#8B0000', '#FF4500', '#FFD700', '#ADFF2F'], // Dark Red to Green Yellow (Fiery)
  ['#006400', '#228B22', '#3CB371', '#90EE90'], // Dark Green to Light Green (Growth)
  ['#191970', '#4169E1', '#6495ED', '#ADD8E6'], // Midnight Blue to Light Blue (Deep Space)
  ['#800080', '#BA55D3', '#DA70D6', '#EE82EE'], // Purple to Violet (Mystic)
  ['#A52A2A', '#CD853F', '#F4A460', '#DEB887'], // Brown to Tan (Wasteland)
];

/**
 * Generates cosmic guidance for a given date.
 * @param date The date for which to generate guidance.
 * @returns A CosmicGuidance object.
 */
export function generateCosmicGuidance(date: Date): CosmicGuidance {
  const dateString = formatDate(date);
  const seed = generateSeedFromDate(dateString);
  const random = createSeededRandom(seed);

  const focusIndex = Math.floor(random() * FOCUS_OPTIONS.length);
  const messageIndex = Math.floor(random() * MESSAGE_OPTIONS.length);
  const paletteIndex = Math.floor(random() * COLOR_PALETTE_OPTIONS.length);

  return {
    date: dateString,
    focus: FOCUS_OPTIONS[focusIndex],
    message: MESSAGE_OPTIONS[messageIndex],
    colorPalette: COLOR_PALETTE_OPTIONS[paletteIndex],
  };
}

/**
 * Main function to run the CLI utility.
 */
function main() {
  let targetDate: Date;
  const dateArg = process.argv[2];

  if (dateArg) {
    const parsedDate = new Date(dateArg);
    if (isNaN(parsedDate.getTime())) {
      console.error("Error: Invalid date format. Please use YYYY-MM-DD.");
      process.exit(1);
    }
    targetDate = parsedDate;
  } else {
    targetDate = new Date();
  }

  const guidance = generateCosmicGuidance(targetDate);

  console.log(`\n🌌 Cosmic Guidance for ${guidance.date} 🌌\n`);
  console.log(`Focus: ${guidance.focus}`);
  console.log(`Message: "${guidance.message}"`);
  console.log(`Color Palette:`);
  guidance.colorPalette.forEach(color => {
    // A simple way to display colors, could be enhanced with actual color output if desired
    // For CLI, just showing hex code and a common name if available.
    const colorName = getColorName(color);
    console.log(`  - ${color} (${colorName})`);
  });
  console.log('');
}

// Simple helper to get a common name for some hex colors (for display purposes)
function getColorName(hex: string): string {
  const colorMap: { [key: string]: string } = {
    '#2F4F4F': 'Dark Slate Gray',
    '#708090': 'Slate Gray',
    '#B0C4DE': 'Light Steel Blue',
    '#E6E6FA': 'Lavender',
    '#4A2C5E': 'Deep Purple',
    '#8B4513': 'Saddle Brown',
    '#D2B48C': 'Tan',
    '#F5DEB3': 'Wheat',
    '#000000': 'Black',
    '#36454F': 'Charcoal',
    '#707070': 'Gray',
    '#D3D3D3': 'Light Gray',
    '#8B0000': 'Dark Red',
    '#FF4500': 'Orange Red',
    '#FFD700': 'Gold',
    '#ADFF2F': 'Green Yellow',
    '#006400': 'Dark Green',
    '#228B22': 'Forest Green',
    '#3CB371': 'Medium Sea Green',
    '#90EE90': 'Light Green',
    '#191970': 'Midnight Blue',
    '#4169E1': 'Royal Blue',
    '#6495ED': 'Cornflower Blue',
    '#ADD8E6': 'Light Blue',
    '#800080': 'Purple',
    '#BA55D3': 'Medium Orchid',
    '#DA70D6': 'Orchid',
    '#EE82EE': 'Violet',
    '#A52A2A': 'Brown',
    '#CD853F': 'Peru',
    '#F4A460': 'Sandy Brown',
    '#DEB887': 'Burly Wood'
  };
  return colorMap[hex.toUpperCase()] || 'Unknown Color';
}


// Only run main if this file is executed directly
if (require.main === module) {
  main();
}
