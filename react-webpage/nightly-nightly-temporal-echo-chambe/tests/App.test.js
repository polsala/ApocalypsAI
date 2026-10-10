import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../src/App';
import * as localStorageService from '../src/data/localStorageService'; // Import the service to mock it

// Mock rationale: localStorage is a browser-specific API and not available in a Node.js test environment.
// Mocking it allows for deterministic, offline testing of the utility functions without a real browser.
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: jest.fn((key) => store[key] || null),
    setItem: jest.fn((key, value) => {
      store[key] = value.toString();
    }),
    clear: jest.fn(() => {
      store = {};
    }),
    removeItem: jest.fn((key) => {
      delete store[key];
    }),
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('App', () => {
  beforeEach(() => {
    localStorageMock.clear();
    localStorageMock.getItem.mockClear();
    localStorageMock.setItem.mockClear();
    // Mock rationale: Date.now() is used to generate a unique ID. Mocking it ensures deterministic IDs for testing.
    jest.spyOn(Date, 'now').mockReturnValue(1234567890);
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Chamber Visualizer/i)).toBeInTheDocument();
  });

  it('loads anomalies from local storage on startup', async () => {
    const mockAnomalies = [
      { id: 1, description: 'Loaded Anomaly 1', timestamp: '2024-01-01T12:00', type: 'Visual Glitch', energyLevel: 5 },
      { id: 2, description: 'Loaded Anomaly 2', timestamp: '2024-01-02T12:00', type: 'Auditory Echo', energyLevel: 7 },
    ];
    localStorageMock.setItem('temporalAnomalies', JSON.stringify(mockAnomalies));

    render(<App />);

    await waitFor(() => {
      expect(localStorageMock.getItem).toHaveBeenCalledWith('temporalAnomalies');
      expect(screen.getByText(/Loaded Anomaly 1/i)).toBeInTheDocument();
      expect(screen.getByText(/Loaded Anomaly 2/i)).toBeInTheDocument();
    });
  });

  it('adds a new anomaly and saves it to local storage', async () => {
    render(<App />);

    fireEvent.change(screen.getByLabelText(/Description:/i), {
      target: { value: 'New Test Anomaly' },
    });
    fireEvent.change(screen.getByLabelText(/Timestamp:/i), {
      target: { value: '2024-10-27T11:00' },
    });
    fireEvent.change(screen.getByLabelText(/Anomaly Type:/i), {
      target: { value: 'Object Displacement' },
    });
    fireEvent.change(screen.getByLabelText(/Temporal Energy Level \(1-10\):/i), {
      target: { value: '8' },
    });

    fireEvent.click(screen.getByRole('button', { name: /Add Anomaly/i }));

    await waitFor(() => {
      expect(screen.getByText(/New Test Anomaly/i)).toBeInTheDocument();
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'temporalAnomalies',
        JSON.stringify([
          {
            id: 1234567890,
            description: 'New Test Anomaly',
            timestamp: '2024-10-27T11:00',
            type: 'Object Displacement',
            energyLevel: 8,
          },
        ])
      );
    });
  });

  it('displays "No anomalies logged yet" when no anomalies are present', () => {
    render(<App />);
    expect(screen.getByText(/No anomalies logged yet./i)).toBeInTheDocument();
  });

  it('sorts anomalies by timestamp in the display', async () => {
    const mockAnomalies = [
      { id: 1, description: 'Later Anomaly', timestamp: '2024-01-02T12:00', type: 'Visual Glitch', energyLevel: 5 },
      { id: 2, description: 'Earlier Anomaly', timestamp: '2024-01-01T12:00', type: 'Auditory Echo', energyLevel: 7 },
    ];
    localStorageMock.setItem('temporalAnomalies', JSON.stringify(mockAnomalies));

    render(<App />);

    await waitFor(() => {
      const anomalyItems = screen.getAllByRole('listitem');
      expect(anomalyItems[0]).toHaveTextContent(/Earlier Anomaly/i);
      expect(anomalyItems[1]).toHaveTextContent(/Later Anomaly/i);
    });
  });
});
