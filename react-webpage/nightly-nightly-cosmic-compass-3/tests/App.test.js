import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import App from '../src/App';

// Mock the Geolocation API
const mockGeolocation = {
  getCurrentPosition: jest.fn()
};

const setupGeolocationMock = (coords = { latitude: 40.7128, longitude: -74.0060 }, error = null) => {
  mockGeolocation.getCurrentPosition.mockImplementation((successCallback, errorCallback) => {
    if (error) {
      errorCallback({ message: error });
    } else {
      successCallback({ coords });
    }
  });
  Object.defineProperty(navigator, 'geolocation', {
    value: mockGeolocation,
    configurable: true
  });
};

const teardownGeolocationMock = () => {
  delete navigator.geolocation;
};

describe('App Component', () => {
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
  });

  afterEach(() => {
    // Clean up any global mocks after each test
    teardownGeolocationMock();
  });

  test('renders without crashing and shows loading message', () => {
    setupGeolocationMock(); // Mock geolocation to be available but not yet called
    render(<App />);
    expect(screen.getByText(/Locating your position in the cosmos.../i)).toBeInTheDocument();
    expect(screen.getByText(/ApocalypsAI Cosmic Compass/i)).toBeInTheDocument();
  });

  test('displays user location after successful geolocation', async () => {
    const mockCoords = { latitude: 34.0522, longitude: -118.2437 }; // Los Angeles
    setupGeolocationMock(mockCoords);

    render(<App />);

    // Wait for the geolocation to be retrieved and the location to be displayed
    await waitFor(() => {
      expect(screen.getByTitle(/Your Location: Lat 34.05, Lng -118.24/i)).toBeInTheDocument();
      expect(screen.getByText(/Locating your position in the cosmos.../i)).not.toBeInTheDocument();
    });
  });

  test('displays error message if geolocation is not supported', () => {
    // Mock navigator.geolocation to be undefined
    Object.defineProperty(navigator, 'geolocation', {
      value: undefined,
      configurable: true
    });

    render(<App />);

    expect(screen.getByText(/Geolocation is not supported by your browser./i)).toBeInTheDocument();
    expect(screen.queryByText(/Locating your position in the cosmos.../i)).not.toBeInTheDocument();
  });

  test('displays error message if getCurrentPosition fails', async () => {
    const errorMessage = 'Permission denied';
    setupGeolocationMock(null, errorMessage);

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(`Error getting location: ${errorMessage}`)).toBeInTheDocument();
      expect(screen.queryByText(/Locating your position in the cosmos.../i)).not.toBeInTheDocument();
    });
  });

  test('renders celestial bodies', () => {
    setupGeolocationMock();
    render(<App />);
    expect(screen.getByText('The Shattered Moon')).toBeInTheDocument();
    expect(screen.getByText('The Crimson Nebula')).toBeInTheDocument();
    expect(screen.getByText('The Whispering Comet')).toBeInTheDocument();
    expect(screen.getByText('The Obsidian Star')).toBeInTheDocument();
    expect(screen.getByText('The Glimmering Debris Field')).toBeInTheDocument();
  });
});
