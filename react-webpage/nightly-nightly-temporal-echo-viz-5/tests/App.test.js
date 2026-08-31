import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import * as EchoDetector from '../src/EchoDetector';

describe('App Component', () => {
  // Mock rationale: We want to test the App's behavior in response to echo detection,
  // not the actual echo detection logic itself. Mocking ensures deterministic results.
  const mockDetectEcho = jest.spyOn(EchoDetector, 'detectEcho');

  beforeEach(() => {
    mockDetectEcho.mockClear();
    // Provide a default mock implementation for detectEcho
    mockDetectEcho.mockImplementation((x, y) => {
      if (x === 5 && y === 5) return { strength: 0.9, type: 'Temporal Rift', id: `echo-${x}-${y}` };
      if (x === 2 && y === 8) return { strength: 0.75, type: 'Echo Chamber', id: `echo-${x}-${y}` };
      return { strength: 0.05, type: 'Stable Zone', id: `echo-${x}-${y}` };
    });
  });

  test('renders header and legend', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo-Location Visualizer/i)).toBeInTheDocument();
    expect(screen.getByText(/Legend/i)).toBeInTheDocument();
    expect(screen.getByText(/Temporal Rift/i)).toBeInTheDocument();
  });

  test('clicking a cell triggers echo detection and displays echo', () => {
    render(<App />);
    const cellToClick = screen.getByTitle('Ping (0,0)'); // Find a default cell
    fireEvent.click(cellToClick);

    expect(mockDetectEcho).toHaveBeenCalledWith(0, 0);
    // Check if the echo indicator is present in the clicked cell
    const clickedCell = screen.getByTitle(/Echo: Stable Zone \(Strength: 0.05\)/i);
    expect(clickedCell).toBeInTheDocument();
    expect(clickedCell.querySelector('.echo-indicator')).toBeInTheDocument();
  });

  test('clicking a specific anomaly cell displays correct echo type', () => {
    render(<App />);
    // Click the cell where a Temporal Rift is mocked to appear
    const riftCell = screen.getByTitle('Ping (5,5)');
    fireEvent.click(riftCell);

    expect(mockDetectEcho).toHaveBeenCalledWith(5, 5);
    const detectedRiftCell = screen.getByTitle(/Echo: Temporal Rift \(Strength: 0.90\)/i);
    expect(detectedRiftCell).toBeInTheDocument();
    expect(detectedRiftCell).toHaveClass('temporal-rift');
  });

  test('clicking the same cell multiple times updates the echo (if logic allowed, here it just re-adds)', () => {
    render(<App />);
    const cell = screen.getByTitle('Ping (0,0)');
    fireEvent.click(cell);
    fireEvent.click(cell);

    expect(mockDetectEcho).toHaveBeenCalledTimes(2);
    // The current implementation replaces the echo if ID matches, so only one should be visible
    const echoes = screen.getAllByTitle(/Echo: Stable Zone/i);
    expect(echoes.length).toBe(1);
  });
});
