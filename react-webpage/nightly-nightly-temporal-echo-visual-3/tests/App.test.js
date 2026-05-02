import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';
import mockEchoes from '../src/data/mockEchoes'; // Import mock data for direct assertion

// Mock rationale: Using static mock data ensures deterministic tests without external dependencies.

describe('App Component', () => {
  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Visualizer/i)).toBeInTheDocument();
  });

  test('displays all mock echoes initially', () => {
    render(<App />);
    // Check if all echoes from mockEchoes are rendered
    mockEchoes.forEach(echo => {
      expect(screen.getByText(new RegExp(echo.location, 'i'))).toBeInTheDocument();
      expect(screen.getByText(new RegExp(echo.description.substring(0, 20), 'i'))).toBeInTheDocument(); // Check part of description
    });
    expect(screen.getAllByRole('heading', { level: 3 }).length).toBe(mockEchoes.length);
  });

  test('filters echoes by type "Temporal Ripple"', () => {
    render(<App />);
    const filterDropdown = screen.getByLabelText(/Filter by Echo Type:/i);
    fireEvent.change(filterDropdown, { target: { value: 'Temporal Ripple' } });

    const temporalRippleEchoes = mockEchoes.filter(echo => echo.type === 'Temporal Ripple');
    const otherEchoes = mockEchoes.filter(echo => echo.type !== 'Temporal Ripple');

    // Assert that only 'Temporal Ripple' echoes are visible
    temporalRippleEchoes.forEach(echo => {
      expect(screen.getByText(new RegExp(echo.location, 'i'))).toBeInTheDocument();
    });
    otherEchoes.forEach(echo => {
      expect(screen.queryByText(new RegExp(echo.location, 'i'))).not.toBeInTheDocument();
    });
    expect(screen.getAllByRole('heading', { level: 3 }).length).toBe(temporalRippleEchoes.length);
  });

  test('filters echoes by type "Void Whisper"', () => {
    render(<App />);
    const filterDropdown = screen.getByLabelText(/Filter by Echo Type:/i);
    fireEvent.change(filterDropdown, { target: { value: 'Void Whisper' } });

    const voidWhisperEchoes = mockEchoes.filter(echo => echo.type === 'Void Whisper');
    const otherEchoes = mockEchoes.filter(echo => echo.type !== 'Void Whisper');

    // Assert that only 'Void Whisper' echoes are visible
    voidWhisperEchoes.forEach(echo => {
      expect(screen.getByText(new RegExp(echo.location, 'i'))).toBeInTheDocument();
    });
    otherEchoes.forEach(echo => {
      expect(screen.queryByText(new RegExp(echo.location, 'i'))).not.toBeInTheDocument();
    });
    expect(screen.getAllByRole('heading', { level: 3 }).length).toBe(voidWhisperEchoes.length);
  });

  test('displays "No temporal echoes" message when no echoes match filter', () => {
    render(<App />);
    const filterDropdown = screen.getByLabelText(/Filter by Echo Type:/i);
    // Choose a type that doesn't exist in mock data, or filter to an empty set
    fireEvent.change(filterDropdown, { target: { value: 'NonExistentType' } });

    expect(screen.getByText(/No temporal echoes of this type detected./i)).toBeInTheDocument();
    expect(screen.queryAllByRole('heading', { level: 3 }).length).toBe(0);
  });

  test('resets filter to "All" and shows all echoes', () => {
    render(<App />);
    const filterDropdown = screen.getByLabelText(/Filter by Echo Type:/i);

    // First, filter to a specific type
    fireEvent.change(filterDropdown, { target: { value: 'Void Whisper' } });
    expect(screen.getAllByRole('heading', { level: 3 }).length).toBe(mockEchoes.filter(e => e.type === 'Void Whisper').length);

    // Then, reset to "All"
    fireEvent.change(filterDropdown, { target: { value: 'All' } });
    expect(screen.getAllByRole('heading', { level: 3 }).length).toBe(mockEchoes.length);
  });
});
