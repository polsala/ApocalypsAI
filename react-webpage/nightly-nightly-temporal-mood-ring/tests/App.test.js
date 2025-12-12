import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: Math.random is used to simulate anomaly severity.
// We mock it to ensure deterministic test results, controlling the generated severity.
const mockMathRandom = jest.spyOn(Math, 'random');

describe('App Component', () => {
  beforeEach(() => {
    // Reset mock before each test
    mockMathRandom.mockRestore();
  });

  test('renders Temporal Anomaly Mood Ring title', () => {
    render(<App />);
    const titleElement = screen.getByText(/Temporal Anomaly Mood Ring/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders Scan for Anomalies button', () => {
    render(<App />);
    const buttonElement = screen.getByRole('button', { name: /Scan for Anomalies/i });
    expect(buttonElement).toBeInTheDocument();
  });

  test('clicking scan button updates temporal mood (simulated)', () => {
    // Mock rationale: We want to test the state update, so we control Math.random
    // to ensure a predictable outcome for the mood change.
    mockMathRandom.mockReturnValueOnce(0.1); // First click: low severity
    mockMathRandom.mockReturnValueOnce(0.9); // Second click: high severity

    render(<App />);

    const buttonElement = screen.getByRole('button', { name: /Scan for Anomalies/i });

    // Initial state (default severity 0.5, which is 'Wobbly Warp')
    expect(screen.getByText(/Current Temporal Mood: Wobbly Warp/i)).toBeInTheDocument();
    expect(screen.getByText(/Severity Index: 0.50/i)).toBeInTheDocument();

    // Click once, expect low severity mood
    fireEvent.click(buttonElement);
    expect(screen.getByText(/Current Temporal Mood: Temporal Calm/i)).toBeInTheDocument();
    expect(screen.getByText(/Severity Index: 0.10/i)).toBeInTheDocument();

    // Click again, expect high severity mood
    fireEvent.click(buttonElement);
    expect(screen.getByText(/Current Temporal Mood: Chronal Chaos!/i)).toBeInTheDocument();
    expect(screen.getByText(/Severity Index: 0.90/i)).toBeInTheDocument();
  });
});
