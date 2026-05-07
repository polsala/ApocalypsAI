import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../src/App';
import { getMockData } from '../src/utils/mockData';

// Mock rationale: Using mock data to ensure deterministic and offline tests.
// The getMockData function provides consistent data for rendering and assertions.

jest.mock('../src/utils/mockData', () => ({
  getMockData: jest.fn()
}));

describe('App Component', () => {
  beforeEach(() => {
    // Reset mocks before each test
    getMockData.mockClear();
  });

  test('renders dashboard title', () => {
    getMockData.mockReturnValue({
      agentStatus: [],
      utilityCounts: {},
      workflowHealth: [],
      resourceScarcity: 0
    });
    render(<App />);
    expect(screen.getByText(/ApocalypsAI Dashboard/i)).toBeInTheDocument();
  });

  test('renders agent status section with mock data', () => {
    const mockData = getMockData();
    mockData.agentStatus = [
      { name: 'Mock Agent 1', status: 'Active' },
      { name: 'Mock Agent 2', status: 'Idle' }
    ];
    getMockData.mockReturnValue(mockData);

    render(<App />);
    expect(screen.getByText(/Agent Status/i)).toBeInTheDocument();
    expect(screen.getByText(/Mock Agent 1/i)).toBeInTheDocument();
    expect(screen.getByText(/Active/i)).toBeInTheDocument();
    expect(screen.getByText(/Mock Agent 2/i)).toBeInTheDocument();
    expect(screen.getByText(/Idle/i)).toBeInTheDocument();
  });

  test('renders utility counter section with mock data', () => {
    const mockData = getMockData();
    mockData.utilityCounts = {
      'python-utils': 10,
      'rust-utils': 5
    };
    getMockData.mockReturnValue(mockData);

    render(<App />);
    expect(screen.getByText(/Utility Counts/i)).toBeInTheDocument();
    expect(screen.getByText(/python-utils: 10/i)).toBeInTheDocument();
    expect(screen.getByText(/rust-utils: 5/i)).toBeInTheDocument();
  });

  test('renders workflow health section with mock data', () => {
    const mockData = getMockData();
    mockData.workflowHealth = [
      { name: 'Test Workflow', status: 'Healthy' }
    ];
    getMockData.mockReturnValue(mockData);

    render(<App />);
    expect(screen.getByText(/Workflow Health/i)).toBeInTheDocument();
    expect(screen.getByText(/Test Workflow/i)).toBeInTheDocument();
    expect(screen.getByText(/Healthy/i)).toBeInTheDocument();
  });

  test('renders resource scarcity meter with mock data', () => {
    const mockData = getMockData();
    mockData.resourceScarcity = 80;
    getMockData.mockReturnValue(mockData);

    render(<App />);
    expect(screen.getByText(/Resource Scarcity Meter/i)).toBeInTheDocument();
    expect(screen.getByText(/80%/i)).toBeInTheDocument();
  });
});
