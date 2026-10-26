const MOOD_KEYWORDS = {
  'Temporal Flux': {
    keywords: ['temporal', 'time', 'rift', 'echo', 'drift', 'anomaly', 'stabiliz', 'tear'],
    color: '#4A90E2', // Blue
    description: 'The fabric of reality is bending. Expect temporal distortions and paradoxes.'
  },
  'Wasteland Wanderlust': {
    keywords: ['wasteland', 'survival', 'resource', 'scavenger', 'shelter', 'sentry', 'wayfinder', 'tracker'],
    color: '#7ED321', // Green
    description: 'Exploring the desolate expanses, seeking resources and new paths.'
  },
  'Whimsical Whimsy': {
    keywords: ['whimsical', 'silly', 'emoji', 'quote', 'affirmation', 'whispers', 'compliment', 'zen'],
    color: '#F5A623', // Orange/Yellow
    description: 'A lighthearted and playful spirit, bringing joy and amusement.'
  },
  'DevOps Drive': {
    keywords: ['ansible', 'docker', 'github', 'workflow', 'config', 'monitor', 'deploy', 'ci-cd', 'k8s', 'terraform', 'test-suite', 'infra'],
    color: '#BD10E0', // Purple
    description: 'Focused on automation, infrastructure, and keeping the systems running smoothly.'
  },
  'CLI Command': {
    keywords: ['cli', 'bash', 'go-utils', 'rust-utils', 'python-utils', 'tool', 'script', 'command'],
    color: '#50E3C2', // Teal
    description: 'A direct and efficient utility, designed for command-line interaction.'
  },
  'Data Deep Dive': {
    keywords: ['data', 'ml', 'database', 'analyze', 'script', 'report'],
    color: '#F8E71C', // Yellow
    description: 'Delving into data, extracting insights, or managing information stores.'
  },
  'Neutral Stability': {
    keywords: [], // Default if no strong keywords are found
    color: '#808080', // Grey
    description: 'A balanced and general-purpose utility, maintaining equilibrium.'
  }
};

export function analyzeUtility(utilityData) {
  let bestMood = 'Neutral Stability';
  let maxScore = 0;

  const textToAnalyze = [
    utilityData.util_name || '',
    utilityData.summary || '',
    utilityData.classifier || ''
  ];

  if (utilityData.files && Array.isArray(utilityData.files)) {
    utilityData.files.forEach(file => {
      if (file.content) {
        textToAnalyze.push(file.content);
      }
    });
  }

  const combinedText = textToAnalyze.join(' ').toLowerCase();

  for (const moodName in MOOD_KEYWORDS) {
    if (moodName === 'Neutral Stability') continue; // Handle default separately

    let currentScore = 0;
    MOOD_KEYWORDS[moodName].keywords.forEach(keyword => {
      const regex = new RegExp(`\\b${keyword}\\b`, 'g'); // Match whole words
      const matches = combinedText.match(regex);
      if (matches) {
        currentScore += matches.length;
      }
    });

    if (currentScore > maxScore) {
      maxScore = currentScore;
      bestMood = moodName;
    }
  }

  const finalMood = MOOD_KEYWORDS[bestMood];
  return {
    name: bestMood,
    color: finalMood.color,
    description: finalMood.description
  };
}
