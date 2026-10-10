import { render, screen } from '@testing-library/react';
import MoodRing from '../src/MoodRing';
import '@testing-library/jest-dom';

// Mock rationale: No external dependencies or side effects to mock for this component.
// It's a pure functional component that renders based on props.

describe('MoodRing', () => {
  test('renders with chaotic color for low moodValue', () => {
    render(<MoodRing moodValue={10} />);
    const ringElement = screen.getByTestId('mood-ring');
    expect(ringElement).toHaveStyle('background-color: #FF4500'); // OrangeRed
  });

  test('renders with uncertain color for medium-low moodValue', () => {
    render(<MoodRing moodValue={40} />);
    const ringElement = screen.getByTestId('mood-ring');
    expect(ringElement).toHaveStyle('background-color: #FFD700'); // Gold
  });

  test('renders with balanced color for medium-high moodValue', () => {
    render(<MoodRing moodValue={70} />);
    const ringElement = screen.getByTestId('mood-ring');
    expect(ringElement).toHaveStyle('background-color: #32CD32'); // LimeGreen
  });

  test('renders with serene color for high moodValue', () => {
    render(<MoodRing moodValue={90} />);
    const ringElement = screen.getByTestId('mood-ring');
    expect(ringElement).toHaveStyle('background-color: #1E90FF'); // DodgerBlue
  });

  test('renders with correct box-shadow based on moodValue', () => {
    render(<MoodRing moodValue={60} />);
    const ringElement = screen.getByTestId('mood-ring');
    expect(ringElement).toHaveStyle('box-shadow: 0 0 20px 5px #32CD32'); // LimeGreen
  });
});
