import { render, screen } from '@testing-library/react';
import CelestialBody from '../src/CelestialBody';

describe('CelestialBody', () => {
  // Mock rationale: This is a presentational component. We test its rendering based on props.
  // No external dependencies or complex logic to mock, just prop-driven rendering.

  test('renders the celestial body with correct initial', () => {
    const props = {
      name: 'Solara',
      angle: 90,
      color: '#FFD700',
      radius: 15,
      orbitRadius: 100
    };
    render(<CelestialBody {...props} />);

    const bodyElement = screen.getByText('S');
    expect(bodyElement).toBeInTheDocument();
    expect(bodyElement).toHaveStyle(`background-color: ${props.color}`);
    expect(bodyElement).toHaveAttribute('title', 'Solara (90.0°)');

    // Check for basic positioning style (exact pixel values might vary slightly due to calc() and rounding)
    // We'll check for the presence of 'absolute' and general left/top properties
    expect(bodyElement).toHaveStyle('position: absolute');
    expect(bodyElement).toHaveStyle('left: calc(50% + 0px - 15px)'); // 100 * cos(0) - 15 = -15
    expect(bodyElement).toHaveStyle('top: calc(50% + 100px - 15px)'); // 100 * sin(0) - 15 = 85
  });

  test('renders with different props', () => {
    const props = {
      name: 'Lunaris',
      angle: 0,
      color: '#C0C0C0',
      radius: 10,
      orbitRadius: 50
    };
    render(<CelestialBody {...props} />);

    const bodyElement = screen.getByText('L');
    expect(bodyElement).toBeInTheDocument();
    expect(bodyElement).toHaveStyle(`background-color: ${props.color}`);
    expect(bodyElement).toHaveAttribute('title', 'Lunaris (0.0°)');

    // Check for basic positioning style
    expect(bodyElement).toHaveStyle('left: calc(50% + -50px - 10px)'); // 50 * cos(-PI/2) - 10 = -10
    expect(bodyElement).toHaveStyle('top: calc(50% + 0px - 10px)'); // 50 * sin(-PI/2) - 10 = -60
  });
});
