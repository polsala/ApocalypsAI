import { CosmicFactor, AlignmentResult, AlignmentStatus } from './types';

const COSMIC_FACTORS_LIST = [
  { name: 'Lunar Phase', favorable: ['Waxing Gibbous, energies are building', 'Full Moon, peak potential', 'Waning Crescent, releasing old patterns'], unfavorable: ['New Moon, hidden challenges', 'First Quarter, growing pains', 'Last Quarter, shedding burdens'] },
  { name: 'Stellar Drift', favorable: ['Towards innovation', 'Stable orbit', 'Accelerating progress'], unfavorable: ['Erratic path', 'Retrograde motion', 'Unforeseen detours'] },
  { name: 'Nebula Bloom', favorable: ['A burst of creative energy', 'Vibrant hues, new beginnings', 'Expanding possibilities'], unfavorable: ['Fading light, diminishing returns', 'Dormant state, stagnant ideas', 'Contracting potential'] },
  { name: 'Quantum Entanglement', favorable: ['Harmonious connections', 'Synchronized flow, perfect timing', 'Interconnected success'], unfavorable: ['Too many entangled particles, proceed with caution', 'Chaotic fluctuations, unpredictable outcomes', 'Misaligned frequencies'] },
  { name: 'Solar Flare Activity', favorable: ['Igniting new ideas', 'Energetic bursts, rapid growth', 'Illuminating insights'], unfavorable: ['Disruptive pulses, communication blackout', 'Overheating systems', 'Blinding glare'] },
  { name: 'Galactic Hum', favorable: ['Resonant frequencies, clear signals', 'Soothing vibrations, calm environment', 'Harmonic convergence'], unfavorable: ['Discordant tones, internal conflict', 'Silent void, lack of inspiration', 'Static interference'] },
  { name: 'Asteroid Belt Stability', favorable: ['Clear path, smooth traversal', 'Well-charted course', 'Minimal debris'], unfavorable: ['Collision course, imminent obstacles', 'Turbulent zone, unexpected challenges', 'Unstable trajectory'] }
];

function getRandomElement<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

function generateCosmicFactor(): CosmicFactor {
  const factorTemplate = getRandomElement(COSMIC_FACTORS_LIST);
  const isFavorable = Math.random() > 0.5; // # Mock rationale: This random choice determines the factor's status (favorable or unfavorable).
  const status: AlignmentStatus = isFavorable ? 'Favorable' : 'Unfavorable';
  const description = isFavorable
    ? getRandomElement(factorTemplate.favorable)
    : getRandomElement(factorTemplate.unfavorable);

  return {
    name: factorTemplate.name,
    status,
    description: `${description}${isFavorable ? '!' : '.'}`,
  };
}

export function checkCosmicAlignment(): AlignmentResult {
  const factors: CosmicFactor[] = [];
  let favorableCount = 0;
  let unfavorableCount = 0;

  for (let i = 0; i < 4; i++) { // Check 4 random factors to allow for a 'Neutral' overall status
    const factor = generateCosmicFactor();
    factors.push(factor);
    if (factor.status === 'Favorable') {
      favorableCount++;
    } else if (factor.status === 'Unfavorable') {
      unfavorableCount++;
    }
  }

  let overallStatus: AlignmentStatus = 'Neutral';
  let message: string = 'The cosmos is undecided. Proceed with caution and a backup plan.';

  if (favorableCount > unfavorableCount) {
    overallStatus = 'Favorable';
    message = 'The cosmos smiles upon your endeavors! Proceed with confidence.';
  } else if (unfavorableCount > favorableCount) {
    overallStatus = 'Unfavorable';
    message = 'The cosmic currents are turbulent. Consider a different approach or a delay.';
  }

  return {
    overallStatus,
    factors,
    message,
  };
}

function formatResult(result: AlignmentResult): string {
  let output = '🌌 Checking Cosmic Alignment... 🌌\n\n';
  output += `✨ Overall Cosmic Alignment: ${result.overallStatus} ✨\n`;
  output += '---------------------------------------\n';
  result.factors.forEach(factor => {
    output += `- ${factor.name}: ${factor.status} (${factor.description})\n`;
  });
  output += `\nRecommendation: ${result.message}\n`;
  return output;
}

if (require.main === module) {
  const result = checkCosmicAlignment();
  console.log(formatResult(result));
}
