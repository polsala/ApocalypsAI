import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// Mock the CSS imports
jest.mock('../src/App.css', () => ({}));
jest.mock('../src/index.css', () => ({}));

// Mock data generator
const mockGenerateData = () => ({
  agents: [
    { name: 'Agent Builder', status: 'online', health: 95, lastSeen: new Date(Date.now() - 300000) },
    { name: 'Agent Guardian', status: 'offline', health: 0, lastSeen: new Date(Date.now() - 3600000) },
  ],
  metrics: {
    totalPRs: 150,
    openPRs: 7,
    mergedPRs: 45,
    failedPRs: 3,
    utilitiesCreated: 600,
    chaosExperiments: 15,
  },
  timeline: [
    {
      time: new Date(Date.now() - 3600000),
      title: 'Chaos Experiment: Network Latency',
      description: 'Injected 200ms latency across all services',
      status: 'success',
    },
  ],
  resources: {
    githubAPI: { usage: 150, limit: 5000 },
    diskSpace: { usage: 45, total: 100 },
    memoryUsage: { usage: 60, total: 100 },
    cpuLoad: { usage: 35, total: 100 },
  },
});

// Mock the fetchData function
const mockFetchData = jest.fn().mockImplementation(async () => {
  // Mock the API delay
  await new Promise(resolve => setTimeout(resolve, 100));
});

describe('App Component', () => {
  beforeEach(() => {
    // Mock console.error to avoid noise in tests
    jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('renders dashboard header', () => {
    render(<App />);
    expect(screen.getByText('ApocalypsAI Dashboard')).toBeInTheDocument();
  });

  test('renders loading state initially', () => {
    render(<App />);
    expect(screen.getByText(/Initializing ApocalypsAI Dashboard/i)).toBeInTheDocument();
    expect(screen.getByText(/Scanning repository for agent activity/i)).toBeInTheDocument();
  });

  test('renders agent health monitor after loading', async () => {
    render(<App />);
    
    // Wait for data to load
    await waitFor(() => {
      expect(screen.getByText('🤖 Agent Health Monitor')).toBeInTheDocument();
    }, { timeout: 5000 });
    
    // Check for agent names
    expect(screen.getByText('Agent Builder')).toBeInTheDocument();
    expect(screen.getByText('Agent Guardian')).toBeInTheDocument();
  });

  test('renders utility metrics after loading', async () => {
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('📊 Utility Metrics')).toBeInTheDocument();
    }, { timeout: 5000 });
    
    expect(screen.getByText(/Total Utilities Created/i)).toBeInTheDocument();
    expect(screen.getByText(/Chaos Experiments/i)).toBeInTheDocument();
    expect(screen.getByText(/Open PRs/i)).toBeInTheDocument();
  });

  test('renders resource tracker after loading', async () => {
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('💾 Resource Tracker')).toBeInTheDocument();
    }, { timeout: 5000 });
    
    expect(screen.getByText(/GitHub API Usage/i)).toBeInTheDocument();
    expect(screen.getByText(/Disk Space/i)).toBeInTheDocument();
    expect(screen.getByText(/Memory Usage/i)).toBeInTheDocument();
    expect(screen.getByText(/CPU Load/i)).toBeInTheDocument();
  });

  test('renders chaos event timeline after loading', async () => {
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('🔥 Chaos Event Timeline')).toBeInTheDocument();
    }, { timeout: 5000 });
    
    expect(screen.getByText(/Chaos Experiment: Network Latency/i)).toBeInTheDocument();
  });

  test('displays refresh controls', async () => {
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText(/Last Updated:/i)).toBeInTheDocument();
    }, { timeout: 5000 });
    
    expect(screen.getByText(/Auto-refresh:/i)).toBeInTheDocument();
    expect(screen.getByText(/Refresh Now/i)).toBeInTheDocument();
  });

  test('handles error state gracefully', async () => {
    // This test would require mocking a failed fetch
    // For now, we test that the component doesn't crash
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('ApocalypsAI Dashboard')).toBeInTheDocument();
    }, { timeout: 5000 });
  });

  test('displays footer information', async () => {
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText(/ApocalypsAI Dashboard v1.0.0/i)).toBeInTheDocument();
    }, { timeout: 5000 });
    
    expect(screen.getByText(/Built with React • Chart.js • CSS3 Animations/i)).toBeInTheDocument();
  });
});
