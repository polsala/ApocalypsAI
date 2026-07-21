import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock localStorage for deterministic tests
// # Mock rationale: Ensures that morale entries are not persisted to the actual browser
// localStorage during tests, and allows for predictable initial states and verification
// of storage interactions.
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

// Mock Date.now() and new Date() for deterministic timestamps
// # Mock rationale: Ensures that the 'date' and 'id' fields in morale entries are predictable
// for testing purposes, preventing test failures due to varying timestamps.
const MOCK_DATE_NOW = 1678886400000; // March 15, 2023 12:00:00 PM UTC
const MOCK_DATE_STRING = new Date(MOCK_DATE_NOW).toLocaleString();

const mockDate = new Date(MOCK_DATE_NOW);
const mockDateConstructor = jest.fn(() => mockDate);
mockDateConstructor.toLocaleString = () => MOCK_DATE_STRING;

const originalDate = global.Date;

beforeAll(() => {
  global.Date = mockDateConstructor;
  jest.spyOn(global.Date, 'now').mockReturnValue(MOCK_DATE_NOW);
});

afterAll(() => {
  global.Date = originalDate; // Restore original Date object
  jest.restoreAllMocks();
});

beforeEach(() => {
  localStorage.clear(); // Clear localStorage before each test
});

describe('App', () => {
  test('renders the main title and initial elements', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Morale Meter/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Morale Level/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Log Morale/i })).toBeInTheDocument();
    expect(screen.getByText(/No morale entries yet/i)).toBeInTheDocument();
  });

  test('allows changing morale level with slider', () => {
    render(<App />);
    const slider = screen.getByLabelText(/Morale Level/i);
    fireEvent.change(slider, { target: { value: '8' } });
    expect(screen.getByText(/How's your spirit today\? \(8\/10\)/i)).toBeInTheDocument();
  });

  test('logs morale entry and displays feedback', () => {
    render(<App />);
    const slider = screen.getByLabelText(/Morale Level/i);
    const logButton = screen.getByRole('button', { name: /Log Morale/i });

    // Set morale to 7
    fireEvent.change(slider, { target: { value: '7' } });
    fireEvent.click(logButton);

    expect(screen.getByText(/Feeling spry! Did you find a fresh can of pre-apocalypse peaches\? Share the joy!/i)).toBeInTheDocument();
    expect(screen.getByText(/Level: 7\/10/i)).toBeInTheDocument();
    expect(screen.getByText(new RegExp(`\(${MOCK_DATE_STRING}\)`))).toBeInTheDocument();
    expect(screen.queryByText(/No morale entries yet/i)).not.toBeInTheDocument();

    // Set morale to 2
    fireEvent.change(slider, { target: { value: '2' } });
    fireEvent.click(logButton);

    expect(screen.getByText(/The void whispers despair, but even a void has echoes of hope. Hang in there, survivor!/i)).toBeInTheDocument();
    expect(screen.getByText(/Level: 2\/10/i)).toBeInTheDocument();
    // Check that both entries are present
    const moraleItems = screen.getAllByRole('listitem');
    expect(moraleItems).toHaveLength(2);
    expect(moraleItems[0]).toHaveTextContent('Level: 2/10'); // Newest entry first
    expect(moraleItems[1]).toHaveTextContent('Level: 7/10');
  });

  test('loads morale entries from localStorage on startup', () => {
    // Pre-populate localStorage
    const initialEntries = [
      {
        id: MOCK_DATE_NOW - 10000, // Older entry
        level: 6,
        date: new Date(MOCK_DATE_NOW - 10000).toLocaleString(),
        feedback: 'Steady as a mutant cockroach! Keep scuttling forward, friend.'
      }
    ];
    localStorage.setItem('moraleEntries', JSON.stringify(initialEntries));

    render(<App />);

    expect(screen.getByText(/Level: 6\/10/i)).toBeInTheDocument();
    expect(screen.getByText(/Steady as a mutant cockroach! Keep scuttling forward, friend./i)).toBeInTheDocument();
  });

  test('feedback changes based on morale level', () => {
    render(<App />);
    const slider = screen.getByLabelText(/Morale Level/i);
    const logButton = screen.getByRole('button', { name: /Log Morale/i });

    // Test low morale feedback
    fireEvent.change(slider, { target: { value: '1' } });
    fireEvent.click(logButton);
    expect(screen.getByText(/The void whispers despair/i)).toBeInTheDocument();

    // Test medium-low morale feedback
    fireEvent.change(slider, { target: { value: '4' } });
    fireEvent.click(logButton);
    expect(screen.getByText(/A bit dusty today, eh\?/i)).toBeInTheDocument();

    // Test medium morale feedback
    fireEvent.change(slider, { target: { value: '6' } });
    fireEvent.click(logButton);
    expect(screen.getByText(/Steady as a mutant cockroach!/i)).toBeInTheDocument();

    // Test medium-high morale feedback
    fireEvent.change(slider, { target: { value: '8' } });
    fireEvent.click(logButton);
    expect(screen.getByText(/Feeling spry!/i)).toBeInTheDocument();

    // Test high morale feedback
    fireEvent.change(slider, { target: { value: '10' } });
    fireEvent.click(logButton);
    expect(screen.getByText(/Radiant as a supernova!/i)).toBeInTheDocument();
  });
});
