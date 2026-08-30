import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: We are testing the React component's rendering and interaction logic.
// The MOCK_ECHOES data is directly imported from App.js, ensuring the test uses the same
// initial data structure as the component under test, making it deterministic and offline.
// No external API calls or complex environment setups are needed.

describe('App Component', () => {
  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Echo Chamber Visualizer/i)).toBeInTheDocument();
  });

  test('displays initial echoes', () => {
    render(<App />);
    expect(screen.getByText(/Minor temporal ripple detected near Sector 7G./i)).toBeInTheDocument();
    expect(screen.getByText(/Unusual spike in 'Scrap Metal' readings in the Western Wastes./i)).toBeInTheDocument();
    expect(screen.getByText(/Repeated distress signal pattern from unknown origin./i)).toBeInTheDocument();
  });

  test('filters echoes by category', () => {
    render(<App />);
    const filterInput = screen.getByPlaceholderText(/Filter echoes.../i);
    fireEvent.change(filterInput, { target: { value: 'Anomaly' } });

    expect(screen.getByText(/Minor temporal ripple detected near Sector 7G./i)).toBeInTheDocument();
    expect(screen.getByText(/Flickering reality distortion field near the old power plant./i)).toBeInTheDocument();
    expect(screen.queryByText(/Unusual spike in 'Scrap Metal' readings in the Western Wastes./i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Repeated distress signal pattern from unknown origin./i)).not.toBeInTheDocument();
  });

  test('filters echoes by description', () => {
    render(<App />);
    const filterInput = screen.getByPlaceholderText(/Filter echoes.../i);
    fireEvent.change(filterInput, { target: { value: 'Scrap Metal' } });

    expect(screen.getByText(/Unusual spike in 'Scrap Metal' readings in the Western Wastes./i)).toBeInTheDocument();
    expect(screen.queryByText(/Minor temporal ripple detected near Sector 7G./i)).not.toBeInTheDocument();
  });

  test('displays no echoes message when filter yields no results', () => {
    render(<App />);
    const filterInput = screen.getByPlaceholderText(/Filter echoes.../i);
    fireEvent.change(filterInput, { target: { value: 'NonExistentEcho' } });

    expect(screen.getByText(/No echoes found matching your criteria./i)).toBeInTheDocument();
    expect(screen.queryByText(/Minor temporal ripple detected near Sector 7G./i)).not.toBeInTheDocument();
  });

  test('filter is case-insensitive', () => {
    render(<App />);
    const filterInput = screen.getByPlaceholderText(/Filter echoes.../i);
    fireEvent.change(filterInput, { target: { value: 'anomaly' } });

    expect(screen.getByText(/Minor temporal ripple detected near Sector 7G./i)).toBeInTheDocument();
    expect(screen.getByText(/Flickering reality distortion field near the old power plant./i)).toBeInTheDocument();
  });
});
