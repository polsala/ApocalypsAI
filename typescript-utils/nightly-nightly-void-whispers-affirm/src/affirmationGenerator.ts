export interface AffirmationOptions {
  name?: string;
  mood?: string;
}

const templates = {
  hopeful: [
    "In the silence of the wasteland, {name}, your spirit burns brighter than any ember. The void whispers your name with reverence.",
    "Though the sun has dimmed, {name}, your inner light casts shadows that stretch to tomorrow. Hope is your compass.",
    "The ruins speak of endings, but {name}, your heartbeat writes new beginnings in the dust. The future listens."
  ],
  determined: [
    "The path ahead is treacherous, but {name}, your determination cuts through darkness like a blade through shadow.",
    "Each step you take reshapes the wasteland. {name}, your will is the hammer that forges tomorrow.",
    "The void tests all survivors, {name}, but your resolve is unyielding as the ancient mountains."
  ],
  cautious: [
    "In shadows you move, {name}, and the wasteland respects those who tread with care. Caution is your shield.",
    "The ruins hold secrets and dangers, {name}. Your watchful eye sees what others miss. Wisdom guides you.",
    "Every footprint tells a story, {name}. Yours speaks of careful planning and deliberate survival."
  ],
  fierce: [
    "The wasteland bows to your fury, {name}. Your strength reshapes the very landscape of tomorrow.",
    "Where others see death, {name}, you see opportunity. Your fierce spirit turns decay into rebirth.",
    "The void whispers warnings to those who would challenge you, {name}. Your name echoes in fear and respect."
  ],
  neutral: [
    "The silence between heartbeats holds infinite possibilities, {name}. In the void, you are both the question and the answer.",
    "Time flows differently in the wasteland, {name}. Your presence bends its currents toward your will.",
    "The echoes of the old world fade, but {name}, your story writes itself in the silence between the ruins."
  ]
};

const defaultNames = [
  "Survivor",
  "Wanderer",
  "Scavenger",
  "Guardian",
  "Reclaimer",
  "Wayfarer",
  "Sentinel",
  "Explorer",
  "Voyager",
  "Pioneer"
];

export function generateAffirmation(options: AffirmationOptions): string {
  const mood = options.mood || 'neutral';
  const name = options.name || defaultNames[Math.floor(Math.random() * defaultNames.length)];
  
  const moodTemplates = templates[mood as keyof typeof templates] || templates.neutral;
  const template = moodTemplates[Math.floor(Math.random() * moodTemplates.length)];
  
  return template.replace('{name}', name);
}
