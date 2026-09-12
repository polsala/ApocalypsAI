import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Mocking the child components to isolate App's behavior
jest.mock('../src/components/AgentStatusCard', () => () => <div>MockAgentStatusCard</div>);
jest.mock('../src/components/WorkflowIndicator', () => () => <div>MockWorkflowIndicator</div>);

// Mocking the mockData module
jest.mock('../src/utils/mockData', () => ({
  generateMockAgentData: jest.fn(() => [
    { id: 1, name: 'Mock Agent 1', status: 'Active' },
    { id: 2, name: 'Mock Agent 2', status: 'Idle' }
  ]),
  generateMockWorkflowData: jest.fn(() => ({ status: 'Success' }))
}));

describe('App Component', () => {
  test('renders the main header and sections', () => {
    render(<App />);
    expect(screen.getByText(/ApocalypsAI Status Dashboard/i)).toBeInTheDocument();
    expect(screen.getByText(/Agent Status/i)).toBeInTheDocument();
    expect(screen.getByText(/Workflow Health/i)).toBeInTheDocument();
  });

  test('renders mock agent cards and workflow indicator', () => {
    render(<App />);
    // Since we mocked the child components, we expect to see their mock representations
    expect(screen.getByText('MockAgentStatusCard')).toBeInTheDocument();
    expect(screen.getByText('MockWorkflowIndicator')).toBeInTheDocument();
  });
});
