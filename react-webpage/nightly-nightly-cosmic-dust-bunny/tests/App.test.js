import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: localStorage is a browser-specific API and needs to be mocked
// for deterministic, offline testing in a Node.js environment (Jest).
// This ensures tests don't rely on actual browser storage or interfere with other tests.
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: jest.fn((key) => store[key] || null),
    setItem: jest.fn((key, value) => { store[key] = value; }),
    removeItem: jest.fn((key) => { delete store[key]; }),
    clear: jest.fn(() => { store = {}; }),
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('App Component', () => {
  beforeEach(() => {
    localStorageMock.clear(); // Clear local storage before each test
    jest.clearAllMocks(); // Clear mock call history
  });

  test('renders header and initial state', () => {
    render(<App />);
    expect(screen.getByText(/Cosmic Dust Bunny Collector/i)).toBeInTheDocument();
    expect(screen.getByText(/The cosmic chamber is pristine... for now!/i)).toBeInTheDocument();
  });

  test('adds a new dust bunny', () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/What tiny cosmic thought did you find?/i);
    const addButton = screen.getByRole('button', { name: /Collect Dust Bunny/i });

    fireEvent.change(inputElement, { target: { value: 'Remember to water the space-plants' } });
    fireEvent.click(addButton);

    expect(screen.getByText(/Remember to water the space-plants/i)).toBeInTheDocument();
    expect(localStorageMock.setItem).toHaveBeenCalledWith(
      'cosmicDustBunnies',
      expect.stringContaining('Remember to water the space-plants')
    );
    expect(screen.getByText(/Your Cosmic Collection \(1\)/i)).toBeInTheDocument();
  });

  test('does not add an empty dust bunny', () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/What tiny cosmic thought did you find?/i);
    const addButton = screen.getByRole('button', { name: /Collect Dust Bunny/i });

    fireEvent.change(inputElement, { target: { value: '   ' } }); // Whitespace only
    fireEvent.click(addButton);

    expect(screen.queryByText(/Your Cosmic Collection \(1\)/i)).not.toBeInTheDocument();
    expect(screen.getByText(/The cosmic chamber is pristine... for now!/i)).toBeInTheDocument();
    expect(localStorageMock.setItem).not.toHaveBeenCalledWith(
      'cosmicDustBunnies',
      '[]'
    ); // Should not save an empty array if nothing was added
  });

  test('clears all dust bunnies', () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/What tiny cosmic thought did you find?/i);
    const addButton = screen.getByRole('button', { name: /Collect Dust Bunny/i });
    const clearButton = screen.getByRole('button', { name: /Sweep Away All Dust Bunnies/i });

    fireEvent.change(inputElement, { target: { value: 'First cosmic thought' } });
    fireEvent.click(addButton);
    fireEvent.change(inputElement, { target: { value: 'Second cosmic task' } });
    fireEvent.click(addButton);

    expect(screen.getByText(/First cosmic thought/i)).toBeInTheDocument();
    expect(screen.getByText(/Second cosmic task/i)).toBeInTheDocument();
    expect(screen.getByText(/Your Cosmic Collection \(2\)/i)).toBeInTheDocument();

    fireEvent.click(clearButton);

    expect(screen.queryByText(/First cosmic thought/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Second cosmic task/i)).not.toBeInTheDocument();
    expect(screen.getByText(/The cosmic chamber is pristine... for now!/i)).toBeInTheDocument();
    expect(localStorageMock.setItem).toHaveBeenCalledWith('cosmicDustBunnies', '[]');
  });

  test('loads dust bunnies from local storage on mount', () => {
    // Pre-populate localStorage mock
    localStorageMock.setItem('cosmicDustBunnies', JSON.stringify([
      { id: 1, description: 'Pre-existing bunny', collectedAt: '2023-01-01T00:00:00.000Z' }
    ]));

    render(<App />);

    expect(screen.getByText(/Pre-existing bunny/i)).toBeInTheDocument();
    expect(screen.getByText(/Your Cosmic Collection \(1\)/i)).toBeInTheDocument();
  });
});
