const tasks = {
  'low-energy': [
    "Stare at a wall and contemplate the void.",
    "Organize your collection of bottle caps by color.",
    "Hum a forgotten tune until it feels new again.",
    "Attempt to communicate with a houseplant using interpretive dance.",
    "Polish a single, ordinary rock until it gleams with existential dread."
  ],
  'medium-focus': [
    "Debug that strange flickering light in Sector 7.",
    "Sharpen all your dull pencils with extreme prejudice.",
    "Draft a strongly worded letter to the squirrels about property rights.",
    "Map out the optimal foraging path for imaginary space-hamsters.",
    "Categorize all the dust bunnies under your bed by age and origin."
  ],
  'high-chaos': [
    "Invent a new dance move inspired by a startled cockroach.",
    "Attempt to teach a raven advanced calculus.",
    "Build a small, non-threatening monument to a forgotten potato.",
    "Re-enact a dramatic scene from a silent film using only spoons.",
    "Organize a philosophical debate between two inanimate objects."
  ],
  'creative-spark': [
    "Compose a haiku about a rusty spoon.",
    "Sketch the emotional journey of a single dust bunny.",
    "Write a short story from the perspective of a sentient sock.",
    "Design a flag for a newly discovered, microscopic civilization.",
    "Choreograph a ballet for a colony of ants."
  ],
  'default': [
    "Ponder the migratory patterns of forgotten thoughts.",
    "Find the perfect spot for a nap that you'll never take.",
    "Consider the structural integrity of a cloud."
  ]
};

function getTaskSuggestion(mood = null) {
  const availableMoods = Object.keys(tasks).filter(m => m !== 'default');
  let selectedMood = mood;

  if (!selectedMood || !availableMoods.includes(selectedMood)) {
    // If no mood provided or invalid, pick a random one from available or use default
    const randomIndex = Math.floor(Math.random() * availableMoods.length);
    selectedMood = availableMoods[randomIndex];
    if (!selectedMood) { // Fallback if availableMoods is empty for some reason
      selectedMood = 'default';
    }
  }

  const moodTasks = tasks[selectedMood] || tasks['default'];
  const taskIndex = Math.floor(Math.random() * moodTasks.length);
  return {
    mood: selectedMood,
    task: moodTasks[taskIndex]
  };
}

module.exports = { getTaskSuggestion, tasks };
