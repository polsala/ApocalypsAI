import { render, screen } from '@testing-library/react';
import TemporalMoodRing from '../src/TemporalMoodRing';

describe('TemporalMoodRing Component', () => {
  test('renders with "Temporal Calm" for low severity', () => {
    render(<TemporalMoodRing severity={0.1} />);
    expect(screen.getByText(/Current Temporal Mood: Temporal Calm/i)).toBeInTheDocument();
    expect(screen.getByText(/Severity Index: 0.10/i)).toBeInTheDocument();
    // Mock rationale: We are testing the component's rendering based on props.
    // No external dependencies to mock here, just verifying output.
  });

  test('renders with "Mild Ripples" for medium-low severity', () => {
    render(<TemporalMoodRing severity={0.3} />);
    expect(screen.getByText(/Current Temporal Mood: Mild Ripples/i)).toBeInTheDocument();
    expect(screen.getByText(/Severity Index: 0.30/i)).toBeInTheDocument();
  });

  test('renders with "Wobbly Warp" for medium severity', () => {
    render(<TemporalMoodRing severity={0.5} />);
    expect(screen.getByText(/Current Temporal Mood: Wobbly Warp/i)).toBeInTheDocument();
    expect(screen.getByText(/Severity Index: 0.50/i)).toBeInTheDocument();
  });

  test('renders with "Chronal Instability" for medium-high severity', () => {
    render(<TemporalMoodRing severity={0.7} />);
    expect(screen.getByText(/Current Temporal Mood: Chronal Instability/i)).toBeInTheDocument();
    expect(screen.getByText(/Severity Index: 0.70/i)).toBeInTheDocument();
  });

  test('renders with "Chronal Chaos!" for high severity', () => {
    render(<TemporalMoodRing severity={0.9} />);
    expect(screen.getByText(/Current Temporal Mood: Chronal Chaos!/i)).toBeInTheDocument();
    expect(screen.getByText(/Severity Index: 0.90/i)).toBeInTheDocument();
  });

  test('orb background color changes based on severity', () => {
    const { rerender } = render(<TemporalMoodRing severity={0.1} />);
    let orb = screen.getByTestId('temporal-orb');
    expect(orb).toHaveStyle('background-color: #4CAF50'); // Temporal Calm color

    rerender(<TemporalMoodRing severity={0.9} />);
    orb = screen.getByTestId('temporal-orb'); // Re-select after rerender
    expect(orb).toHaveStyle('background-color: #F44336'); // Chronal Chaos! color
  });
});
