import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: We are mocking the useEffect hook to control the data updates and avoid
// relying on actual timers or external data sources during testing. This ensures deterministic tests.
jest.useFakeTimers();

describe('App Component', () => {
  test('renders the dashboard title', () => {
    render(<App />);
    expect(screen.getByText(/ApocalypsAI Status Dashboard/i)).toBeInTheDocument();
  });

  test('displays agent status section', () => {
    render(<App />);
    expect(screen.getByText(/Agent Status/i)).toBeInTheDocument();
  });

  test('displays utility counts section', () => {
    render(<App />);
    expect(screen.getByText(/Utility Counts by Classifier/i)).toBeInTheDocument();
  });

  test('displays workflow health section', () => {
    render(<App />);
    expect(screen.getByText(/Workflow Health/i)).toBeInTheDocument();
  });

  test('displays resource scarcity section', () => {
    render(<App />);
    expect(screen.getByText(/Resource Scarcity Meter/i)).toBeInTheDocument();
  });

  test('updates agent status after a delay', async () => {
    render(<App />);
    // Advance timers by 5 seconds to trigger the first useEffect update
    jest.advanceTimersByTime(5000);

    // Wait for the state to update. The exact text might vary due to random status.
    // We'll check for the presence of status indicators.
    await waitFor(() => {
      expect(screen.getByText(/ACTIVE|IDLE/i)).toBeInTheDocument();
    });
  });

  test('updates utility counts after a delay', async () => {
    render(<App />);
    jest.advanceTimersByTime(5000);

    await waitFor(() => {
      // Check for a representative utility count, e.g., python-utils
      expect(screen.getByText(/python-utils:/i)).toBeInTheDocument();
      expect(screen.getByText(/react-webpage:/i)).toBeInTheDocument();
    });
  });

  test('updates workflow health after a delay', async () => {
    render(<App />);
    jest.advanceTimersByTime(5000);

    await waitFor(() => {
      expect(screen.getByText(/STABLE|WARNING|CRITICAL/i)).toBeInTheDocument();
    });
  });

  test('updates resource scarcity meter after a delay', async () => {
    render(<App />);
    jest.advanceTimersByTime(5000);

    await waitFor(() => {
      // Check if the meter bar is rendered and has some width
      const meterBar = screen.getByText(/%/, {
        selector: '.meter-bar'
      });
      expect(meterBar).toBeInTheDocument();
      // We can't assert exact width due to randomness, but we can check it's not 0%
      expect(meterBar).not.toHaveStyle('width: 0%');
    });
  });
});
