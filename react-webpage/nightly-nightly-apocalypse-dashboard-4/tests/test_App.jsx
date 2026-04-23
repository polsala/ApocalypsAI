import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Mock the window.apocalypseData object before each test
const mockApocalypseData = {
  resources: [
    { name: 'Canned Beans', quantity: 500, unit: 'cans' },
    { name: 'Clean Water', quantity: 1000, unit: 'liters' }
  ],
  threatLevel: { level: 8, description: 'High mutant activity!' },
  safeZones: [
    { name: 'Fortress Alpha', status: 'Secure', capacity: 200 },
    { name: 'Underground Bunker 7', status: 'Compromised', capacity: 50 }
  ],
  voidWhispers: 'The end is nigh.'
};

// Mock rationale: We are mocking the global `window.apocalypseData` object
// because the App component directly accesses it. This allows us to control
// the data and ensure deterministic tests without relying on external state
// or complex setup for data generation.
Object.defineProperty(window, 'apocalypseData', {
  value: mockApocalypseData,
  writable: true
});

describe('App Component', () => {
  it('renders the main title', () => {
    render(<App />);
    expect(screen.getByText('Apocalypse Dashboard')).toBeInTheDocument();
  });

  it('renders ResourceTracker with mock data', () => {
    render(<App />);
    expect(screen.getByText('Resource Tracker')).toBeInTheDocument();
    expect(screen.getByText('Canned Beans')).toBeInTheDocument();
    expect(screen.getByText('500 cans')).toBeInTheDocument();
    expect(screen.getByText('Clean Water')).toBeInTheDocument();
    expect(screen.getByText('1000 liters')).toBeInTheDocument();
  });

  it('renders ThreatLevelMonitor with mock data', () => {
    render(<App />);
    expect(screen.getByText('Threat Level Monitor')).toBeInTheDocument();
    expect(screen.getByText('8')).toBeInTheDocument();
    expect(screen.getByText('High mutant activity!')).toBeInTheDocument();
  });

  it('renders SafeZoneStatus with mock data', () => {
    render(<App />);
    expect(screen.getByText('Safe Zone Status')).toBeInTheDocument();
    expect(screen.getByText('Fortress Alpha')).toBeInTheDocument();
    expect(screen.getByText('Secure')).toBeInTheDocument();
    expect(screen.getByText('Underground Bunker 7')).toBeInTheDocument();
    expect(screen.getByText('Compromised')).toBeInTheDocument();
  });

  it('renders VoidWhispers with mock data', () => {
    render(<App />);
    expect(screen.getByText('Whispers of the Void')).toBeInTheDocument();
    expect(screen.getByText('The end is nigh.')).toBeInTheDocument();
  });

  it('renders fallback messages when no data is available', () => {
    // Mock rationale: Temporarily set window.apocalypseData to null or empty
    // to test the fallback rendering logic in the components.
    window.apocalypseData = null;
    render(<App />);

    expect(screen.getByText('Resource Tracker')).toBeInTheDocument();
    expect(screen.getByText('No resource data available. The pantry is bare...')).toBeInTheDocument();

    expect(screen.getByText('Threat Level Monitor')).toBeInTheDocument();
    expect(screen.getByText('Unknown threat level.')).toBeInTheDocument();

    expect(screen.getByText('Safe Zone Status')).toBeInTheDocument();
    expect(screen.getByText('No safe zones identified. The world is a wasteland...')).toBeInTheDocument();

    expect(screen.getByText('Whispers of the Void')).toBeInTheDocument();
    expect(screen.getByText('The void is silent...')).toBeInTheDocument();
  });
});
