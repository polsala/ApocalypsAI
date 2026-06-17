import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Mock the EchoVisualizer component to prevent canvas rendering issues in tests
// # Mock rationale: The EchoVisualizer component contains canvas drawing logic and animation loops
// # that are difficult and unnecessary to test in isolation within the App component's tests.
// # Mocking it ensures that App's rendering and structure are tested without side effects
// # from the complex canvas operations, making tests deterministic and faster.
jest.mock('../src/EchoVisualizer', () => {
  return function MockEchoVisualizer() {
    return <div data-testid="mock-echo-visualizer">Mock Echo Visualizer</div>;
  };
});

describe('App', () => {
  test('renders the main heading', () => {
    render(<App />);
    const headingElement = screen.getByText(/Temporal Echo Visualizer/i);
    expect(headingElement).toBeInTheDocument();
  });

  test('renders the subtitle', () => {
    render(<App />);
    const subtitleElement = screen.getByText(/Observing the ripples in time's fabric./i);
    expect(subtitleElement).toBeInTheDocument();
  });

  test('renders the EchoVisualizer component', () => {
    render(<App />);
    const visualizerElement = screen.getByTestId('mock-echo-visualizer');
    expect(visualizerElement).toBeInTheDocument();
  });
});
