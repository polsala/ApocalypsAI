import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import App from '../src/App';

// Mock rationale: localStorage is a browser-specific API and needs to be mocked
// for a Node.js test environment (Vitest/JSDOM). This ensures tests are deterministic
// and don't interfere with actual browser storage or rely on its state.
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: (key) => store[key] || null,
    setItem: (key, value) => { store[key] = value.toString(); },
    clear: () => { store = {}; }
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('App', () => {
  beforeEach(() => {
    localStorage.clear(); // Clear localStorage before each test
    vi.clearAllMocks();
  });

  it('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Resonance Visualizer/i)).toBeInTheDocument();
  });

  it('displays "No temporal echoes detected yet" initially', () => {
    render(<App />);
    expect(screen.getByText(/No temporal echoes detected yet/i)).toBeInTheDocument();
  });

  it('allows adding a new event and updates the list', async () => {
    render(<App />);

    const eventNameInput = screen.getByLabelText(/Event Name:/i);
    const eventDateInput = screen.getByLabelText(/Event Date:/i);
    const resonanceSelect = screen.getByLabelText(/Resonance Strength \(1-10\):/i);
    const addButton = screen.getByRole('button', { name: /Add Event/i });

    fireEvent.change(eventNameInput, { target: { value: 'First Echo' } });
    fireEvent.change(eventDateInput, { target: { value: '2023-10-26T10:00' } });
    fireEvent.change(resonanceSelect, { target: { value: '7' } });
    fireEvent.click(addButton);

    await waitFor(() => {
      expect(screen.getByText('First Echo')).toBeInTheDocument();
      expect(screen.getByText(/Resonance: 7/i)).toBeInTheDocument();
      expect(screen.queryByText(/No temporal echoes detected yet/i)).not.toBeInTheDocument();
    });
  });

  it('calculates and displays overall resonance correctly', async () => {
    render(<App />);

    const eventNameInput = screen.getByLabelText(/Event Name:/i);
    const eventDateInput = screen.getByLabelText(/Event Date:/i);
    const resonanceSelect = screen.getByLabelText(/Resonance Strength \(1-10\):/i);
    const addButton = screen.getByRole('button', { name: /Add Event/i });

    // Add first event
    fireEvent.change(eventNameInput, { target: { value: 'Event A' } });
    fireEvent.change(eventDateInput, { target: { value: '2023-01-01T12:00' } });
    fireEvent.change(resonanceSelect, { target: { value: '5' } });
    fireEvent.click(addButton);

    // Add second event
    fireEvent.change(eventNameInput, { target: { value: 'Event B' } });
    fireEvent.change(eventDateInput, { target: { value: '2023-02-01T12:00' } });
    fireEvent.change(resonanceSelect, { target: { value: '9' } });
    fireEvent.click(addButton);

    await waitFor(() => {
      // (5 + 9) / 2 = 7
      expect(screen.getByText(/Current Score: 7.0/i)).toBeInTheDocument();
      expect(screen.getByText(/Strong temporal currents are active!/i)).toBeInTheDocument();
    });
  });

  it('loads events from localStorage on startup', () => {
    // Mock rationale: Simulate existing data in localStorage before the component mounts.
    const initialEvents = [
      { id: 1, name: 'Old Echo', date: '2022-01-01T00:00', resonance: 4 }
    ];
    localStorage.setItem('temporalEvents', JSON.stringify(initialEvents));

    render(<App />);

    expect(screen.getByText('Old Echo')).toBeInTheDocument();
    expect(screen.getByText(/Resonance: 4/i)).toBeInTheDocument();
    expect(screen.getByText(/Current Score: 4.0/i)).toBeInTheDocument();
  });

  it('persists events to localStorage when state changes', async () => {
    const setItemSpy = vi.spyOn(localStorage, 'setItem');
    render(<App />);

    const eventNameInput = screen.getByLabelText(/Event Name:/i);
    const eventDateInput = screen.getByLabelText(/Event Date:/i);
    const resonanceSelect = screen.getByLabelText(/Resonance Strength \(1-10\):/i);
    const addButton = screen.getByRole('button', { name: /Add Event/i });

    fireEvent.change(eventNameInput, { target: { value: 'Persistent Echo' } });
    fireEvent.change(eventDateInput, { target: { value: '2024-01-01T00:00' } });
    fireEvent.change(resonanceSelect, { target: { value: '6' } });
    fireEvent.click(addButton);

    await waitFor(() => {
      expect(setItemSpy).toHaveBeenCalledWith(
        'temporalEvents',
        expect.stringContaining('"name":"Persistent Echo","date":"2024-01-01T00:00","resonance":6')
      );
    });
  });
});
