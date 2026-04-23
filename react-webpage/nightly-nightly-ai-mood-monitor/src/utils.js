let moodIndex = 0;

const moods = [
  { color: '#61dafb', description: 'Serene Blue: Calm, efficient operations.' },
  { color: '#4CAF50', description: 'Vibrant Green: Productive, growing integrations.' },
  { color: '#FF5722', description: 'Fiery Red: Intense activity, focused on critical tasks.' },
  { color: '#9C27B0', description: 'Mystic Purple: Deep thought, complex problem-solving.' },
  { color: '#FFC107', description: 'Golden Yellow: Optimistic, successful deployments imminent.' },
  { color: '#795548', description: 'Earthy Brown: Grounded, performing routine maintenance.' },
  { color: '#E91E63', description: 'Rose Pink: Harmonious collaboration, fostering community.' }
];

export const generateMood = () => {
  const currentMood = moods[moodIndex];
  moodIndex = (moodIndex + 1) % moods.length;
  return currentMood;
};

// For testing purposes, allow resetting the mood index
export const resetMoodIndex = () => {
  moodIndex = 0;
};
