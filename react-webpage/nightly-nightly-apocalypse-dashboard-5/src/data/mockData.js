export const getMockData = () => {
  const agents = [
    'nightly-shelter-sentry-log',
    'nightly-silly-commit-message-generat',
    'nightly-wasteland-resource-tracker',
    'nightly-temporal-anomaly-detector',
    'nightly-whimsical-emoji-clock'
  ];

  const actions = [
    'monitoring logs',
    'generating commit messages',
    'scavenging resources',
    'detecting anomalies',
    'keeping time',
    'writing poetry',
    'brewing coffee'
  ];

  const classifiers = [
    'python-utils',
    'rust-utils',
    'bash-utils',
    'react-webpage',
    'github-actions',
    'cli-apps',
    'data-scripts'
  ];

  const mockAgentActivity = Array.from({ length: 5 }, (_, i) => ({
    agent: agents[Math.floor(Math.random() * agents.length)],
    action: actions[Math.floor(Math.random() * actions.length)]
  }));

  const mockUtilityStats = {};
  classifiers.forEach(classifier => {
    mockUtilityStats[classifier] = Math.floor(Math.random() * 50);
  });

  return {
    agentActivity: mockAgentActivity,
    utilityStats: mockUtilityStats
  };
};
