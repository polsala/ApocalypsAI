// src/moodData.js

export const moods = [
  {
    "name": "Chaotic",
    "color": "#FF4500", // OrangeRed
    "icon": "🌀",
    "insight": "Embrace the swirl. Sometimes, the best plan is no plan at all. Just keep spinning!"
  },
  {
    "name": "Serene",
    "color": "#6A5ACD", // SlateBlue
    "icon": "🧘",
    "insight": "A moment of calm in the storm. Breathe. The void can wait a minute."
  },
  {
    "name": "Optimistic",
    "color": "#32CD32", // LimeGreen
    "icon": "✨",
    "insight": "The sun will rise again, probably. Or at least a new, interesting anomaly will appear!"
  },
  {
    "name": "Anxious",
    "color": "#FFD700", // Gold
    "icon": "⚡",
    "insight": "Feeling the static? Channel that energy into something productive, like fortifying your bunker."
  },
  {
    "name": "Melancholy",
    "color": "#4682B4", // SteelBlue
    "icon": "🌧️",
    "insight": "It's okay to feel the weight of the world. Just don't let it crush your spirit... or your supplies."
  },
  {
    "name": "Curious",
    "color": "#DA70D6", // Orchid
    "icon": "🔍",
    "insight": "What's around the next temporal corner? Go find out! (Safely, of course.)"
  },
  {
    "name": "Resilient",
    "color": "#8B0000", // DarkRed
    "icon": "💪",
    "insight": "You've faced worse. You'll face this too. The apocalypse builds character!"
  }
];

export const getRandomMood = () => {
  const randomIndex = Math.floor(Math.random() * moods.length);
  return moods[randomIndex];
};
