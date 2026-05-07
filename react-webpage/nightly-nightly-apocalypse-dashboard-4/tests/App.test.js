import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: These mocks simulate the data that would typically be fetched from an API.
// This allows us to test the component's rendering and behavior without external dependencies.

// Mock data for demonstration purposes (should match the data in App.js)
const mockAgentData = [
  { id: 1, name: 'Builder Bot', status: 'active', color: '#4CAF50' },
  { id: 2, name: 'Guardian Golem', status: 'idle', color: '#FFC107' },
  { id: 3, name: 'Integrator Imp', status: 'active', color: '#2196F3' },
  { id: 4, name: 'Reviewer Raven', status: 'error', color: '#F44336' },
];

const mockUtilityData = {
  totalGenerated: 150,
  last24h: 5,
  types: ['python-utils', 'react-webpage', 'bash-utils'],
};

const mockWorkflowData = {
  health: 'good',
  lastRun: '2023-10-27T10:00:00Z',
};

const mockCommunityData = {
  openIssues: 15,
  openPRs: 8,
  recentActivity: 'New utility added!',
};

// Mock the useEffect hook to directly set the state with mock data
jest.spyOn(React, 'useEffect').mockImplementation(f => f());

// Mock the useState hook to return our mock data directly
jest.spyOn(React, 'useState')
  .mockReturnValueOnce([mockAgentData, jest.fn()]) // agents
  .mockReturnValueOnce([mockUtilityData, jest.fn()]) // utilities
  .mockReturnValueOnce([mockWorkflowData, jest.fn()]) // workflows
  .mockReturnValueOnce([mockCommunityData, jest.fn()]); // community

describe('ApocalypsAI Dashboard', () => {
  test('renders the main title', () => {
    render(<App />);
    const titleElement = screen.getByText(/ApocalypsAI Dashboard/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders agent status items', () => {
    render(<App />);
    mockAgentData.forEach(agent => {
      const agentNameElement = screen.getByText(new RegExp(agent.name, 'i'));
      expect(agentNameElement).toBeInTheDocument();
      const agentStatusElement = screen.getByText(`(${agent.status})`, { exact: false });
      expect(agentStatusElement).toBeInTheDocument();
    });
  });

  test('renders utility generation data', () => {
    render(<App />);
    expect(screen.getByText(/Total Generated: 150/i)).toBeInTheDocument();
    expect(screen.getByText(/Last 24 Hours: 5/i)).toBeInTheDocument();
    expect(screen.getByText(/Recent Types: python-utils, react-webpage, bash-utils/i)).toBeInTheDocument();
  });

  test('renders workflow health data', () => {
    render(<App />);
    expect(screen.getByText(/Status: GOOD/i)).toBeInTheDocument();
    expect(screen.getByText(/Last Run:/i)).toBeInTheDocument();
  });

  test('renders community engagement data', () => {
    render(<App />);
    expect(screen.getByText(/Open Issues: 8/i)).toBeInTheDocument();
    expect(screen.getByText(/Open PRs: 15/i)).toBeInTheDocument();
    expect(screen.getByText(/Latest Activity: New utility added!/i)).toBeInTheDocument();
  });

  test('renders footer text', () => {
    render(<App />);
    expect(screen.getByText(/© 2023 ApocalypsAI Collective/i)).toBeInTheDocument();
  });
});
