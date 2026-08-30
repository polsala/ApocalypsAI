import { render, screen, waitFor } from '@testing-library/react';
import App from '../src/App';
import EchoTimeline from '../src/EchoTimeline'; // Import the component to mock
import sampleEchoes from '../src/data/sample-echoes.json'; // Import sample data

// Mock rationale: We mock the EchoTimeline component to isolate the testing
// of the App component. This ensures that App's responsibilities (loading data,
// handling loading/error states, and passing data to EchoTimeline) are tested
// independently of EchoTimeline's rendering logic. This makes tests faster
// and less brittle to changes in the visualization component.
jest.mock('../src/EchoTimeline', () => {
  return jest.fn((props) => (
    <div data-testid="mock-echo-timeline">
      Mock Echo Timeline for {props.echoes.length} echoes.
    </div>
  ));
});

describe('App', () => {
  beforeEach(() => {
    // Clear mock calls before each test
    EchoTimeline.mockClear();
  });

  test('renders loading state initially', () => {
    render(<App />);
    expect(screen.getByText(/Loading temporal echoes.../i)).toBeInTheDocument();
  });

  test('renders header and footer', async () => {
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText(/Nightly Temporal Echo Visualizer/i)).toBeInTheDocument();
      expect(screen.getByText(/ApocalypsAI Integrator Agent/i)).toBeInTheDocument();
    });
  });

  test('loads sample echoes and passes them to EchoTimeline', async () => {
    render(<App />);

    // Wait for the loading state to resolve and content to appear
    await waitFor(() => {
      expect(screen.queryByText(/Loading temporal echoes.../i)).not.toBeInTheDocument();
      expect(screen.getByTestId('mock-echo-timeline')).toBeInTheDocument();
    });

    // Verify that EchoTimeline was called with the correct props
    expect(EchoTimeline).toHaveBeenCalledTimes(1);
    expect(EchoTimeline).toHaveBeenCalledWith(
      expect.objectContaining({
        echoes: sampleEchoes,
      }),
      {} // Second argument is context, usually empty
    );
    expect(screen.getByText(`Mock Echo Timeline for ${sampleEchoes.length} echoes.`)).toBeInTheDocument();
  });

  test('renders "No temporal echoes detected" if sample data is empty', async () => {
    // Mock rationale: Temporarily override the imported sampleEchoes to be empty
    // for this specific test case, simulating a scenario where no data is found.
    jest.spyOn(require('../src/data/sample-echoes.json'), 'default', 'get').mockReturnValueOnce([]);

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/No temporal echoes detected. All clear... for now./i)).toBeInTheDocument();
    });
    expect(EchoTimeline).not.toHaveBeenCalled(); // EchoTimeline should not be rendered if no echoes
  });

  // Restore original mock after all tests in this describe block
  afterAll(() => {
    jest.restoreAllMocks();
  });
});
