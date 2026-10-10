import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: We don't want to render the actual Leaflet map in tests,
// nor do we want to make network requests for map tiles. We're testing
// the App's ability to render its child components and pass data.
jest.mock('../src/components/EchoMap', () => {
  return function MockEchoMap(props) {
    return <div data-testid="mock-echo-map">Mock Echo Map for {props.echoes.length} echoes</div>;
  };
});

jest.mock('../src/components/EchoDisplay', () => {
  return function MockEchoDisplay(props) {
    return (
      <div data-testid="mock-echo-display">
        Mock Echo Display for {props.selectedEcho ? props.selectedEcho.id : 'no echo'}
      </div>
    );
  };
});

describe('App', () => {
  test('renders header and main sections', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Visualization/i)).toBeInTheDocument();
    expect(screen.getByText(/Unveiling the whispers of the past/i)).toBeInTheDocument();
    expect(screen.getByTestId('mock-echo-map')).toBeInTheDocument();
    expect(screen.getByTestId('mock-echo-display')).toBeInTheDocument();
  });

  test('EchoMap receives echoes data', async () => {
    render(<App />);
    // Mock data has 5 echoes
    expect(await screen.findByText(/Mock Echo Map for 5 echoes/i)).toBeInTheDocument();
  });

  test('EchoDisplay initially shows no echo selected message', () => {
    render(<App />);
    expect(screen.getByText(/Mock Echo Display for no echo/i)).toBeInTheDocument();
  });
});
