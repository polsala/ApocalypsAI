import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

describe('App Component', () => {
  test('renders Nightly Cosmic Drift Compass title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Cosmic Drift Compass/i)).toBeInTheDocument();
  });

  test('renders initial cosmic drift value', () => {
    render(<App />);
    expect(screen.getByText(/Current Cosmic Drift: 0°/i)).toBeInTheDocument();
  });

  test('renders initial alignment advice', () => {
    render(<App />);
    // Mock rationale: The getAlignmentAdvice function is pure and deterministic.
    // For drift 0, it should return the specific advice for the 0-45 range.
    expect(screen.getByText(/The Whispering Nebula aligns. Seek quiet contemplation and hidden truths./i)).toBeInTheDocument();
  });

  test('advances cosmic drift on button click', () => {
    render(<App />);
    const advanceButton = screen.getByRole('button', { name: /Advance Cosmic Drift/i });
    fireEvent.click(advanceButton);
    // Mock rationale: The advanceDrift function deterministically adds 30 to the drift.
    expect(screen.getByText(/Current Cosmic Drift: 30°/i)).toBeInTheDocument();
  });

  test('alignment advice changes after advancing drift', () => {
    render(<App />);
    const advanceButton = screen.getByRole('button', { name: /Advance Cosmic Drift/i });

    // Initial drift 0
    expect(screen.getByText(/The Whispering Nebula aligns./i)).toBeInTheDocument();

    // Advance to 30°
    fireEvent.click(advanceButton);
    expect(screen.getByText(/Current Cosmic Drift: 30°/i)).toBeInTheDocument();
    // Mock rationale: The getAlignmentAdvice function is pure. For drift 30, it's still in the 0-45 range.
    expect(screen.getByText(/The Whispering Nebula aligns./i)).toBeInTheDocument();

    // Advance to 60°
    fireEvent.click(advanceButton);
    expect(screen.getByText(/Current Cosmic Drift: 60°/i)).toBeInTheDocument();
    // Mock rationale: The getAlignmentAdvice function is pure. For drift 60, it should be in the 45-135 range.
    expect(screen.getByText(/The Glimmering Comet streaks. Embrace change and swift action./i)).toBeInTheDocument();
  });

  test('celestial bodies are rendered', () => {
    render(<App />);
    expect(screen.getByTitle(/Whispering Nebula/i)).toBeInTheDocument();
    expect(screen.getByTitle(/Glimmering Comet/i)).toBeInTheDocument();
    expect(screen.getByTitle(/Silent Moon Fragment/i)).toBeInTheDocument();
    expect(screen.getByTitle(/Wandering Star/i)).toBeInTheDocument();
  });

  test('drift cycles correctly after multiple advances', () => {
    render(<App />);
    const advanceButton = screen.getByRole('button', { name: /Advance Cosmic Drift/i });

    // Advance 12 times (30 * 12 = 360), should reset to 0
    for (let i = 0; i < 12; i++) {
      fireEvent.click(advanceButton);
    }
    // Mock rationale: The advanceDrift function uses modulo 360, ensuring it cycles.
    expect(screen.getByText(/Current Cosmic Drift: 0°/i)).toBeInTheDocument();
    expect(screen.getByText(/The Whispering Nebula aligns./i)).toBeInTheDocument();
  });
});
