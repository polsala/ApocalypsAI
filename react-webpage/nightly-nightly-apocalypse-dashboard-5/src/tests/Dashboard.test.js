import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Dashboard from '../components/Dashboard';
import * as mockApi from '../utils/mockApi';

// Mocking the entire module
jest.mock('../utils/mockApi');

describe('Dashboard Component', () => {
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();

    // Mocking the API calls to return deterministic data
    mockApi.fetchResources.mockResolvedValue({
      cannedGoods: 500,
      cleanWater: 250,
      ammo: 100,
      medicalSupplies: 150
    });
    mockApi.fetchSurvivalOdds.mockResolvedValue(75);
    mockApi.fetchThreatLevel.mockResolvedValue('medium');
    mockApi.fetchAlerts.mockResolvedValue('Mock alert message.');

    // Mocking setInterval and clearInterval to prevent actual timers
    jest.useFakeTimers();
  });

  test('renders loading state initially', () => {
    render(<Dashboard />);
    expect(screen.getByText(/Scavenging for supplies.../i)).toBeInTheDocument();
    expect(screen.getByText(/Calculating probabilities.../i)).toBeInTheDocument();
    expect(screen.getByText(/Assessing environment.../i)).toBeInTheDocument();
    expect(screen.getByText(/Listening for cosmic murmurs.../i)).toBeInTheDocument();
  });

  test('renders dashboard data after loading', async () => {
    render(<Dashboard />);

    // Advance timers to allow useEffect to run and mock API calls to resolve
    jest.advanceTimersByTime(1000); // Advance past the initial setTimeout in mockApi

    await waitFor(() => {
      expect(screen.getByText(/Canned Goods: 500/i)).toBeInTheDocument();
      expect(screen.getByText(/Clean Water: 250/i)).toBeInTheDocument();
      expect(screen.getByText(/Ammunition: 100/i)).toBeInTheDocument();
      expect(screen.getByText(/Medical Supplies: 150/i)).toBeInTheDocument();
      expect(screen.getByText(/75%/i)).toBeInTheDocument();
      expect(screen.getByText(/MEDIUM/i)).toBeInTheDocument();
      expect(screen.getByText(/Mock alert message./i)).toBeInTheDocument();
    });
  });

  test('calls API functions correctly', async () => {
    render(<Dashboard />);
    jest.advanceTimersByTime(1000);

    await waitFor(() => {
      expect(mockApi.fetchResources).toHaveBeenCalledTimes(1);
      expect(mockApi.fetchSurvivalOdds).toHaveBeenCalledTimes(1);
      expect(mockApi.fetchThreatLevel).toHaveBeenCalledTimes(1);
      expect(mockApi.fetchAlerts).toHaveBeenCalledTimes(1);
    });
  });

  test('refreshes data periodically', async () => {
    render(<Dashboard />);
    jest.advanceTimersByTime(1000);

    await waitFor(() => {
      expect(mockApi.fetchResources).toHaveBeenCalledTimes(1);
    });

    // Advance timers by the interval duration (15 seconds)
    jest.advanceTimersByTime(15000);

    await waitFor(() => {
      // Expecting the API calls to have been made again
      expect(mockApi.fetchResources).toHaveBeenCalledTimes(2);
      expect(mockApi.fetchSurvivalOdds).toHaveBeenCalledTimes(2);
      expect(mockApi.fetchThreatLevel).toHaveBeenCalledTimes(2);
      expect(mockApi.fetchAlerts).toHaveBeenCalledTimes(2);
    });
  });

  test('handles API errors gracefully', async () => {
    // Mock one of the API calls to reject
    mockApi.fetchResources.mockRejectedValue(new Error('Network error'));

    render(<Dashboard />);
    jest.advanceTimersByTime(1000);

    await waitFor(() => {
      expect(screen.getByText(/Failed to load critical survival data. Improvise!/i)).toBeInTheDocument();
      // Ensure other components still show loading or default states if possible
      expect(screen.queryByText(/Canned Goods:/i)).not.toBeInTheDocument();
    });
  });

  test('renders correct threat level class', async () => {
    mockApi.fetchThreatLevel.mockResolvedValue('low');
    render(<Dashboard />);
    jest.advanceTimersByTime(1000);
    await waitFor(() => {
      const threatElement = screen.getByText(/LOW/i).parentElement;
      expect(threatElement).toHaveClass('threat-low');
    });

    mockApi.fetchThreatLevel.mockResolvedValue('high');
    // Re-render or update state if necessary, but for simplicity, we'll assume a new render context
    // In a real app, you might trigger a re-fetch or state update
    // For this test, we'll just check the class for 'high'
    render(<Dashboard />); // Re-render to pick up new mock
    jest.advanceTimersByTime(1000);
    await waitFor(() => {
      const threatElement = screen.getByText(/HIGH/i).parentElement;
      expect(threatElement).toHaveClass('threat-high');
    });
  });
});
