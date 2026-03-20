import { render, screen, waitFor } from '@testing-library/react';
import App from '../src/App';

// Mock the TemporalEchoDisplay component to simplify testing App.js in isolation
jest.mock('../src/TemporalEchoDisplay', () => {
  return function MockTemporalEchoDisplay({ echoes }) {
    // # Mock rationale: Prevents the need to render and test the child component's full DOM structure
    // # within the parent's test. It allows us to verify that App.js passes the correct props
    // # to TemporalEchoDisplay without worrying about TemporalEchoDisplay's internal rendering logic.
    return (
      <div data-testid="mock-echo-display">
        {echoes.map(echo => (
          <div key={echo.id} data-testid={`echo-item-${echo.id}`}>
            {echo.type}
          </div>
        ))}
      </div>
    );
  };
});

describe('App', () => {
  test('renders the main title', () => {
    render(<App />);
    const titleElement = screen.getByText(/Temporal Echo Visualizer/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('shows loading message initially', () => {
    render(<App />);
    const loadingElement = screen.getByText(/Loading temporal echoes.../i);
    expect(loadingElement).toBeInTheDocument();
  });

  test('renders TemporalEchoDisplay with data after loading', async () => {
    render(<App />);
    // Wait for the simulated data fetch to complete
    await waitFor(() => {
      expect(screen.queryByText(/Loading temporal echoes.../i)).not.toBeInTheDocument();
    }, { timeout: 1000 }); // Adjust timeout if mock delay changes

    // Check if the mocked TemporalEchoDisplay is rendered
    const mockDisplay = screen.getByTestId('mock-echo-display');
    expect(mockDisplay).toBeInTheDocument();

    // Check if the mock data items are passed to the display
    expect(screen.getByTestId('echo-item-echo-001')).toHaveTextContent('Minor Ripple');
    expect(screen.getByTestId('echo-item-echo-004')).toHaveTextContent('Major Anomaly');
  });
});
