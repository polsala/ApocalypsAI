import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import App from '../src/App';

// Mock the Geolocation API
const mockGeolocation = {
  getCurrentPosition: jest.fn(),
};

const setupGeolocation = (coords = { latitude: 34.0522, longitude: -118.2437 }) => {
  mockGeolocation.getCurrentPosition.mockImplementation((successCallback) => {
    successCallback({ coords });
  });
  Object.defineProperty(navigator, 'geolocation', {
    value: mockGeolocation,
  });
};

const teardownGeolocation = () => {
  delete navigator.geolocation;
};

describe('App Component', () => {
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
    // Set up a default mock location
    setupGeolocation();
  });

  afterEach(() => {
    // Clean up mock geolocation after each test
    teardownGeolocation();
  });

  test('renders without crashing and displays loading state', () => {
    render(<App />);
    expect(screen.getByText(/Locating your position.../i)).toBeInTheDocument();
    expect(screen.getByText(/Mapping the cosmos.../i)).toBeInTheDocument();
  });

  test('displays user location and celestial info after geolocation succeeds', async () => {
    const mockCoords = { latitude: 40.7128, longitude: -74.0060 }; // New York
    setupGeolocation(mockCoords);

    render(<App />);

    // Wait for the location and celestial info to be displayed
    await waitFor(() => {
      expect(screen.getByText(/Latitude: 40.7128, Longitude: -74.0060/i)).toBeInTheDocument();
    });

    // Check for presence of celestial info (specific star/constellation will vary due to mock randomness)
    expect(screen.getByText(/Prominent Star:/i)).toBeInTheDocument();
    expect(screen.getByText(/Visible Constellation:/i)).toBeInTheDocument();
    expect(screen.getByText(/Wasteland Wisdom:/i)).toBeInTheDocument();
  });

  test('falls back to mock location if geolocation is not supported', () => {
    // Mock navigator.geolocation to be undefined
    Object.defineProperty(navigator, 'geolocation', {
      value: undefined,
    });

    render(<App />);

    // Check if it uses the default mock location
    expect(screen.getByText(/Latitude: 34.0522, Longitude: -118.2437/i)).toBeInTheDocument();
  });

  test('falls back to mock location if geolocation fails', async () => {
    mockGeolocation.getCurrentPosition.mockImplementation((successCallback, errorCallback) => {
      errorCallback(new Error('Permission denied'));
    });
    Object.defineProperty(navigator, 'geolocation', {
      value: mockGeolocation,
    });

    render(<App />);

    // Wait for the fallback location to be displayed
    await waitFor(() => {
      expect(screen.getByText(/Latitude: 34.0522, Longitude: -118.2437/i)).toBeInTheDocument();
    });
  });
});
