#!/usr/bin/env node
// Nightly Apocalypse Color Namer
// Usage: node src/index.js <hexColor>
// Example: node src/index.js #ff5733

function hexToHsl(hex) {
  // Remove leading #
  hex = hex.replace(/^#/, '');
  if (hex.length === 3) {
    hex = hex.split('').map(c => c + c).join('');
  }
  const num = parseInt(hex, 16);
  const r = (num >> 16) & 255;
  const g = (num >> 8) & 255;
  const b = num & 255;
  const rNorm = r / 255;
  const gNorm = g / 255;
  const bNorm = b / 255;
  const max = Math.max(rNorm, gNorm, bNorm);
  const min = Math.min(rNorm, gNorm, bNorm);
  let h, s, l = (max + min) / 2;

  if (max === min) {
    h = s = 0; // achromatic
  } else {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case rNorm:
        h = (gNorm - bNorm) / d + (gNorm < bNorm ? 6 : 0);
        break;
      case gNorm:
        h = (bNorm - rNorm) / d + 2;
        break;
      case bNorm:
        h = (rNorm - gNorm) / d + 4;
        break;
    }
    h *= 60;
  }
  return { h, s, l };
}

function getAdjective(hue) {
  const adjectives = [
    { range: [0, 30], word: 'Scorched' },
    { range: [30, 90], word: 'Blazing' },
    { range: [90, 150], word: 'Radiant' },
    { range: [150, 210], word: 'Murked' },
    { range: [210, 270], word: 'Frozen' },
    { range: [270, 330], word: 'Eerie' },
    { range: [330, 360], word: 'Ashen' }
  ];
  for (const entry of adjectives) {
    if (hue >= entry.range[0] && hue < entry.range[1]) {
      return entry.word;
    }
  }
  return 'Mystic';
}

function getNoun(lightness, saturation) {
  // Mock rationale: prioritize low saturation (gray) as "Ash"
  if (saturation < 0.1) return 'Ash';
  if (lightness < 0.3) return 'Obsidian';
  if (lightness < 0.5) return 'Ash';
  if (lightness < 0.7) return 'Ember';
  if (saturation > 0.6) return 'Flame';
  return 'Glow';
}

function nameColor(hex) {
  const { h, s, l } = hexToHsl(hex);
  const adj = getAdjective(h);
  const noun = getNoun(l, s);
  return `${adj} ${noun}`;
}

// CLI handling
if (require.main === module) {
  const input = process.argv[2];
  if (!input) {
    console.error('Usage: node src/index.js <hexColor>');
    process.exit(1);
  }
  console.log(nameColor(input));
}

// Export for testing
module.exports = { hexToHsl, getAdjective, getNoun, nameColor };
