import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import CosmicCompass from '../src/main.jsx';

// Mock the geolocation API
// Mock rationale: The geolocation API is asynchronous and depends on user permission,
// making it unsuitable for deterministic, offline testing. We mock it to control its behavior.
const mockGeolocation = {
  getCurrentPosition: jest.fn()
};

const setupGeolocationMock = (position = { latitude: 40.7128, longitude: -74.0060 }, error = null) => {
  mockGeolocation.getCurrentPosition.mockImplementation((success, failure) => {
    if (error) {
      failure({ message: error });
    } else {
      success({
        coords: {
          latitude: position.latitude,
          longitude: position.longitude
        }
      });
    }
  });
  Object.defineProperty(navigator, 'geolocation', {
    value: mockGeolocation
  });
};

// Mock Leaflet's MapContainer and TileLayer to avoid rendering actual map components
// Mock rationale: Rendering actual map components requires complex setup and external dependencies
// that are not suitable for isolated unit tests. We replace them with simple divs.
jest.mock('react-leaflet', () => ({
  MapContainer: ({ children }) => <div data-testid="mock-map-container">{children}</div>,
  TileLayer: () => <div data-testid="mock-tile-layer"></div>,
  Marker: ({ children }) => <div data-testid="mock-marker">{children}</div>,
  Popup: ({ children }) => <div data-testid="mock-popup">{children}</div>,
}));

// Mock L.Icon.Default to prevent errors related to missing icon URLs
// Mock rationale: Leaflet's default icons require image files which are not bundled
// in this self-contained utility. This mock ensures the component renders without errors.
jest.mock('leaflet', () => ({
  ...jest.requireActual('leaflet'), // Keep other Leaflet exports
  Icon: {
    Default: {
      mergeTo: jest.fn(),
      prototype: {
        _getIconUrl: jest.fn()
      }
    }
  }
}));

describe('CosmicCompass', () => {
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
    // Ensure navigator.geolocation is reset if it was modified
    delete navigator.geolocation;
  });

  it('renders the main title and subtitle', () => {
    setupGeolocationMock();
    render(<CosmicCompass />);
    expect(screen.getByText('Cosmic Compass')).toBeInTheDocument();
    expect(screen.getByText('Your whimsical guide to the universe, starting from your current location.')).toBeInTheDocument();
  });

  it('displays loading message while fetching location', () => {
    setupGeolocationMock();
    render(<CosmicCompass />);
    expect(screen.getByText('Loading cosmic coordinates...')).toBeInTheDocument();
  });

  it('renders the map with user position after geolocation succeeds', async () => {
    const userPosition = { latitude: 34.0522, longitude: -118.2437 };
    setupGeolocationMock(userPosition);
    render(<CosmicCompass />);

    // Wait for the geolocation to be processed and the map to potentially render
    await waitFor(() => {
      expect(screen.getByTestId('mock-map-container')).toBeInTheDocument();
      // We can't directly assert the center of the map with our mock, but we can check for its presence.
      // We can also check if the mock marker for the user's position is rendered.
      expect(screen.getAllByTestId('mock-marker')).toHaveLength(1 + mockCelestialBodies.length + mockAlienCivilizations.length); // User + bodies + civs
    });
  });

  it('falls back to a default location if geolocation is not supported', () => {
    Object.defineProperty(navigator, 'geolocation', {
      value: undefined // Simulate no geolocation support
    });
    render(<CosmicCompass />);

    // Wait for the fallback to occur
    return waitFor(() => {
      expect(screen.getByText('Error: Geolocation is not supported by your browser.')).toBeInTheDocument();
      expect(screen.getByTestId('mock-map-container')).toBeInTheDocument();
      // Check if the default marker is rendered (we can't directly check center with mock)
      expect(screen.getAllByTestId('mock-marker')).toHaveLength(1 + mockCelestialBodies.length + mockAlienCivilizations.length); // Default + bodies + civs
    });
  });

  it('falls back to a default location if geolocation fails with an error', async () => {
    const geoError = 'Permission denied';
    setupGeolocationMock({ latitude: 0, longitude: 0 }, geoError);
    render(<CosmicCompass />);

    await waitFor(() => {
      expect(screen.getByText(`Error: ${geoError}`)).toBeInTheDocument();
      expect(screen.getByTestId('mock-map-container')).toBeInTheDocument();
      // Check if the default marker is rendered
      expect(screen.getAllByTestId('mock-marker')).toHaveLength(1 + mockCelestialBodies.length + mockAlienCivilizations.length); // Default + bodies + civs
    });
  });

  it('renders mock celestial bodies and alien civilizations', async () => {
    setupGeolocationMock();
    render(<CosmicCompass />);

    await waitFor(() => {
      expect(screen.getByTestId('mock-map-container')).toBeInTheDocument();
      // Check for presence of mock data in popups
      expect(screen.getByText('Nebula of Whispers')).toBeInTheDocument();
      expect(screen.getByText('Xylos Prime')).toBeInTheDocument();
      expect(screen.getByText('Zorpian Outpost')).toBeInTheDocument();
      expect(screen.getByText('Gleep Glorp Colony')).toBeInTheDocument();
    });
  });
});
