import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: We are testing the React component's rendering and interaction
// with its internal state and props. The simulated data in App.js's useEffect
// serves as a deterministic, offline data source for these tests, avoiding
// any external dependencies.
describe('App', () => {
  test('renders Nightly Chrono-Compass title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Chrono-Compass/i)).toBeInTheDocument();
  });

  test('renders ChronoMap component', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Stability Map/i)).toBeInTheDocument();
  });

  test('displays CorrectionSuggestions when a region is clicked', async () => {
    render(<App />);
    // Initially, suggestions should not be visible
    expect(screen.queryByText(/Correction Suggestions for/i)).not.toBeInTheDocument();

    // Click on a region (e.g., Alpha Sector)
    const alphaSector = await screen.findByText(/Alpha Sector/i);
    fireEvent.click(alphaSector);

    // Now, suggestions for Alpha Sector should be visible
    expect(screen.getByText(/Correction Suggestions for Alpha Sector/i)).toBeInTheDocument();
    expect(screen.getByText(/Temporal field within acceptable parameters. Maintain vigilance./i)).toBeInTheDocument();
  });

  test('displays correct suggestions for an unstable region', async () => {
    render(<App />);
    const epsilonVoid = await screen.findByText(/Epsilon Void/i);
    fireEvent.click(epsilonVoid);

    expect(screen.getByText(/Correction Suggestions for Epsilon Void/i)).toBeInTheDocument();
    expect(screen.getByText(/Critical/i)).toBeInTheDocument();
    expect(screen.getByText(/Immediate Chrono-Stabilization Protocol required. Deploy Temporal Anchors./i)).toBeInTheDocument();
  });
});
