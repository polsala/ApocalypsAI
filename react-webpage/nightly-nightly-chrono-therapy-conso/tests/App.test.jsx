import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import App from '../src/App';

// # Mock rationale: Date.now() is used for unique IDs and timestamps. Mocking it ensures deterministic IDs for consistent test results.
const MOCK_DATE_NOW = 1678886400000; // March 15, 2023 12:00:00 PM UTC
vi.spyOn(Date, 'now').mockReturnValue(MOCK_DATE_NOW);
vi.spyOn(Date.prototype, 'toLocaleString').mockReturnValue('3/15/2023, 12:00:00 PM');

describe('App', () => {
  beforeEach(() => {
    localStorage.clear(); // Clear localStorage before each test
    vi.clearAllMocks();
    vi.spyOn(Date, 'now').mockReturnValue(MOCK_DATE_NOW);
    vi.spyOn(Date.prototype, 'toLocaleString').mockReturnValue('3/15/2023, 12:00:00 PM');
  });

  it('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Chrono-Therapy Console/i)).toBeInTheDocument();
  });

  it('allows logging a temporal distortion event', async () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Describe the temporal ripple you experienced.../i);
    const button = screen.getByRole('button', { name: /Log Event/i });

    fireEvent.change(textarea, { target: { value: 'Saw a glitch in the matrix during breakfast.' } });
    fireEvent.click(button);

    await waitFor(() => {
      expect(screen.getByText(/Saw a glitch in the matrix during breakfast./i)).toBeInTheDocument();
    });

    // Check localStorage
    const storedEvents = JSON.parse(localStorage.getItem('chronoTherapyEvents'));
    expect(storedEvents).toHaveLength(1);
    expect(storedEvents[0].description).toBe('Saw a glitch in the matrix during breakfast.');
    expect(storedEvents[0].timestamp).toBe('3/15/2023, 12:00:00 PM');
  });

  it('allows logging a mood entry', async () => {
    render(<App />);
    const moodSlider = screen.getByRole('slider', { name: /Chronological Ripple Intensity \(Mood Tracker\)/i });
    const logMoodButton = screen.getByRole('button', { name: /Log Mood/i });

    // Simulate changing mood to 7
    fireEvent.change(moodSlider, { target: { value: '7' } });
    fireEvent.click(logMoodButton);

    await waitFor(() => {
      expect(screen.getByText(/Mood: 7 🙂/i)).toBeInTheDocument();
    });

    // Check localStorage
    const storedMoods = JSON.parse(localStorage.getItem('chronoTherapyMoods'));
    expect(storedMoods).toHaveLength(1);
    expect(storedMoods[0].rating).toBe(7);
    expect(storedMoods[0].timestamp).toBe('3/15/2023, 12:00:00 PM');
  });

  it('loads events and moods from localStorage on initial render', async () => {
    // Pre-populate localStorage
    localStorage.setItem('chronoTherapyEvents', JSON.stringify([{ id: 1, description: 'Pre-loaded event', timestamp: '3/14/2023, 10:00:00 AM' }]));
    localStorage.setItem('chronoTherapyMoods', JSON.stringify([{ id: 2, rating: 6, timestamp: '3/14/2023, 11:00:00 AM' }]));

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/Pre-loaded event/i)).toBeInTheDocument();
      expect(screen.getByText(/Mood: 6 🙂/i)).toBeInTheDocument();
    });
  });

  it('displays correct emoji for different mood ratings', () => {
    render(<App />);
    const moodSlider = screen.getByRole('slider', { name: /Chronological Ripple Intensity \(Mood Tracker\)/i });
    const logMoodButton = screen.getByRole('button', { name: /Log Mood/i });

    fireEvent.change(moodSlider, { target: { value: '9' } });
    fireEvent.click(logMoodButton);
    expect(screen.getByText(/Mood: 9 😊/i)).toBeInTheDocument();

    fireEvent.change(moodSlider, { target: { value: '5' } });
    fireEvent.click(logMoodButton);
    expect(screen.getByText(/Mood: 5 😐/i)).toBeInTheDocument();

    fireEvent.change(moodSlider, { target: { value: '1' } });
    fireEvent.click(logMoodButton);
    expect(screen.getByText(/Mood: 1 😩/i)).toBeInTheDocument();
  });
});
