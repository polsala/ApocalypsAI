import { render, screen, fireEvent, cleanup } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// Mock rationale: localStorage is a browser-specific API.
// For deterministic, offline testing, we mock it to control its behavior
// and prevent actual browser storage from being affected.
const localStorageMock = (function() {
  let store = {};
  return {
    getItem: jest.fn((key) => store[key] || null),
    setItem: jest.fn((key, value) => { store[key] = value.toString(); }),
    clear: jest.fn(() => { store = {}; }),
    removeItem: jest.fn((key) => { delete store[key]; })
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Mock rationale: window.confirm is a browser-specific API.
// We mock it to prevent actual dialogs from appearing during tests
// and to control the user's response for deterministic testing.
const mockConfirm = jest.fn(() => true);
Object.defineProperty(window, 'confirm', {
  value: mockConfirm,
});

describe('App Component', () => {
  beforeEach(() => {
    localStorageMock.clear(); // Clear local storage before each test
    mockConfirm.mockClear(); // Clear mock confirm calls
    cleanup(); // Clean up DOM after each test
  });

  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Wasteland Atlas/i)).toBeInTheDocument();
  });

  test('allows adding a new location', async () => {
    render(<App />);

    fireEvent.change(screen.getByLabelText(/Name:/i), { target: { value: 'Scavenger Camp Alpha' } });
    fireEvent.change(screen.getByLabelText(/Type:/i), { target: { value: 'Safe Zone' } });
    fireEvent.change(screen.getByLabelText(/Coordinates:/i), { target: { value: 'X:100 Y:200' } });
    fireEvent.change(screen.getByLabelText(/Description:/i), { target: { value: 'Friendly traders, good water source.' } });

    fireEvent.click(screen.getByRole('button', { name: /Add Location/i }));

    expect(await screen.findByText(/Scavenger Camp Alpha/i)).toBeInTheDocument();
    expect(screen.getByText(/Type: Safe Zone/i)).toBeInTheDocument();
    expect(screen.getByText(/Coordinates: X:100 Y:200/i)).toBeInTheDocument();
    expect(screen.getByText(/Description: Friendly traders, good water source./i)).toBeInTheDocument();

    // Verify localStorage was called
    expect(localStorageMock.setItem).toHaveBeenCalledWith(
      'wastelandAtlasLocations',
      expect.stringContaining('Scavenger Camp Alpha')
    );
  });

  test('persists locations across renders', () => {
    // Simulate a stored location
    localStorageMock.setItem('wastelandAtlasLocations', JSON.stringify([{
      id: 1,
      name: 'Old Bunker',
      type: 'Resource',
      coordinates: 'X:50 Y:50',
      description: 'Potential tech loot.'
    }]));

    render(<App />);

    expect(screen.getByText(/Old Bunker/i)).toBeInTheDocument();
    expect(screen.getByText(/Type: Resource/i)).toBeInTheDocument();
    expect(screen.getByText(/Coordinates: X:50 Y:50/i)).toBeInTheDocument();
  });

  test('filters locations by type', async () => {
    render(<App />);

    // Add a Hazard
    fireEvent.change(screen.getByLabelText(/Name:/i), { target: { value: 'Mutant Den' } });
    fireEvent.change(screen.getByLabelText(/Type:/i), { target: { value: 'Hazard' } });
    fireEvent.change(screen.getByLabelText(/Coordinates:/i), { target: { value: 'X:300 Y:300' } });
    fireEvent.click(screen.getByRole('button', { name: /Add Location/i }));

    // Add a Safe Zone
    fireEvent.change(screen.getByLabelText(/Name:/i), { target: { value: 'Oasis Spring' } });
    fireEvent.change(screen.getByLabelText(/Type:/i), { target: { value: 'Safe Zone' } });
    fireEvent.change(screen.getByLabelText(/Coordinates:/i), { target: { value: 'X:10 Y:10' } });
    fireEvent.click(screen.getByRole('button', { name: /Add Location/i }));

    // Initially, both should be visible
    expect(await screen.findByText(/Mutant Den/i)).toBeInTheDocument();
    expect(screen.getByText(/Oasis Spring/i)).toBeInTheDocument();

    // Filter by Safe Zone
    fireEvent.change(screen.getByLabelText(/Filter by Type:/i), { target: { value: 'Safe Zone' } });
    expect(screen.queryByText(/Mutant Den/i)).not.toBeInTheDocument();
    expect(screen.getByText(/Oasis Spring/i)).toBeInTheDocument();

    // Filter by Hazard
    fireEvent.change(screen.getByLabelText(/Filter by Type:/i), { target: { value: 'Hazard' } });
    expect(screen.getByText(/Mutant Den/i)).toBeInTheDocument();
    expect(screen.queryByText(/Oasis Spring/i)).not.toBeInTheDocument();

    // Filter by All
    fireEvent.change(screen.getByLabelText(/Filter by Type:/i), { target: { value: 'All' } });
    expect(screen.getByText(/Mutant Den/i)).toBeInTheDocument();
    expect(screen.getByText(/Oasis Spring/i)).toBeInTheDocument();
  });

  test('clears all locations', async () => {
    render(<App />);

    fireEvent.change(screen.getByLabelText(/Name:/i), { target: { value: 'Test Location' } });
    fireEvent.change(screen.getByLabelText(/Coordinates:/i), { target: { value: 'X:1 Y:1' } });
    fireEvent.click(screen.getByRole('button', { name: /Add Location/i }));

    expect(await screen.findByText(/Test Location/i)).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: /Clear All Locations/i }));

    // Confirm dialog is mocked to return true
    expect(mockConfirm).toHaveBeenCalledTimes(1);
    expect(screen.queryByText(/Test Location/i)).not.toBeInTheDocument();
    expect(screen.getByText(/No locations plotted yet, or no locations match the current filter./i)).toBeInTheDocument();
    expect(localStorageMock.setItem).toHaveBeenCalledWith('wastelandAtlasLocations', '[]');
  });

  test('shows alert if name or coordinates are missing', () => {
    const alertMock = jest.spyOn(window, 'alert').mockImplementation(() => {});
    render(<App />);

    fireEvent.change(screen.getByLabelText(/Name:/i), { target: { value: '' } }); // Missing name
    fireEvent.change(screen.getByLabelText(/Coordinates:/i), { target: { value: 'X:1 Y:1' } });
    fireEvent.click(screen.getByRole('button', { name: /Add Location/i }));

    expect(alertMock).toHaveBeenCalledWith('Name and Coordinates are required!');
    expect(screen.queryByText(/X:1 Y:1/i)).not.toBeInTheDocument(); // Location should not be added

    alertMock.mockRestore();
  });
});
