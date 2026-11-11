// Mock rationale: Provides deterministic, offline data for the dashboard without requiring external API calls.
// This ensures tests are self-contained and repeatable.
const generateMockData = (days) => {
  const data = [];
  const today = new Date();
  const agentNames = ['Agent Integrator', 'Agent Builder', 'Agent Reviewer', 'Agent Guardian', 'Agent Empathy'];

  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(today.getDate() - i);
    const formattedDate = date.toISOString().split('T')[0]; // YYYY-MM-DD

    const dailyAgentActivity = agentNames.map(agent => ({
      agent: agent,
      count: Math.floor(Math.random() * 10) // Each agent contributes 0-9 activities
    }));

    data.push({
      date: formattedDate,
      stars: Math.floor(Math.random() * 50) + 10, // 10-59 stars
      commits: Math.floor(Math.random() * 100) + 20, // 20-119 commits
      issues: Math.floor(Math.random() * 30) + 5, // 5-34 issues
      agentActivity: dailyAgentActivity,
    });
  }
  return data;
};

export const mockDailyDust = generateMockData(30); // Generate 30 days of data
