#!/usr/bin/env node

const moods = {
  "resilient": {
    base: ["Sturdy scavenged boots", "Reinforced denim jacket", "Multi-tool belt"],
    accessories: ["Dust-proof goggles", "Weathered bandana"],
    description: "For facing the wastes head-on."
  },
  "mysterious": {
    base: ["Silent-tread sneakers", "Darkened, flowing cloak", "Utility harness with hidden pockets"],
    accessories: ["Visor that obscures identity", "Gloved hands"],
    description: "For those who prefer to observe from the shadows."
  },
  "optimistic": {
    base: ["Brightly patched overalls", "Comfortable walking sandals", "Upcycled backpack with solar charger"],
    accessories: ["Sun-faded wide-brim hat", "Gleaming salvaged trinkets"],
    description: "For finding joy amidst the desolation."
  },
  "daring": {
    base: ["Armored plating (lightweight)", "High-traction climbing boots", "Grappling hook holster"],
    accessories: ["Night-vision monocle", "Survival knife sheath"],
    description: "For adventurers seeking new horizons."
  },
  "calm": {
    base: ["Soft, breathable tunic", "Loose-fitting trousers", "Woven grass sandals"],
    accessories: ["Herbal pouch", "Meditative stone pendant"],
    description: "For finding inner peace in the chaos."
  }
};

const weatherConditions = {
  "ashfall": {
    modifiers: ["Respirator mask", "Full-coverage outer layer", "Wide-brimmed hat for dust"],
    warning: "Expect reduced visibility and fine particulate matter."
  },
  "irradiated drizzle": {
    modifiers: ["Waterproof outer shell (lead-lined if available)", "Geiger counter pouch", "Radiation-resistant hood"],
    warning: "Minimize skin exposure to the glowing droplets."
  },
  "solar flare advisory": {
    modifiers: ["UV-protective eyewear", "Light, breathable fabrics", "Shade-providing canopy or parasol"],
    warning: "Intense solar radiation expected. Stay hydrated."
  },
  "whispering winds": {
    modifiers: ["Thick scarf or cowl", "Layered garments for warmth", "Sound-dampening ear coverings"],
    warning: "The winds carry secrets... and a chill."
  },
  "clear skies": {
    modifiers: ["Light jacket (optional)", "Comfortable footwear"],
    warning: "A rare moment of peace. Enjoy the view."
  }
};

function generateOutfit(moodInput, weatherInput) {
  const normalizedMood = moodInput.toLowerCase();
  const normalizedWeather = weatherInput.toLowerCase();

  const selectedMood = moods[normalizedMood];
  const selectedWeather = weatherConditions[normalizedWeather];

  if (!selectedMood) {
    return `Unknown mood: "${moodInput}". Available moods: ${Object.keys(moods).join(", ")}.`;
  }
  if (!selectedWeather) {
    return `Unknown weather: "${weatherInput}". Available weather: ${Object.keys(weatherConditions).join(", ")}.`;
  }

  let outfit = `\n--- Nightly Mood-Matching Outfit Oracle ---\n`;
  outfit += `Desired Mood: ${moodInput.charAt(0).toUpperCase() + moodInput.slice(1)} (${selectedMood.description})\n`;
  outfit += `Simulated Weather: ${weatherInput.charAt(0).toUpperCase() + weatherInput.slice(1)} (${selectedWeather.warning})\n\n`;

  outfit += `Your recommended ensemble:\n`;
  selectedMood.base.forEach(item => outfit += `- ${item}\n`);
  selectedMood.accessories.forEach(item => outfit += `- ${item} (accessory)\n`);

  outfit += `\nWeather-specific adjustments:\n`;
  selectedWeather.modifiers.forEach(modifier => outfit += `- ${modifier}\n`);

  outfit += `\nStay safe and stylish in the wastes!\n`;
  return outfit;
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const moodArg = args[0];
  const weatherArg = args[1];

  if (!moodArg || !weatherArg) {
    console.error("Usage: nightly-mood-outfit-oracle <mood> <weather>");
    console.error(`Available moods: ${Object.keys(moods).join(", ")}`);
    console.error(`Available weather: ${Object.keys(weatherConditions).join(", ")}`);
    process.exit(1);
  }

  console.log(generateOutfit(moodArg, weatherArg));
}

module.exports = { generateOutfit, moods, weatherConditions };
