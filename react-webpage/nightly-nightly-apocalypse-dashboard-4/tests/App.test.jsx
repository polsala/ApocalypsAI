import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Mocking the components to isolate App's rendering logic
jest.mock('../src/components/ResourceTracker', () => () => <div>Mock ResourceTracker</div>);
jest.mock('../src/components/ThreatLevel', () => () => <div>Mock ThreatLevel</div>);
jest.mock('../src/components/SafeZones', () => () => <div>Mock SafeZones</div>);
jest.mock('../src/components/WhispersOfTheVoid', () => () => <div>Mock WhispersOfTheVoid</div>);
jest.mock('../src/components/TemporalAnomalyWatch', () => () => <div>Mock TemporalAnomalyWatch</div>);

// Mocking useEffect to prevent actual data fetching and ensure deterministic tests
const mockUseEffect = jest.spyOn(React, 'useEffect');

describe('App Component', () => {
  beforeEach(() => {
    // Reset mocks before each test
    mockUseEffect.mockClear();
    // Mock useEffect to do nothing, as the actual data fetching is mocked
    mockUseEffect.mockImplementation(f => f());
  });

  afterAll(() => {
    // Restore original useEffect after all tests
    mockUseEffect.mockRestore();
  });

  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Apocalypse Dashboard/i)).toBeInTheDocument();
  });

  test('renders all dashboard components', () => {
    render(<App />);
    expect(screen.getByText(/Mock ResourceTracker/i)).toBeInTheDocument();
    expect(screen.getByText(/Mock ThreatLevel/i)).toBeInTheDocument();
    expect(screen.getByText(/Mock SafeZones/i)).toBeInTheDocument();
    expect(screen.getByText(/Mock WhispersOfTheVoid/i)).toBeInTheDocument();
    expect(screen.getByText(/Mock TemporalAnomalyWatch/i)).toBeInTheDocument();
  });

  test('useEffect is called once on mount', () => {
    render(<App />);
    expect(mockUseEffect).toHaveBeenCalledTimes(1);
  });
});
