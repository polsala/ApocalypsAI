import { Mood, Quest } from './types';

const quests: Quest[] = [
  {
    mood: 'energetic',
    title: 'The Sparkle & Conquer Protocol',
    description: 'Initiate the "Sparkle & Conquer" Protocol: Tidy one small area, then reward yourself with a vigorous dance-off against imaginary foes.',
    actionableSteps: ['Choose a small area (e.g., a desk corner).', 'Tidy it for 10 minutes.', 'Put on your favorite pump-up song and dance!']
  },
  {
    mood: 'energetic',
    title: 'The Sprint of the Swift Squirrel',
    description: 'Undertake the Sprint of the Swift Squirrel: Complete three quick, pending tasks, then celebrate with a healthy, crunchy snack.',
    actionableSteps: ['Identify 3 tasks taking less than 5 minutes each.', 'Complete them.', 'Enjoy a handful of nuts or an apple.']
  },
  {
    mood: 'tired',
    title: 'The Great Pillow Expedition',
    description: 'Embark on the Great Pillow Expedition: Seek the softest cushion and claim it for a 15-minute power-nap ritual.',
    actionableSteps: ['Find your comfiest spot.', 'Set a 15-minute timer.', 'Rest your eyes and mind.']
  },
  {
    mood: 'tired',
    title: 'The Gentle Gaze of the Cloud Watcher',
    description: 'Engage in the Gentle Gaze of the Cloud Watcher: Find a window, observe the sky for 5 minutes, and let your thoughts drift like clouds.',
    actionableSteps: ['Locate a window with a view.', 'Gaze outside for 5 minutes.', 'Breathe deeply and relax.']
  },
  {
    mood: 'creative',
    title: 'The Idea Bloom Spell',
    description: 'Unleash the "Idea Bloom" Spell: Jot down three absurd concepts, then pick one to doodle or free-write about for 10 minutes.',
    actionableSteps: ['Grab a pen and paper (or open a doc).', 'Write down 3 wild ideas, no judgment.', 'Choose one and explore it for 10 minutes.']
  },
  {
    mood: 'creative',
    title: 'The Symphony of Found Sounds',
    description: 'Compose the Symphony of Found Sounds: Listen intently to your immediate environment for 3 minutes, identifying unique sounds. Can you mimic one?',
    actionableSteps: ['Close your eyes for 3 minutes.', 'Focus on ambient sounds.', 'Try to recreate one sound with your voice or hands.']
  },
  {
    mood: 'procrastinating',
    title: 'The Tiny Task Takedown',
    description: 'Undertake the "Tiny Task Takedown": Identify the smallest, most annoying chore and vanquish it within 5 minutes. The rewards are immense (and imaginary).',
    actionableSteps: ['Spot a task that takes < 5 minutes (e.g., emptying a cup).', 'Complete it immediately.', 'Feel the surge of accomplishment!']
  },
  {
    mood: 'procrastinating',
    title: 'The "Just One Thing" Ritual',
    description: 'Perform the "Just One Thing" Ritual: Pick one item on your to-do list, commit to working on it for exactly 10 minutes, then stop.',
    actionableSteps: ['Choose one task from your list.', 'Set a 10-minute timer.', 'Work on it, no distractions. Stop when the timer rings.']
  },
  {
    mood: 'neutral',
    title: 'The Path of the Curious Explorer',
    description: 'Embark on the Path of the Curious Explorer: Learn one new, random fact about anything that catches your eye online or in a book.',
    actionableSteps: ['Open a search engine or a book.', 'Find something you\'re mildly curious about.', 'Learn one new fact.']
  },
  {
    mood: 'neutral',
    title: 'The Breath of Stillness',
    description: 'Engage in the Breath of Stillness: Take 5 deep, slow breaths, focusing only on the sensation of air entering and leaving your body.',
    actionableSteps: ['Sit comfortably.', 'Inhale slowly for 4 counts.', 'Exhale slowly for 6 counts. Repeat 5 times.']
  },
  {
    mood: 'anxious',
    title: 'The Grounding Stone Meditation',
    description: 'Perform the Grounding Stone Meditation: Find an object near you, focus on its texture, weight, and temperature for a minute to anchor yourself.',
    actionableSteps: ['Pick up a small object (e.g., a pen, a rock).', 'Feel its texture, weight, temperature.', 'Focus on these sensations for 1 minute.']
  },
  {
    mood: 'anxious',
    title: 'The Worry Web Untangler',
    description: 'Initiate the Worry Web Untangler: Write down one specific worry, then brainstorm three tiny, immediate steps you could take to address it (even if just researching).',
    actionableSteps: ['Grab paper and pen.', 'Write down one specific worry.', 'List 3 tiny, actionable steps related to it.']
  },
  {
    mood: 'playful',
    title: 'The Silly Sound Scavenger Hunt',
    description: 'Embark on the Silly Sound Scavenger Hunt: Find three objects that make amusing noises when interacted with. Bonus points for a mini-concert!',
    actionableSteps: ['Look for objects that make interesting sounds.', 'Experiment with them.', 'Perform a short "silly sound" concert.']
  },
  {
    mood: 'playful',
    title: 'The Doodle Dragon Tamer',
    description: 'Become the Doodle Dragon Tamer: Draw a fantastical creature using only basic shapes (circles, squares, triangles). Give it a name!',
    actionableSteps: ['Grab paper and pen.', 'Draw a creature using only simple shapes.', 'Give your creature a whimsical name.']
  }
];

export function generateQuest(mood: Mood): Quest | undefined {
  const filteredQuests = quests.filter(q => q.mood === mood);
  if (filteredQuests.length === 0) {
    // Fallback to a neutral quest if no specific mood quests are found
    const neutralQuests = quests.filter(q => q.mood === 'neutral');
    if (neutralQuests.length === 0) return undefined; // Should not happen with current data
    return neutralQuests[Math.floor(Math.random() * neutralQuests.length)];
  }
  return filteredQuests[Math.floor(Math.random() * filteredQuests.length)];
}

export function getAllMoods(): Mood[] {
  const uniqueMoods = new Set<Mood>();
  quests.forEach(q => uniqueMoods.add(q.mood));
  return Array.from(uniqueMoods);
}
