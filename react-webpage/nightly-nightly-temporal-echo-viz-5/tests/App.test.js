import { render, screen, waitFor } from '@testing-library/react';
import App from '../src/App';
import mockEchoes from '../src/data/mockEchoes'; // Mock rationale: Directly import mock data to ensure deterministic and offline testing.

// Mock the EchoTimeline component to simplify testing App.js's data handling
jest.mock('../src/components/EchoTimeline', () => {
  return function MockEchoTimeline({ echoes }) {
    return (
      <div data-testid="mock-echo-timeline">
        {echoes.map(echo => (
          <div key={echo.id} data-testid={`echo-item-${echo.id}`}>
            {echo.description}
          </div>
        ))}
      </div>
    );
  };
});

describe('App Component', () => {
  test('renders header and loading message initially', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Visualizer/i)).toBeInTheDocument();
    expect(screen.getByText(/Calibrating temporal sensors.../i)).toBeInTheDocument();
  });

  test('renders EchoTimeline with mock data after loading', async () => {
    render(<App />);

    // Wait for the loading state to resolve and mock data to be passed
    await waitFor(() => {
      expect(screen.queryByText(/Calibrating temporal sensors.../i)).not.toBeInTheDocument();
    }, { timeout: 1000 }); // Allow time for the simulated setTimeout

    // Check if the mock EchoTimeline component is rendered
    const mockTimeline = screen.getByTestId('mock-echo-timeline');
    expect(mockTimeline).toBeInTheDocument();

    // Check if mock data descriptions are present, indicating data was passed
    mockEchoes.forEach(echo => {
      expect(screen.getByText(echo.description)).toBeInTheDocument();
    });
  });

  test('renders footer', () => {
    render(<App />);
    expect(screen.getByText(/\u00A9 ApocalypsAI Nightly Integrator/i)).toBeInTheDocument();
  });
});
