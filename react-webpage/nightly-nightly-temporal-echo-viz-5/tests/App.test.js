import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import mockEchoes from '../src/data/mockEchoes'; // # Mock rationale: Using local mock data for deterministic, offline tests.

describe('App Component', () => {
  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Temporal Echo Visualizer/i)).toBeInTheDocument();
  });

  test('displays all mock echoes initially', async () => {
    render(<App />);
    // Wait for the mock data to be "fetched" and rendered
    for (const echo of mockEchoes) {
      expect(await screen.findByText(new RegExp(echo.id))).toBeInTheDocument();
      expect(screen.getByText(new RegExp(echo.type))).toBeInTheDocument();
    }
    expect(screen.getAllByRole('listitem').length).toBe(mockEchoes.length);
  });

  test('filters echoes by type', async () => {
    render(<App />);
    const typeFilter = screen.getByLabelText(/Filter by Type:/i);
    fireEvent.change(typeFilter, { target: { value: 'Chronal Feedback' } });

    // Only 'Chronal Feedback' echoes should be visible
    expect(await screen.findByText(/echo-002/i)).toBeInTheDocument();
    expect(screen.getByText(/echo-005/i)).toBeInTheDocument();
    expect(screen.queryByText(/echo-001/i)).not.toBeInTheDocument(); // Temporal Ripple
    expect(screen.getAllByRole('listitem').length).toBe(2);
  });

  test('filters echoes by minimum intensity', async () => {
    render(<App />);
    const intensityFilter = screen.getByLabelText(/Min Intensity:/i);
    fireEvent.change(intensityFilter, { target: { value: '8' } });

    // Only echoes with intensity >= 8 should be visible
    expect(await screen.findByText(/echo-002/i)).toBeInTheDocument(); // Intensity 9
    expect(screen.getByText(/echo-005/i)).toBeInTheDocument(); // Intensity 8
    expect(screen.queryByText(/echo-001/i)).not.toBeInTheDocument(); // Intensity 7
    expect(screen.getAllByRole('listitem').length).toBe(2);
  });

  test('filters echoes by type and minimum intensity combined', async () => {
    render(<App />);
    const typeFilter = screen.getByLabelText(/Filter by Type:/i);
    const intensityFilter = screen.getByLabelText(/Min Intensity:/i);

    fireEvent.change(typeFilter, { target: { value: 'Temporal Ripple' } });
    fireEvent.change(intensityFilter, { target: { value: '5' } });

    // Only 'Temporal Ripple' with intensity >= 5
    expect(await screen.findByText(/echo-001/i)).toBeInTheDocument(); // Intensity 7
    expect(screen.queryByText(/echo-003/i)).not.toBeInTheDocument(); // Intensity 3
    expect(screen.queryByText(/echo-006/i)).not.toBeInTheDocument(); // Intensity 2
    expect(screen.getAllByRole('listitem').length).toBe(1);
  });

  test('displays "No temporal echoes" message when no matches', async () => {
    render(<App />);
    const typeFilter = screen.getByLabelText(/Filter by Type:/i);
    const intensityFilter = screen.getByLabelText(/Min Intensity:/i);

    fireEvent.change(typeFilter, { target: { value: 'NonExistentType' } });
    fireEvent.change(intensityFilter, { target: { value: '10' } });

    expect(await screen.findByText(/No temporal echoes matching current filters./i)).toBeInTheDocument();
    expect(screen.queryByRole('listitem', { name: /echo-/i })).not.toBeInTheDocument();
  });
});
