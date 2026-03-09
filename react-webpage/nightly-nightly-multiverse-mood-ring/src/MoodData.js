const moodDefinitions = [
  { keyword: "Hopeful", color: "#87CEEB", message: "A shimmering beacon in the temporal fog. Keep that light burning!" },
  { keyword: "Anxious", color: "#FFD700", message: "The cosmic currents are turbulent. Breathe, and brace for the next ripple." },
  { keyword: "Resilient", color: "#228B22", message: "Like bedrock against the void's erosion. Your strength echoes across dimensions." },
  { keyword: "Weary", color: "#8B4513", message: "Even temporal navigators need rest. Find your quiet corner of the continuum." },
  { keyword: "Curious", color: "#9370DB", message: "What strange new realities await? The multiverse rewards the inquisitive." },
  { keyword: "Determined", color: "#DC143C", message: "A focused will bends reality. Your path is clear, even through the chaos." },
  { keyword: "Neutral", color: "#808080", message: "Observing the cosmic dance. Sometimes, stillness is the greatest power." }
];

export const getMoodData = (moodKeyword) => {
  const normalizedKeyword = moodKeyword.toLowerCase();
  return moodDefinitions.find(m => m.keyword.toLowerCase() === normalizedKeyword) || {
    keyword: "Unclassified",
    color: "#000000",
    message: "The multiverse has yet to categorize this resonance. Intriguing!"
  };
};

export const getRandomCommunityMood = () => {
  const randomIndex = Math.floor(Math.random() * moodDefinitions.length);
  return moodDefinitions[randomIndex];
};
