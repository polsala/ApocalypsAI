export const getMockData = () => ({
  agentStatus: [
    { name: 'Agent Integrator', status: 'Active' },
    { name: 'Agent Builder', status: 'Idle' },
    { name: 'Agent Guardian', status: 'Active' },
    { name: 'Agent Reviewer', status: 'Maintenance' }
  ],
  utilityCounts: {
    'python-utils': 150,
    'rust-utils': 25,
    'bash-utils': 75,
    'react-webpage': 5,
    'github-actions': 10,
    'devops-tools': 30
  },
  workflowHealth: [
    { name: 'Nightly Self Heal', status: 'Healthy' },
    { name: 'Generator (OpenRouter)', status: 'Warning' },
    { name: 'Generator (Groq)', status: 'Healthy' },
    { name: 'PR Auto Review', status: 'Healthy' }
  ],
  resourceScarcity: 65 // Represents a medium level of scarcity
});
