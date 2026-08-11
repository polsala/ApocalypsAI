// src/api.js
const mockActivityData = [
  { id: '1', title: 'Fix: Critical bug in temporal anomaly detector', type: 'issue' },
  { id: '2', title: 'Feature: Add new whimsical emoji clock', type: 'pr' },
  { id: '3', title: 'Docs: Update README for new utility', type: 'pr' },
  { id: '4', title: 'Chore: Refactor agent_builder for clarity', type: 'pr' },
  { id: '5', title: 'Discussion: Brainstorming next-gen survival tools', type: 'discussion' },
  { id: '6', title: 'Enhancement: Improve performance of wasteland tracker', type: 'issue' },
  { id: '7', title: 'Bug: Minor UI glitch in time-ago-cli', type: 'issue' },
  { id: '8', title: 'Resolved: All known issues addressed', type: 'pr' },
  { id: '9', title: 'Urgent: Database connection failed', type: 'issue' }
];

export const fetchRepoActivity = () => {
  // # Mock rationale: To ensure deterministic and offline testing, and to simplify the utility
  // by avoiding actual GitHub API key management and rate limits for a purely UI-focused tool.
  // In a real-world scenario, this would fetch data from GitHub's API.
  return new Promise(resolve => {
    setTimeout(() => {
      resolve(mockActivityData);
    }, 500); // Simulate network delay
  });
};

// This function is for testing specific mood scenarios by allowing tests to inject different mock data.
export const setMockActivityData = (data) => {
  mockActivityData.splice(0, mockActivityData.length, ...data);
};
