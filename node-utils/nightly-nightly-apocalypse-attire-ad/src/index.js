const { attireRules, weatherConditions, moods } = require('./data');

function getRandomElement(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function getAttireSuggestion(weather, mood) {
  if (!weather || !mood) {
    return "Please provide both a weather condition and a mood, or let me choose for you!";
  }

  const normalizedWeather = weatherConditions.find(w => w.toLowerCase() === weather.toLowerCase());
  const normalizedMood = moods.find(m => m.toLowerCase() === mood.toLowerCase());

  if (!normalizedWeather) {
    return `Unknown weather condition: "${weather}". Available: ${weatherConditions.join(', ')}.`;
  }
  if (!normalizedMood) {
    return `Unknown mood/occasion: "${mood}". Available: ${moods.join(', ')}.`;
  }

  return attireRules[normalizedWeather][normalizedMood];
}

function runCli() {
  const args = process.argv.slice(2);
  let weatherArg = args[0];
  let moodArg = args[1];

  if (args.includes('--help') || args.includes('-h')) {
    console.log(`\nApocalypse Attire Advisor\n\nUsage:\n  node src/index.js [weather] [mood]\n  node src/index.js --random\n  node src/index.js --list\n\nOptions:\n  --random      Get a random attire suggestion.\n  --list        List all available weather conditions and moods.\n  -h, --help    Show this help message.\n\nExamples:\n  node src/index.js "Acid Rain" "Scavenging"\n  node src/index.js --random\n  node src/index.js "Irradiated Haze"\n    (If mood is omitted, a random mood will be chosen for the given weather)\n    `);
    return;
  }

  if (args.includes('--list')) {
    console.log("Available Weather Conditions:");
    weatherConditions.forEach(w => console.log(`- ${w}`));
    console.log("\nAvailable Moods/Occasions:");
    moods.forEach(m => console.log(`- ${m}`));
    return;
  }

  if (args.includes('--random')) {
    weatherArg = getRandomElement(weatherConditions);
    moodArg = getRandomElement(moods);
    console.log(`Randomly selected: Weather "${weatherArg}", Mood "${moodArg}"`);
  } else {
    if (!weatherArg) {
      console.log("No weather provided. Choosing a random one.");
      weatherArg = getRandomElement(weatherConditions);
    }
    if (!moodArg) {
      console.log("No mood provided. Choosing a random one.");
      moodArg = getRandomElement(moods);
    }
  }

  const suggestion = getAttireSuggestion(weatherArg, moodArg);
  console.log(`\nFor "${weatherArg}" and "${moodArg}", you should wear:\n"${suggestion}"`);
}

// Only run CLI if executed directly
if (require.main === module) {
  runCli();
}

module.exports = {
  getAttireSuggestion,
  getRandomElement, // Export for testing purposes
  weatherConditions,
  moods
};
