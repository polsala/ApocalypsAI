const prompts = require('prompts');
const chalk = require('chalk');

const moodMap = [
  { keywords: ['happy', 'joy', 'excited', 'energetic', 'good', 'great'], color: chalk.red, description: 'Radiant Ruby (Happy and energetic!)' },
  { keywords: ['calm', 'peace', 'relaxed', 'serene'], color: chalk.green, description: 'Serene Emerald (Feeling peaceful and calm.)' },
  { keywords: ['sad', 'down', 'blue', 'gloomy', 'unhappy'], color: chalk.blue, description: 'Melancholy Sapphire (Feeling a bit sad or reflective.)' },
  { keywords: ['angry', 'frustrated', 'irritated', 'annoyed'], color: chalk.hex('#FF4500'), description: 'Volatile Vermilion (Feeling agitated or frustrated.)' }, // OrangeRed
  { keywords: ['confused', 'uncertain', 'puzzled', 'unsure'], color: chalk.magenta, description: 'Mystic Amethyst (Feeling confused or uncertain.)' },
  { keywords: ['curious', 'interested', 'exploring'], color: chalk.yellow, description: 'Curious Citrine (Feeling inquisitive and engaged.)' },
  { keywords: ['anxious', 'nervous', 'stressed', 'worried'], color: chalk.hex('#8B0000'), description: 'Anxious Garnet (Feeling stressed or worried.)' }, // DarkRed
  { keywords: ['content', 'satisfied', 'pleased'], color: chalk.cyan, description: 'Content Aquamarine (Feeling satisfied and at ease.)' },
  { keywords: ['bored', 'dull', 'monotonous'], color: chalk.grey, description: 'Apathetic Ash (Feeling bored or uninspired.)' },
  { keywords: ['love', 'affection', 'caring'], color: chalk.hex('#FF69B4'), description: 'Loving Rose Quartz (Feeling affectionate and warm.)' } // HotPink
];

const defaultMood = { color: chalk.white, description: 'Shifting Quartz (Neutral, adaptable, or uncertain.)' };

async function getMood() {
  console.log(chalk.bold('✨ Nightly Mood Ring ✨'));

  const response = await prompts({
    type: 'text',
    name: 'feeling',
    message: 'Enter a phrase describing your current feeling:'
  });

  const inputPhrase = response.feeling ? response.feeling.toLowerCase() : '';
  const words = inputPhrase.split(/\s+/).filter(Boolean); // Split by whitespace and remove empty strings

  let detectedMood = defaultMood;

  for (const mood of moodMap) {
    if (mood.keywords.some(keyword => words.includes(keyword))) {
      detectedMood = mood;
      break; // Take the first matching mood for simplicity
    }
  }

  console.log(`Your mood is: ${detectedMood.color(detectedMood.description)}`);
}

if (require.main === module) {
  getMood();
}

module.exports = { getMood, moodMap, defaultMood }; // Export for testing
