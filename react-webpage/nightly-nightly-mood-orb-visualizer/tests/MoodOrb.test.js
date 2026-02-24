import { render, screen } from '@testing-library/react';
import MoodOrb from '../src/MoodOrb';

describe('MoodOrb', () => {
  test('renders without crashing', () => {
    render(<MoodOrb mood={0} />);
    expect(screen.getByTestId('mood-orb')).toBeInTheDocument();
  });

  test('applies correct CSS variables based on mood prop (neutral)', () => {
    render(<MoodOrb mood={0} />);
    const orbContainer = screen.getByTestId('mood-orb');
    const orb = orbContainer.querySelector('.mood-orb');

    // Mood 0 should map to hue 60 (yellow/orange)
    expect(orb).toHaveStyle('--orb-color: hsl(60, 80%, 50%)');
    // Neutral mood (0) should have animationSpeed 1.5 - (0/100)*0.5 = 1.5
    expect(orb).toHaveStyle('--animation-speed: 1.5s');
    // Neutral mood (0) should have glowIntensity 0.5 + (0/100)*0.5 = 0.5
    expect(orb).toHaveStyle('--glow-intensity: 0.5');
  });

  test('applies correct CSS variables based on mood prop (high mood)', () => {
    render(<MoodOrb mood={100} />);
    const orbContainer = screen.getByTestId('mood-orb');
    const orb = orbContainer.querySelector('.mood-orb');

    // Mood 100 should map to hue 120 (green)
    expect(orb).toHaveStyle('--orb-color: hsl(120, 80%, 50%)');
    // High mood (100) should have animationSpeed 1.5 - (100/100)*0.5 = 1.0
    expect(orb).toHaveStyle('--animation-speed: 1s');
    // High mood (100) should have glowIntensity 0.5 + (100/100)*0.5 = 1.0
    expect(orb).toHaveStyle('--glow-intensity: 1');
  });

  test('applies correct CSS variables based on mood prop (low mood)', () => {
    render(<MoodOrb mood={-100} />);
    const orbContainer = screen.getByTestId('mood-orb');
    const orb = orbContainer.querySelector('.mood-orb');

    // Mood -100 should map to hue 0 (red)
    expect(orb).toHaveStyle('--orb-color: hsl(0, 80%, 50%)');
    // Low mood (-100) should have animationSpeed 1.5 - (100/100)*0.5 = 1.0
    expect(orb).toHaveStyle('--animation-speed: 1s');
    // Low mood (-100) should have glowIntensity 0.5 + (100/100)*0.5 = 1.0
    expect(orb).toHaveStyle('--glow-intensity: 1');
  });

  test('applies correct CSS variables based on mood prop (mid-low mood)', () => {
    render(<MoodOrb mood={-50} />);
    const orbContainer = screen.getByTestId('mood-orb');
    const orb = orbContainer.querySelector('.mood-orb');

    // Mood -50 should map to hue 30 (orange-red)
    expect(orb).toHaveStyle('--orb-color: hsl(30, 80%, 50%)');
    // Mid-low mood (-50) should have animationSpeed 1.5 - (50/100)*0.5 = 1.25
    expect(orb).toHaveStyle('--animation-speed: 1.25s');
    // Mid-low mood (-50) should have glowIntensity 0.5 + (50/100)*0.5 = 0.75
    expect(orb).toHaveStyle('--glow-intensity: 0.75');
  });
});
