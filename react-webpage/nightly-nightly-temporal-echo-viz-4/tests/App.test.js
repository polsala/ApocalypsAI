import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import EchoTimeline from '../src/components/EchoTimeline';
import mockEchoes from '../src/data/mockEchoes'; // # Mock rationale: Directly import mock data for deterministic, offline testing.

describe('App Component', () => {
  test('renders header and filters', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Temporal Echo Visualizer/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Filter by Intensity:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Filter by Origin:/i)).toBeInTheDocument();
  });

  test('displays all echoes by default', () => {
    render(<App />);
    // Check if all mock echoes are rendered
    mockEchoes.forEach(echo => {
      expect(screen.getByText(new RegExp(echo.description.substring(0, 20), 'i'))).toBeInTheDocument();
    });
    expect(screen.getAllByText(/Echo ID:/i)).toHaveLength(mockEchoes.length);
  });

  test('filters echoes by intensity correctly', () => {
    render(<App />);
    const intensityFilter = screen.getByLabelText(/Filter by Intensity:/i);
    fireEvent.change(intensityFilter, { target: { value: '5' } });

    // Only echoes with intensity 5 should be visible
    const intensity5Echoes = mockEchoes.filter(echo => echo.intensity === 5);
    intensity5Echoes.forEach(echo => {
      expect(screen.getByText(new RegExp(echo.description.substring(0, 20), 'i'))).toBeInTheDocument();
    });

    const nonIntensity5Echoes = mockEchoes.filter(echo => echo.intensity !== 5);
    nonIntensity5Echoes.forEach(echo => {
      expect(screen.queryByText(new RegExp(echo.description.substring(0, 20), 'i'))).not.toBeInTheDocument();
    });
    expect(screen.getAllByText(/Echo ID:/i)).toHaveLength(intensity5Echoes.length);
  });

  test('filters echoes by origin correctly', () => {
    render(<App />);
    const originFilter = screen.getByLabelText(/Filter by Origin:/i);
    fireEvent.change(originFilter, { target: { value: 'Future' } });

    // Only echoes with origin 'Future' should be visible
    const futureEchoes = mockEchoes.filter(echo => echo.origin === 'Future');
    futureEchoes.forEach(echo => {
      expect(screen.getByText(new RegExp(echo.description.substring(0, 20), 'i'))).toBeInTheDocument();
    });

    const nonFutureEchoes = mockEchoes.filter(echo => echo.origin !== 'Future');
    nonFutureEchoes.forEach(echo => {
      expect(screen.queryByText(new RegExp(echo.description.substring(0, 20), 'i'))).not.toBeInTheDocument();
    });
    expect(screen.getAllByText(/Echo ID:/i)).toHaveLength(futureEchoes.length);
  });

  test('displays "No echoes" message when no echoes match filters', () => {
    render(<App />);
    const intensityFilter = screen.getByLabelText(/Filter by Intensity:/i);
    fireEvent.change(intensityFilter, { target: { value: '1' } }); // Filter for intensity 1
    const originFilter = screen.getByLabelText(/Filter by Origin:/i);
    fireEvent.change(originFilter, { target: { value: 'Past' } }); // Filter for origin Past

    // There are no echoes with intensity 1 AND origin Past in mock data
    expect(screen.getByText(/No echoes match the current filters. The timeline is eerily quiet.../i)).toBeInTheDocument();
    expect(screen.queryByText(/Echo ID:/i)).not.toBeInTheDocument();
  });
});

describe('EchoTimeline Component', () => {
  test('renders a list of EchoCards', () => {
    render(<EchoTimeline echoes={mockEchoes.slice(0, 2)} />); // Render with a subset of echoes
    expect(screen.getByText(/Faint echo of a forgotten tea party/i)).toBeInTheDocument();
    expect(screen.getByText(/Strong resonance of a giant, sentient toaster uprising/i)).toBeInTheDocument();
    expect(screen.getAllByText(/Echo ID:/i)).toHaveLength(2);
  });

  test('renders "No echoes" message when provided an empty array', () => {
    render(<EchoTimeline echoes={[]} />);
    expect(screen.getByText(/No echoes match the current filters. The timeline is eerily quiet.../i)).toBeInTheDocument();
  });
});
