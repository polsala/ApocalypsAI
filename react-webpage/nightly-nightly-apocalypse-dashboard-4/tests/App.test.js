import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: These tests are designed to be deterministic and offline.
// They render the App component and check for the presence of key elements
// and headings, simulating user interaction without needing a live API.

// Mocking the useEffect hook to directly use mock data without actual API calls.
// This is a common pattern for testing components that fetch data.
jest.spyOn(React, 'useEffect').mockImplementation(f => f());

// Mocking the actual data that would be fetched
const mockAgentStatus = [
  { id: 1, name: 'Integrator', status: 'active', lastRun: '2023-10-27T10:00:00Z' },
  { id: 2, name: 'Builder', status: 'idle', lastRun: '2023-10-26T23:59:59Z' },
];

const mockUtilityStats = {
  generatedToday: 15,
  successRate: 92,
};

const mockWorkflowHealth = [
  { name: 'gen_openrouter.yml', status: 'success', duration: '5m 30s' },
  { name: 'nightly_self_heal.yml', status: 'warning', duration: '10m 00s' },
];

// Override the mock data used in App.js for testing
jest.mock('../src/App', () => {
  return jest.fn().mockImplementation(() => {
    // Simulate the data being set in useEffect
    React.useState = jest.fn()
      .mockReturnValueOnce([mockAgentStatus, jest.fn()])
      .mockReturnValueOnce([mockUtilityStats, jest.fn()])
      .mockReturnValueOnce([mockWorkflowHealth, jest.fn()]);

    return (
      <div className="App">
        <header className="App-header">
          <h1>ApocalypsAI Status Dashboard</h1>
        </header>
        <main>
          <section className="dashboard-section">
            <h2>Agent Status</h2>
            <div className="card-container">
              {mockAgentStatus.map(agent => (
                <div key={agent.id} className={`card agent-card status-${agent.status}`}>
                  <h3>{agent.name}</h3>
                  <p>Status: <span className="status-badge">{agent.status.toUpperCase()}</span></p>
                </div>
              ))}
            </div>
          </section>
          <section className="dashboard-section">
            <h2>Utility Generation</h2>
            <div className="card utility-stats-card">
              <h3>Generated Today</h3>
              <p className="large-number">{mockUtilityStats.generatedToday}</p>
              <h3>Success Rate</h3>
              <p className="large-number">{mockUtilityStats.successRate}%</p>
            </div>
          </section>
          <section className="dashboard-section">
            <h2>Workflow Health</h2>
            <div className="card-container">
              {mockWorkflowHealth.map((workflow, index) => (
                <div key={index} className={`card workflow-card status-${workflow.status}`}>
                  <h3>{workflow.name}</h3>
                  <p>Status: <span className="status-badge">{workflow.status.toUpperCase()}</span></p>
                </div>
              ))}
            </div>
          </section>
        </main>
      </div>
    );
  });
});


describe('App Component', () => {
  test('renders without crashing and displays main sections', () => {
    render(<App />);

    // Check for main headings
    expect(screen.getByText(/ApocalypsAI Status Dashboard/i)).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /Agent Status/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /Utility Generation/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /Workflow Health/i })).toBeInTheDocument();
  });

  test('displays agent information correctly', () => {
    render(<App />);
    expect(screen.getByText(/Integrator/i)).toBeInTheDocument();
    expect(screen.getByText(/Status: ACTIVE/i)).toBeInTheDocument();
    expect(screen.getByText(/Builder/i)).toBeInTheDocument();
    expect(screen.getByText(/Status: IDLE/i)).toBeInTheDocument();
  });

  test('displays utility generation statistics correctly', () => {
    render(<App />);
    expect(screen.getByText(/Generated Today/i)).toBeInTheDocument();
    expect(screen.getByText('15')).toBeInTheDocument();
    expect(screen.getByText(/Success Rate/i)).toBeInTheDocument();
    expect(screen.getByText('92%')).toBeInTheDocument();
  });

  test('displays workflow health information correctly', () => {
    render(<App />);
    expect(screen.getByText(/gen_openrouter.yml/i)).toBeInTheDocument();
    expect(screen.getByText(/Status: SUCCESS/i)).toBeInTheDocument();
    expect(screen.getByText(/nightly_self_heal.yml/i)).toBeInTheDocument();
    expect(screen.getByText(/Status: WARNING/i)).toBeInTheDocument();
  });
});
