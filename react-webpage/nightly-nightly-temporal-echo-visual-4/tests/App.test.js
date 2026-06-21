import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import mockEchoes from '../src/data/mockEchoes';

describe('App Component', () => {
  // Mock rationale: The App component directly imports mockEchoes.js,
  // so no external mocking library is needed for data. We test the rendering
  // based on this internal, deterministic data source.

  test('renders the main title', () => {
    render(<App />);
    const titleElement = screen.getByText(/Nightly Temporal Echo Visualizer/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders the timeline section title', () => {
    render(<App />);
    const timelineTitle = screen.getByText(/Temporal Echo Timeline/i);
    expect(timelineTitle).toBeInTheDocument();
  });

  test('renders the details section title', () => {
    render(<App />);
    const detailsTitle = screen.getByText(/Selected Echo Details/i);
    expect(detailsTitle).toBeInTheDocument();
  });

  test('displays initial message to select an echo', () => {
    render(<App />);
    const selectMessage = screen.getByText(/Select an echo from the timeline to view its details./i);
    expect(selectMessage).toBeInTheDocument();
  });

  test('loads and displays mock echoes on the timeline', () => {
    render(<App />);
    // Check if at least one echo type from mock data is rendered as a marker label
    expect(screen.getByText(/Minor/i)).toBeInTheDocument(); // From 'Minor Ripple'
    expect(screen.getByText(/Significant/i)).toBeInTheDocument(); // From 'Significant Distortion'
    expect(screen.getByText(/Temporal/i)).toBeInTheDocument(); // From 'Temporal Tear'
  });

  test('clicking an echo marker displays its details', () => {
    render(<App />);

    // Find the first echo marker (e.g., by its title attribute or text content)
    const firstEchoMarker = screen.getByTitle(`${mockEchoes[0].type} at ${new Date(mockEchoes[0].timestamp).toLocaleString()}`);
    fireEvent.click(firstEchoMarker);

    // Check if the details of the first echo are displayed
    expect(screen.getByText(mockEchoes[0].type)).toBeInTheDocument();
    expect(screen.getByText(`Magnitude: ${mockEchoes[0].magnitude}`)).toBeInTheDocument();
    expect(screen.getByText(`Location: ${mockEchoes[0].location}`)).toBeInTheDocument();
    expect(screen.getByText(`Description: ${mockEchoes[0].description}`)).toBeInTheDocument();

    // Ensure the initial message is no longer present
    expect(screen.queryByText(/Select an echo from the timeline to view its details./i)).not.toBeInTheDocument();
  });

  test('clicking a different echo marker updates the displayed details', () => {
    render(<App />);

    // Click the first echo
    const firstEchoMarker = screen.getByTitle(`${mockEchoes[0].type} at ${new Date(mockEchoes[0].timestamp).toLocaleString()}`);
    fireEvent.click(firstEchoMarker);

    // Click the second echo
    const secondEchoMarker = screen.getByTitle(`${mockEchoes[1].type} at ${new Date(mockEchoes[1].timestamp).toLocaleString()}`);
    fireEvent.click(secondEchoMarker);

    // Check if the details of the second echo are displayed
    expect(screen.getByText(mockEchoes[1].type)).toBeInTheDocument();
    expect(screen.getByText(`Magnitude: ${mockEchoes[1].magnitude}`)).toBeInTheDocument();
    expect(screen.getByText(`Location: ${mockEchoes[1].location}`)).toBeInTheDocument();
    expect(screen.getByText(`Description: ${mockEchoes[1].description}`)).toBeInTheDocument();

    // Ensure details of the first echo are no longer present
    expect(screen.queryByText(mockEchoes[0].type)).not.toBeInTheDocument();
  });
});
