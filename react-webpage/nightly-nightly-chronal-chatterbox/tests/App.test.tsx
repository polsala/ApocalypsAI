import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../src/App';
import * as EchoGenerator from '../src/EchoGenerator';

// Mock rationale: We need to control time-based operations (setInterval, setTimeout) to make tests deterministic.
// We also mock the EchoGenerator to provide predictable echo messages for assertions.

const mockGenerateEcho = vi.spyOn(EchoGenerator, 'generateEcho');

describe('App', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    mockGenerateEcho.mockImplementation((frequency: string) => ({
      id: `mock-echo-${Date.now()}`,
      message: `Mock Echo for ${frequency}`,
      frequency,
      timestamp: Date.now(),
    }));
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });

  it('renders the main title and frequency selector', () => {
    render(<App />);
    expect(screen.getByText('Chronal Chatterbox')).toBeInTheDocument();
    expect(screen.getByLabelText('Tune Frequency:')).toBeInTheDocument();
    expect(screen.getByRole('combobox')).toBeInTheDocument();
  });

  it('displays initial frequency as Whimsical Wisdom', () => {
    render(<App />);
    const selectElement = screen.getByRole('combobox') as HTMLSelectElement;
    expect(selectElement.value).toBe('Whimsical Wisdom');
  });

  it('generates and displays an echo after an interval', async () => {
    render(<App />);

    // Advance timers by 2 seconds to trigger the first echo generation
    vi.advanceTimersByTime(2000);

    await waitFor(() => {
      expect(mockGenerateEcho).toHaveBeenCalledWith('Whimsical Wisdom');
      expect(screen.getByText('Mock Echo for Whimsical Wisdom')).toBeInTheDocument();
    });
  });

  it('changes frequency when selected from the dropdown', async () => {
    render(<App />);
    const selectElement = screen.getByRole('combobox');

    fireEvent.change(selectElement, { target: { value: 'Temporal Trivia' } });

    expect(selectElement).toHaveValue('Temporal Trivia');

    // Advance timers to trigger echo generation with the new frequency
    vi.advanceTimersByTime(2000);

    await waitFor(() => {
      expect(mockGenerateEcho).toHaveBeenCalledWith('Temporal Trivia');
      expect(screen.getByText('Mock Echo for Temporal Trivia')).toBeInTheDocument();
    });
  });

  it('removes echoes after they fade out', async () => {
    render(<App />);

    // Trigger first echo
    vi.advanceTimersByTime(2000);
    await waitFor(() => {
      expect(screen.getByText('Mock Echo for Whimsical Wisdom')).toBeInTheDocument();
    });

    // Advance timers past the fade duration (initialDelay + fadeDuration from EchoDisplay.tsx)
    // EchoDisplay has initialDelay = 1000ms, fadeDuration = 5000ms. So total 6000ms from echo creation.
    // App creates echo every 2000ms. So, after 2000ms, echo is created. After another 6000ms, it should be gone.
    // Total 8000ms from app start.
    vi.advanceTimersByTime(6000); // 2000 (creation) + 6000 (fade out) = 8000

    await waitFor(() => {
      expect(screen.queryByText('Mock Echo for Whimsical Wisdom')).not.toBeInTheDocument();
    }, { timeout: 100 }); // Small timeout for waitFor to check DOM updates
  });
});
