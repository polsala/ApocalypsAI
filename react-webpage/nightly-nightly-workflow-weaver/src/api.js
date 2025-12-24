const WORKFLOW_NAMES = [
  'gen_openrouter.yml',
  'gen_groq.yml',
  'gen_gemini.yml',
  'nightly_self_heal.yml',
  'pr_auto_review.yml',
  'pr_review.yml',
  'test_and_eval.yml',
  'agent_pr_path_check.yml'
];

const MOOD_EMOJIS = [
  { emoji: '✨', description: 'Joyful' },
  { emoji: '☁️', description: 'Pensive' },
  { emoji: '⚡', description: 'Energetic' },
  { emoji: '🔥', description: 'Fiery' },
  { emoji: '💧', description: 'Calm' },
  { emoji: '🔮', description: 'Mysterious' },
  { emoji: '🌀', description: 'Whirling' }
];

const getRandomStatus = () => {
  const statuses = ['success', 'failure', 'running', 'unknown'];
  return statuses[Math.floor(Math.random() * statuses.length)];
};

const getRandomMood = () => {
  return MOOD_EMOJIS[Math.floor(Math.random() * MOOD_EMOJIS.length)];
};

const generateMockWorkflows = () => {
  return WORKFLOW_NAMES.map(name => ({
    id: name,
    name: name.replace('.yml', '').replace(/_/g, ' ').replace('gen', 'Generator').replace('nightly', 'Nightly').replace('pr', 'PR').replace('test', 'Test').replace('agent', 'Agent'),
    status: getRandomStatus(),
    lastRun: new Date(Date.now() - Math.random() * 86400000).toLocaleString(), // Last 24 hours
    mood: getRandomMood()
  }));
};

export const fetchWorkflows = () => {
  // # Mock rationale: Simulates an asynchronous API call to fetch workflow data.
  // This ensures deterministic and offline testing without requiring a real backend.
  return new Promise(resolve => {
    setTimeout(() => {
      if (Math.random() < 0.1) { // Simulate occasional API failure
        resolve({ success: false, error: 'Failed to fetch cosmic threads.' });
      } else {
        resolve({ success: true, data: generateMockWorkflows() });
      }
    }, 500 + Math.random() * 1000); // Simulate network latency
  });
};
