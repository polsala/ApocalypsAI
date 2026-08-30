import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../src/App';
import ChronoInput from '../src/ChronoInput';
import ChronoChart from '../src/ChronoChart';

// # Mock rationale: localStorage is a browser API and needs to be mocked for deterministic
// # and isolated testing. This prevents tests from interfering with actual browser storage
// # and ensures consistent test results.
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: (key) => store[key] || null,
    setItem: (key, value) => { store[key] = value.toString(); },
    clear: () => { store = {}; },
    removeItem: (key) => { delete store[key]; }
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// # Mock rationale: The Date object is non-deterministic. Mocking it ensures that
// # timestamps generated within the app (e.g., when adding an entry) are consistent
// # across test runs, making tests deterministic.
const MOCK_DATE = new Date('2023-10-27T10:00:00.000Z');
const MOCK_DATE_PLUS_HOUR = new Date('2023-10-27T11:00:00.000Z');

const mockDate = (date) => {
  const _Date = Date;
  global.Date = class extends _Date {
    constructor(dateString) {
      if (dateString) {
        return new _Date(dateString);
      }
      return date;
    }
  };
  global.Date.now = jest.fn(() => date.getTime());
};

const unmockDate = () => {
  global.Date = Date;
};

// # Mock rationale: Chart.js components are visual and can be complex to test directly.
// # Mocking the react-chartjs-2 Line component simplifies tests by ensuring we only
// # check if it's rendered with the correct data, rather than testing the charting library itself.
jest.mock('react-chartjs-2', () => ({
  Line: jest.fn(() => null) // Mock the Line component to render nothing
}));

describe('Nightly Chrono-Compass App', () => {
  beforeEach(() => {
    localStorage.clear();
    mockDate(MOCK_DATE);
    jest.clearAllMocks();
  });

  afterEach(() => {
    unmockDate();
  });

  test('renders app title and initial message', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Chrono-Compass/i)).toBeInTheDocument();
    expect(screen.getByText(/Log some entries to see your temporal patterns!/i)).toBeInTheDocument();
  });

  test('ChronoInput allows logging an entry and updates App state', async () => {
    render(<App />);

    const energySlider = screen.getByLabelText(/Energy Level:/i);
    const focusSlider = screen.getByLabelText(/Focus Level:/i);
    const timeSpeedSlider = screen.getByLabelText(/Perceived Time Speed:/i);
    const logButton = screen.getByRole('button', { name: /Log Entry/i });

    // Simulate user input
    fireEvent.change(energySlider, { target: { value: '8' } });
    fireEvent.change(focusSlider, { target: { value: '7' } });
    fireEvent.change(timeSpeedSlider, { target: { value: '6' } });

    await userEvent.click(logButton);

    // Expect the chart to be rendered now that there's data
    await waitFor(() => {
      expect(screen.queryByText(/Log some entries to see your temporal patterns!/i)).not.toBeInTheDocument();
      expect(screen.getByText(/Temporal Patterns/i)).toBeInTheDocument();
    });

    // Verify localStorage was updated
    const storedEntries = JSON.parse(localStorage.getItem('chronoCompassEntries'));
    expect(storedEntries).toHaveLength(1);
    expect(storedEntries[0]).toEqual({
      energy: 8,
      focus: 7,
      timeSpeed: 6,
      timestamp: MOCK_DATE.toISOString(),
    });

    // Add a second entry at a different time
    unmockDate(); // Unmock to allow setting a new mock date
    mockDate(MOCK_DATE_PLUS_HOUR);

    fireEvent.change(energySlider, { target: { value: '3' } });
    fireEvent.change(focusSlider, { target: { value: '4' } });
    fireEvent.change(timeSpeedSlider, { target: { value: '2' } });

    await userEvent.click(logButton);

    const updatedStoredEntries = JSON.parse(localStorage.getItem('chronoCompassEntries'));
    expect(updatedStoredEntries).toHaveLength(2);
    expect(updatedStoredEntries[1]).toEqual({
      energy: 3,
      focus: 4,
      timeSpeed: 2,
      timestamp: MOCK_DATE_PLUS_HOUR.toISOString(),
    });
  });

  test('ChronoChart receives correct data props', async () => {
    const mockAddEntry = jest.fn();
    const mockChartData = {
      labels: ['10:00'],
      datasets: [
        { label: 'Average Energy', data: [8] },
        { label: 'Average Focus', data: [7] },
        { label: 'Average Perceived Time Speed', data: [6] }
      ]
    };

    // Render App, add an entry, then check if ChronoChart was called with correct data
    render(<App />);

    const energySlider = screen.getByLabelText(/Energy Level:/i);
    const focusSlider = screen.getByLabelText(/Focus Level:/i);
    const timeSpeedSlider = screen.getByLabelText(/Perceived Time Speed:/i);
    const logButton = screen.getByRole('button', { name: /Log Entry/i });

    fireEvent.change(energySlider, { target: { value: '8' } });
    fireEvent.change(focusSlider, { target: { value: '7' } });
    fireEvent.change(timeSpeedSlider, { target: { value: '6' } });
    await userEvent.click(logButton);

    await waitFor(() => {
      // Check if the mocked Line component (from react-chartjs-2) was called
      // This implicitly checks if ChronoChart was rendered with the data
      const LineComponent = require('react-chartjs-2').Line;
      expect(LineComponent).toHaveBeenCalledTimes(1);
      const { data } = LineComponent.mock.calls[0][0];

      // Verify the structure and content of the data passed to the chart
      expect(data.labels).toEqual(expect.arrayContaining(Array.from({ length: 24 }, (_, i) => `${i}:00`)));
      expect(data.datasets).toHaveLength(3);
      expect(data.datasets[0].label).toBe('Average Energy');
      expect(data.datasets[0].data[10]).toBe(8); // Entry at 10:00
      expect(data.datasets[1].label).toBe('Average Focus');
      expect(data.datasets[1].data[10]).toBe(7);
      expect(data.datasets[2].label).toBe('Average Perceived Time Speed');
      expect(data.datasets[2].data[10]).toBe(6);
    });
  });

  test('loads entries from localStorage on initial render', () => {
    // # Mock rationale: localStorage is a browser API. Mocking it ensures that
    // # tests are deterministic and don't rely on actual browser storage state.
    localStorage.setItem('chronoCompassEntries', JSON.stringify([
      { energy: 9, focus: 8, timeSpeed: 7, timestamp: '2023-10-27T09:00:00.000Z' }
    ]));

    render(<App />);

    // Expect the chart to be rendered immediately with the loaded data
    expect(screen.queryByText(/Log some entries to see your temporal patterns!/i)).not.toBeInTheDocument();
    expect(screen.getByText(/Temporal Patterns/i)).toBeInTheDocument();

    const LineComponent = require('react-chartjs-2').Line;
    expect(LineComponent).toHaveBeenCalledTimes(1);
    const { data } = LineComponent.mock.calls[0][0];
    expect(data.datasets[0].data[9]).toBe(9); // Entry at 09:00
  });
});
