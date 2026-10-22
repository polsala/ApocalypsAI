import chalk from 'chalk';

export type MoodType = 'Serene Sapphire' | 'Vibrant Verdant' | 'Golden Glow' | 'Amethyst Aura' | 'Crimson Ember' | 'Azure Abyss' | 'Obsidian Shadow' | 'Rainbow Shimmer';

export interface Mood {
  type: MoodType;
  color: chalk.Chalk;
  keywords: string[];
  insight: string;
}

export const moods: Mood[] = [
  {
    type: 'Serene Sapphire',
    color: chalk.hex('#007FFF'), // Deep Blue
    keywords: ['calm', 'peaceful', 'relaxed', 'tranquil', 'serene', 'still'],
    insight: 'The tranquil depths of the sapphire reflect the calm within your soul. Embrace this stillness, for it is a wellspring of strength.'
  },
  {
    type: 'Vibrant Verdant',
    color: chalk.hex('#228B22'), // Forest Green
    keywords: ['energetic', 'happy', 'joyful', 'excited', 'lively', 'enthusiastic', 'vibrant'],
    insight: 'Your spirit blossoms like a vibrant verdant forest! Let this energy guide your growth and spread joy to those around you.'
  },
  {
    type: 'Golden Glow',
    color: chalk.hex('#FFD700'), // Gold
    keywords: ['hopeful', 'optimistic', 'content', 'grateful', 'positive', 'bright'],
    insight: 'A golden glow surrounds you, signaling hope and contentment. Bask in this warmth and let its light illuminate your path forward.'
  },
  {
    type: 'Amethyst Aura',
    color: chalk.hex('#9966CC'), // Amethyst Purple
    keywords: ['thoughtful', 'introspective', 'curious', 'reflective', 'pensive', 'pondering'],
    insight: 'Your amethyst aura suggests deep thought and introspection. Dive into the mysteries of your mind; profound insights await.'
  },
  {
    type: 'Crimson Ember',
    color: chalk.hex('#DC143C'), // Crimson Red
    keywords: ['frustrated', 'angry', 'annoyed', 'irritated', 'furious', 'rage'],
    insight: 'A crimson ember burns within. Acknowledge this fire, but let it not consume you. Channel its intensity into constructive action.'
  },
  {
    type: 'Azure Abyss',
    color: chalk.hex('#4682B4'), // Steel Blue
    keywords: ['sad', 'melancholic', 'tired', 'down', 'gloomy', 'weary', 'depressed'],
    insight: 'The azure abyss holds a quiet sorrow. It is okay to feel this depth. Allow yourself rest, and remember that even the deepest waters eventually meet the shore.'
  },
  {
    type: 'Obsidian Shadow',
    color: chalk.hex('#2F4F4F'), // Dark Slate Gray
    keywords: ['anxious', 'worried', 'stressed', 'nervous', 'fearful', 'overwhelmed'],
    insight: 'An obsidian shadow looms, reflecting worries. Remember that shadows are cast by light. Seek the source of your strength and face the unknown with courage.'
  },
  {
    type: 'Rainbow Shimmer',
    color: chalk.hex('#8A2BE2'), // Blue Violet (as a base for 'shimmer')
    keywords: ['confused', 'mixed feelings', 'uncertain', 'perplexed', 'indecisive', 'complex'],
    insight: 'Your aura shimmers with a rainbow of emotions, a beautiful complexity. Embrace the spectrum of your feelings; clarity will emerge from the blend.'
  }
];

export function classifyMood(input: string): Mood {
  const lowerInput = input.toLowerCase();
  for (const mood of moods) {
    for (const keyword of mood.keywords) {
      if (lowerInput.includes(keyword)) {
        return mood;
      }
    }
  }
  // Default mood if no keywords match
  return {
    type: 'Rainbow Shimmer',
    color: chalk.hex('#8A2BE2'), // Blue Violet
    keywords: [], // No specific keywords for default
    insight: 'The Nightly Mood Ring detects a unique blend of energies. Your aura shimmers with a rainbow of emotions, a beautiful complexity. Embrace the spectrum of your feelings; clarity will emerge from the blend.'
  };
}
