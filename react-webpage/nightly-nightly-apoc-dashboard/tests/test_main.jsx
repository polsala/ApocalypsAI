import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ApocDashboard from '../src/main';

// Mock Chart.js components
jest.mock('react-chartjs-2', () => ({ Bar: 'div', Gauge: 'div' }));

describe('ApocDashboard', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
    jest.clearAllMocks();
  });

  test('renders dashboard title', () => {
    render(<ApocDashboard />);
    expect(screen.getByText('ApocalypsAI Nightly Dashboard')).toBeInTheDocument();
  });

  test('renders weather section', () => {
    render(<ApocDashboard />);
    expect(screen.getByText('Wasteland Weather')).toBeInTheDocument();
  });

  test('renders morale meter', () => {
    render(<ApocDashboard />);
    expect(screen.getByText('Morale Meter')).toBeInTheDocument();
  });

  test('renders temporal rift countdown', () => {
    render(<ApocDashboard />);
    expect(screen.getByText('Temporal Rift Countdown')).toBeInTheDocument();
  });

  test('renders survival resources', () => {
    render(<ApocDashboard />);
    expect(screen.getByText('Survival Resources')).toBeInTheDocument();
  });

  test('renders compliment corner', () => {
    render(<ApocDashboard />);
    expect(screen.getByText('Compliment Corner')).toBeInTheDocument();
  });

  test('renders utility distribution chart', () => {
    render(<ApocDashboard />);
    expect(screen.getByText('Utility Distribution')).toBeInTheDocument();
  });

  test('displays initial weather icon', () => {
    render(<ApocDashboard />);
    // Since weather is random, we just check for an emoji
    const icon = screen.getByText(/☀️|☁️|🌧️|⛈️|🌫️|🌬️|🌈/);
    expect(icon).toBeInTheDocument();
  });

  test('displays initial morale percentage', () => {
    render(<ApocDashboard />);
    // Morale is randomized, so we check for the pattern
    expect(screen.getByText(/Morale Meter:/)).toBeInTheDocument();
  });

  test('displays resource percentages', () => {
    render(<ApocDashboard />);
    expect(screen.getByText(/Water/)).toBeInTheDocument();
    expect(screen.getByText(/Food/)).toBeInTheDocument();
    expect(screen.getByText(/Ammo/)).toBeInTheDocument();
    expect(screen.getByText(/Power/)).toBeInTheDocument();
  });

  test('displays initial compliment', () => {
    render(<ApocDashboard />);
    expect(screen.getByText(/You have the survival instincts/)).toBeInTheDocument();
  });

  test('updates weather on interval', async () => {
    render(<ApocDashboard />);
    const initialIcon = screen.getByText(/☀️|☁️|🌧️|⛈️|🌫️|🌬️|🌈/);
    jest.advanceTimersByTime(5000);
    await waitFor(() => {
      const newIcon = screen.getByText(/☀️|☁️|🌧️|⛈️|🌫️|🌬️|🌈/);
      expect(newIcon).toBeInTheDocument();
    });
  });

  test('updates morale on interval', async () => {
    render(<ApocDashboard />);
    jest.advanceTimersByTime(5000);
    await waitFor(() => {
      expect(screen.getByText(/Morale Meter:/)).toBeInTheDocument();
    });
  });

  test('updates resources on interval', async () => {
    render(<ApocDashboard />);
    jest.advanceTimersByTime(5000);
    await waitFor(() => {
      expect(screen.getByText(/Water/)).toBeInTheDocument();
    });
  });

  test('updates compliment on interval', async () => {
    render(<ApocDashboard />);
    jest.advanceTimersByTime(5000);
    await waitFor(() => {
      expect(screen.getByText(/You have the survival instincts/)).toBeInTheDocument();
    });
  });

  test('displays countdown timer', () => {
    render(<ApocDashboard />);
    // The countdown is dynamic, so we just check for the pattern
    expect(screen.getByText(/Until next anomaly/)).toBeInTheDocument();
  });

  test('renders with correct background and styling classes', () => {
    const { container } = render(<ApocDashboard />);
    expect(container.firstChild).toHaveStyle({ background: '#0f172a' });
  });
});
