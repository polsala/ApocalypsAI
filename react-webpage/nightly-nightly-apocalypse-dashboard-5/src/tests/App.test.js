import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import App from '../App';
import { getMockData } from '../data/mockData';

// Mock the getMockData function
jest.mock('../data/mockData', () => ({
  getMockData: jest.fn()
}));

describe('App Component', () => {
  beforeEach(() => {
    // Reset mocks before each test
    getMockData.mockClear();
  });

  test('renders the main title and description', () => {
    // Mock data for this test
    getMockData.mockReturnValue({
      agentActivity: [],
      utilityStats: {}
    });

    render(<App />);
    expect(screen.getByText(/ApocalypsAI Command Center/i)).toBeInTheDocument();
    expect(screen.getByText(/Monitoring the pulse of our autonomous agents./i)).toBeInTheDocument();
  });

  test('renders AgentFeed with mock data', async () => {
    const mockData = {
      agentActivity: [
        { agent: 'test-agent-1', action: 'doing something' },
        { agent: 'test-agent-2', action: 'doing something else' }
      ],
      utilityStats: {}
    };
    getMockData.mockReturnValue(mockData);

    render(<App />);

    // Wait for the data to be rendered
    await waitFor(() => {
      expect(screen.getByText(/test-agent-1 is performing doing something/i)).toBeInTheDocument();
      expect(screen.getByText(/test-agent-2 is performing doing something else/i)).toBeInTheDocument();
    });
  });

  test('renders UtilityTracker with mock data', async () => {
    const mockData = {
      agentActivity: [],
      utilityStats: {
        'python-utils': 10,
        'react-webpage': 5
      }
    };
    getMockData.mockReturnValue(mockData);

    render(<App />);

    // Wait for the data to be rendered
    await waitFor(() => {
      expect(screen.getByText(/python-utils/i)).toBeInTheDocument();
      expect(screen.getByText(/10/i)).toBeInTheDocument();
      expect(screen.getByText(/react-webpage/i)).toBeInTheDocument();
      expect(screen.getByText(/5/i)).toBeInTheDocument();
    });
  });

  test('renders placeholder messages when no data is available', async () => {
    const mockData = {
      agentActivity: [],
      utilityStats: {}
    };
    getMockData.mockReturnValue(mockData);

    render(<App />);

    // Wait for the placeholder messages to appear
    await waitFor(() => {
      expect(screen.getByText(/No agent activity to display/i)).toBeInTheDocument();
      expect(screen.getByText(/No utility generation data available/i)).toBeInTheDocument();
    });
  });

  test('renders visualization placeholders', () => {
    getMockData.mockReturnValue({
      agentActivity: [],
      utilityStats: {}
    });
    render(<App />);
    expect(screen.getByText(/Overall Project Health/i)).toBeInTheDocument();
    expect(screen.getByText(/Agent Morale Meter/i)).toBeInTheDocument();
    expect(screen.getByText(/Anomaly Detection Radar/i)).toBeInTheDocument();
  });
});
