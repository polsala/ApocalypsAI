export const generateWhimsyForecast = () => {
  const weatherOptions = [
    "Dust Devil Dance", "Glow-worm Glimmer", "Scrap Shower",
    "Whispering Winds", "Sun-scorched Stillness", "Rad-rain Drizzle"
  ];
  const resourceOptions = [
    "Scrap Scarcity", "Water Wellspring", "Mutant Mushroom Bloom",
    "Tech Cache Found", "Fuel Fumes Fading", "Berry Bush Bounty"
  ];
  const moodOptions = [
    "Hopeful Hum", "Grumpy Growl", "Curious Chirp",
    "Anxious Aura", "Serene Silence", "Chaotic Cackle"
  ];

  const getRandomElement = (arr) => arr[Math.floor(Math.random() * arr.length)];

  return {
    weather: getRandomElement(weatherOptions),
    resources: getRandomElement(resourceOptions),
    mood: getRandomElement(moodOptions),
    timestamp: new Date().toLocaleTimeString()
  };
};
