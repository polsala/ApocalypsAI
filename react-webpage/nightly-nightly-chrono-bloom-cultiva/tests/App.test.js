import { render, screen, fireEvent, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// Mock rationale: To ensure deterministic tests for time-dependent bloom growth and visual updates,
// `jest.useFakeTimers()` is employed. This allows precise control over the passage of time,
// simulating bloom progression without actual delays and ensuring consistent test results.

describe('App', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers();
  });

  test('renders App title and initial message', () => {
    render(<App />);
    expect(screen.getByText(/Chrono-Bloom Cultivator/i)).toBeInTheDocument();
    expect(screen.getByText(/No blooms planted yet. Start cultivating!/i)).toBeInTheDocument();
  });

  test('allows adding a new bloom', () => {
    render(<App />);

    const nameInput = screen.getByLabelText(/Bloom Name/i);
    const durationInput = screen.getByLabelText(/Duration in minutes/i);
    const plantButton = screen.getByRole('button', { name: /Plant Bloom/i });

    fireEvent.change(nameInput, { target: { value: 'Test Bloom' } });
    fireEvent.change(durationInput, { target: { value: '1' } }); // 1 minute duration for easy testing
    fireEvent.click(plantButton);

    expect(screen.getByText('Test Bloom')).toBeInTheDocument();
    expect(screen.getByText('Stage: Budding')).toBeInTheDocument();
    expect(screen.getByText('0% complete')).toBeInTheDocument();
    expect(screen.queryByText(/No blooms planted yet/i)).not.toBeInTheDocument();
  });

  test('bloom progresses over time', () => {
    render(<App />);

    const nameInput = screen.getByLabelText(/Bloom Name/i);
    const durationInput = screen.getByLabelText(/Duration in minutes/i);
    const plantButton = screen.getByRole('button', { name: /Plant Bloom/i });

    fireEvent.change(nameInput, { target: { value: 'Growing Bloom' } });
    fireEvent.change(durationInput, { target: { value: '1' } }); // 1 minute = 60 seconds
    fireEvent.click(plantButton);

    expect(screen.getByText('Growing Bloom')).toBeInTheDocument();
    expect(screen.getByText('0% complete')).toBeInTheDocument();

    // Advance time by 15 seconds (25% of 60 seconds)
    act(() => {
      jest.advanceTimersByTime(15 * 1000); // 15 seconds
    });
    expect(screen.getByText('25% complete')).toBeInTheDocument();
    expect(screen.getByText('Stage: Growing')).toBeInTheDocument();

    // Advance time to 60 seconds (100%)
    act(() => {
      jest.advanceTimersByTime(45 * 1000); // Another 45 seconds
    });
    expect(screen.getByText('100% complete')).toBeInTheDocument();
    expect(screen.getByText('Stage: Full Bloom')).toBeInTheDocument();
    expect(screen.getByText('Fully bloomed!')).toBeInTheDocument();
  });

  test('allows deleting a bloom', () => {
    render(<App />);

    const nameInput = screen.getByLabelText(/Bloom Name/i);
    const durationInput = screen.getByLabelText(/Duration in minutes/i);
    const plantButton = screen.getByRole('button', { name: /Plant Bloom/i });

    fireEvent.change(nameInput, { target: { value: 'Ephemeral Bloom' } });
    fireEvent.change(durationInput, { target: { value: '1' } });
    fireEvent.click(plantButton);

    expect(screen.getByText('Ephemeral Bloom')).toBeInTheDocument();

    const witherButton = screen.getByRole('button', { name: /Wither/i });
    fireEvent.click(witherButton);

    expect(screen.queryByText('Ephemeral Bloom')).not.toBeInTheDocument();
    expect(screen.getByText(/No blooms planted yet/i)).toBeInTheDocument();
  });

  test('input fields reset after adding a bloom', () => {
    render(<App />);

    const nameInput = screen.getByLabelText(/Bloom Name/i);
    const durationInput = screen.getByLabelText(/Duration in minutes/i);
    const plantButton = screen.getByRole('button', { name: /Plant Bloom/i });

    fireEvent.change(nameInput, { target: { value: 'Reset Test' } });
    fireEvent.change(durationInput, { target: { value: '5' } });
    fireEvent.click(plantButton);

    expect(nameInput).toHaveValue('');
    expect(durationInput).toHaveValue(30); // Resets to default 30
  });

  test('duration input prevents negative or zero values', () => {
    render(<App />);
    const durationInput = screen.getByLabelText(/Duration in minutes/i);

    fireEvent.change(durationInput, { target: { value: '-5' } });
    expect(durationInput).toHaveValue(1); // Should clamp to min 1

    fireEvent.change(durationInput, { target: { value: '0' } });
    expect(durationInput).toHaveValue(1); // Should clamp to min 1
  });
});
