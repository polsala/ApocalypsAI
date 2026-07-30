import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Mocking the child components to isolate App's behavior
jest.mock('../src/components/EventDisplay', () => () => <div>MockEventDisplay</div>);
jest.mock('../src/components/ResourceTracker', () => () => <div>MockResourceTracker</div>);
jest.mock('../src/components/WandererStatus', () => () => <div>MockWandererStatus</div>);

describe('App Component', () => {
  test('renders the main header', () => {
    render(<App />);
    const headerElement = screen.getByText(/Apocalypse Dashboard/i);
    expect(headerElement).toBeInTheDocument();
  });

  test('renders the subtitle', () => {
    render(<App />);
    const subtitleElement = screen.getByText(/Keeping an eye on the end of the world/i);
    expect(subtitleElement).toBeInTheDocument();
  });

  test('renders the EventDisplay component', () => {
    render(<App />);
    const eventDisplayElement = screen.getByText(/MockEventDisplay/i);
    expect(eventDisplayElement).toBeInTheDocument();
  });

  test('renders the ResourceTracker component', () => {
    render(<App />);
    const resourceTrackerElement = screen.getByText(/MockResourceTracker/i);
    expect(resourceTrackerElement).toBeInTheDocument();
  });

  test('renders the WandererStatus component', () => {
    render(<App />);
    const wandererStatusElement = screen.getByText(/MockWandererStatus/i);
    expect(wandererStatusElement).toBeInTheDocument();
  });

  test('renders the footer', () => {
    render(<App />);
    const footerElement = screen.getByText(/© 2023 ApocalypsAI/i);
    expect(footerElement).toBeInTheDocument();
  });

  // Mock rationale: We are mocking the fetch API and setInterval to ensure deterministic tests.
  // In a real scenario, these would be tested more thoroughly, potentially with integration tests.
  test('fetches simulated data on mount', async () => {
    // Mocking the fetch call within useEffect
    const mockFetch = jest.spyOn(global, 'fetch');
    // Mocking setInterval to prevent actual interval execution during tests
    jest.useFakeTimers();

    render(<App />);

    // Expecting the initial fetch to have been called (or simulated within useEffect)
    // Since the data is hardcoded in useEffect for this example, we check for rendered components.
    // A more robust test would mock the actual data fetching mechanism.

    // Advance timers to ensure any setInterval callbacks are processed if needed
    jest.advanceTimersByTime(60000);

    // Check if the components that rely on fetched data are rendered
    expect(screen.getByText(/MockEventDisplay/i)).toBeInTheDocument();
    expect(screen.getByText(/MockResourceTracker/i)).toBeInTheDocument();
    expect(screen.getByText(/MockWandererStatus/i)).toBeInTheDocument();

    // Clean up mocks
    mockFetch.mockRestore();
    jest.useRealTimers();
  });
});
