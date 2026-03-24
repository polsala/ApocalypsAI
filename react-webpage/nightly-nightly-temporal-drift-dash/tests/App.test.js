import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import App, { fetchDriftData } from '../src/App';

// # Mock rationale: Mocking the fetchDriftData function to ensure tests are deterministic
// and do not rely on actual asynchronous operations or external data.
jest.mock('../src/App', () => ({
  ...jest.requireActual('../src/App'),
  fetchDriftData: jest.fn(() =>
    Promise.resolve([
      { id: 'test1', timestamp: '2024-07-21T08:00:00Z', severity: 'low', description: 'Test ripple.' },
      { id: 'test2', timestamp: '2024-07-21T09:00:00Z', severity: 'high', description: 'Test displacement.' }
    ])
  ),
}));

describe('App', () => {
  test('renders the main dashboard title', async () => {
    render(<App />);
    expect(screen.getByText(/ApocalypsAI Temporal Drift Dashboard/i)).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText(/Detected Temporal Anomalies/i)).toBeInTheDocument());
  });

  test('displays loading message initially and then drift data', async () => {
    render(<App />);
    expect(screen.getByText(/Calibrating temporal sensors... please wait./i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.queryByText(/Calibrating temporal sensors... please wait./i)).not.toBeInTheDocument();
      expect(screen.getByText(/Test ripple./i)).toBeInTheDocument();
      expect(screen.getByText(/Test displacement./i)).toBeInTheDocument();
    });
  });

  test('calls fetchDriftData on mount', async () => {
    render(<App />);
    await waitFor(() => expect(fetchDriftData).toHaveBeenCalledTimes(1));
  });
});
