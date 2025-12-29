import React from 'react';
import { render, screen, act } from '@testing-library/react';
import App from '../src/App';

// Mock the setInterval and clearInterval to control time in tests
jest.useFakeTimers();

describe('App Component', () => {
  test('renders without crashing', () => {
    render(<App />);
    expect(screen.getByText(/Apocalypse Dashboard/i)).toBeInTheDocument();
  });

  test('displays initial dashboard sections', () => {
    render(<App />);
    expect(screen.getByText(/Resource Availability/i)).toBeInTheDocument();
    expect(screen.getByText(/Global Threat Level/i)).toBeInTheDocument();
    expect(screen.getByText(/Safe Zone Status/i)).toBeInTheDocument();
    expect(screen.getByText(/Whispers of the Void/i)).toBeInTheDocument();
  });

  test('updates data periodically', () => {
    render(<App />);

    // Mock the data generation functions to ensure deterministic output for testing
    const mockResourceData = [
      { name: 'Water', value: 75 },
      { name: 'Food', value: 60 },
      { name: 'Medicine', value: 90 },
      { name: 'Fuel', value: 45 },
    ];
    const mockThreatLevel = 'High';
    const mockSafeZones = [
      { name: 'Haven Alpha', population: 4500 },
      { name: 'Sanctuary Beta', population: 2800 },
    ];
    const mockVoidWhispers = [
      "Mock whisper 1",
      "Mock whisper 2",
    ];

    // Spy on the internal functions and provide mock return values
    const generateResourceDataSpy = jest.spyOn(global, 'generateResourceData').mockReturnValue(mockResourceData);
    const generateThreatLevelSpy = jest.spyOn(global, 'generateThreatLevel').mockReturnValue(mockThreatLevel);
    const generateSafeZonesSpy = jest.spyOn(global, 'generateSafeZones').mockReturnValue(mockSafeZones);
    const generateVoidWhispersSpy = jest.spyOn(global, 'generateVoidWhispers').mockReturnValue(mockVoidWhispers[0]); // Mock one at a time for simplicity

    // Advance timers by the interval duration to trigger the update
    act(() => {
      jest.advanceTimersByTime(15000);
    });

    // Check if the mock data is rendered
    expect(screen.getByText(/Water/i)).toBeInTheDocument();
    expect(screen.getByText(/75%/i)).toBeInTheDocument();
    expect(screen.getByText(/High/i)).toBeInTheDocument();
    expect(screen.getByText(/Haven Alpha/i)).toBeInTheDocument();
    expect(screen.getByText(/4,500/i)).toBeInTheDocument();
    expect(screen.getByText(/- Mock whisper 1/i)).toBeInTheDocument();

    // Restore original implementations
    generateResourceDataSpy.mockRestore();
    generateThreatLevelSpy.mockRestore();
    generateSafeZonesSpy.mockRestore();
    generateVoidWhispersSpy.mockRestore();
  });

  // Mock rationale: These are internal helper functions that are not directly exported or intended for external use. 
  // We mock them here to ensure deterministic test results and isolate the App component's logic.
  // In a real-world scenario, these might be imported from a separate utility file.
  const originalGenerateResourceData = global.generateResourceData;
  const originalGenerateThreatLevel = global.generateThreatLevel;
  const originalGenerateSafeZones = global.generateSafeZones;
  const originalGenerateVoidWhispers = global.generateVoidWhispers;

  beforeAll(() => {
    global.generateResourceData = () => [
      { name: 'Water', value: 50 },
      { name: 'Food', value: 50 },
      { name: 'Medicine', value: 50 },
      { name: 'Fuel', value: 50 },
    ];
    global.generateThreatLevel = () => 'Medium';
    global.generateSafeZones = () => [
      { name: 'Safe Haven', population: 1000 },
    ];
    global.generateVoidWhispers = () => "A test whisper.";
  });

  afterAll(() => {
    global.generateResourceData = originalGenerateResourceData;
    global.generateThreatLevel = originalGenerateThreatLevel;
    global.generateSafeZones = originalGenerateSafeZones;
    global.generateVoidWhispers = originalGenerateVoidWhispers;
  });
});
