const themes = {
  ruins: [
    "In the skeletal remains of forgotten cities, where rust weeps silent tears, the echoes of a lost world whisper tales of grandeur and decay.",
    "Beneath crumbling arches and shattered skylines, the ghosts of progress linger, silent witnesses to humanity's fall.",
    "The concrete giants, once symbols of power, now stand as hollow monuments to a civilization consumed by its own hubris.",
    "Dust motes dance in the shafts of light piercing broken roofs, illuminating the forgotten stories etched into decaying walls."
  ],
  mutants: [
    "Amongst the twisted flora and fauna, where life finds grotesque new forms, the irradiated earth births wonders and horrors alike.",
    "Whispers tell of creatures born of the glowing wastes, their forms grotesque, their minds a fractured mirror of what once was.",
    "Evolution, accelerated by the cataclysm, has sculpted new predators and prey, each a testament to the wasteland's brutal creativity.",
    "Beware the shadows that move with unnatural grace; they are the wasteland's children, and their hunger knows no bounds."
  ],
  hope: [
    "Even in the deepest desolation, a flicker of green persists, a stubborn sprout pushing through cracked pavement, promising renewal.",
    "A faint signal, a distant campfire, a shared smile \u2014 these are the fragile threads that weave the tapestry of tomorrow.",
    "Against the backdrop of endless grey, the human spirit, resilient and defiant, seeks to rebuild, to dream, to hope once more.",
    "The old world may be gone, but in the eyes of the young, a new dawn is always possible, a chance to forge a better path."
  ],
  despair: [
    "The silence of the wastes is a heavy shroud, muffling cries for help, echoing only the gnawing emptiness within.",
    "Every sunrise brings not warmth, but the chilling reminder of what was lost, and the crushing weight of what remains.",
    "Hope is a dangerous illusion in these lands, a cruel trick played by the dying sun on those too weary to fight.",
    "The dust covers everything \u2014 memories, dreams, and the last vestiges of a world that simply gave up."
  ],
  technology: [
    "Scattered relics of advanced machinery lie dormant, their complex circuits now home to insects, their purpose a forgotten mystery.",
    "The hum of ancient generators, if one can find them, is a symphony of power, a fleeting glimpse into a past of abundant energy.",
    "Data fragments, corrupted and fragmented, hint at vast networks and knowledge, now just digital ghosts in a dead world.",
    "A working device, no matter how simple, is a treasure beyond measure, a whisper of the ingenuity that once defined us."
  ],
  nature: [
    "The wild has reclaimed its dominion, vines strangling skyscrapers, forests growing where cities once stood, a silent, green revenge.",
    "Beneath the irradiated skies, new ecosystems emerge, beautiful in their savagery, indifferent to the fate of mankind.",
    "The rivers run with strange colors, the air carries unfamiliar scents, and the very ground pulses with an alien vitality.",
    "From the ashes, life finds a way, not as we knew it, but as a testament to the planet's enduring, untamed spirit."
  ]
};

function getRandomElement(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function generateLore(theme = null, count = 1) {
  const availableThemes = Object.keys(themes);
  const selectedTheme = theme && availableThemes.includes(theme) ? theme : getRandomElement(availableThemes);

  if (!selectedTheme || themes[selectedTheme].length === 0) {
    return "No lore themes available.";
  }

  const loreSnippets = [];
  for (let i = 0; i < count; i++) {
    loreSnippets.push(getRandomElement(themes[selectedTheme]));
  }
  return loreSnippets.join('\n\n');
}

// CLI Logic
if (require.main === module) {
  const args = process.argv.slice(2);
  let themeArg = null;
  let countArg = 1;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--theme' && args[i + 1]) {
      themeArg = args[i + 1];
      i++;
    } else if (args[i] === '--count' && args[i + 1]) {
      countArg = parseInt(args[i + 1], 10);
      if (isNaN(countArg) || countArg < 1) {
        console.error("Error: --count must be a positive integer.");
        process.exit(1);
      }
      i++;
    }
  }

  console.log(generateLore(themeArg, countArg));
}

module.exports = { generateLore, themes };
