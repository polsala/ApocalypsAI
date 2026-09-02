import { render, screen } from '@testing-library/react';
import SignalVisualizer from '../src/SignalVisualizer';

describe('SignalVisualizer', () => {
  test('does not render anything if no data is provided', () => {
    const { container } = render(<SignalVisualizer data={null} />);
    expect(container).toBeEmptyDOMElement();
  });

  test('renders the correct number of circles based on numRings prop', () => {
    const mockData = {
      numRings: 5,
      hueStart: 0,
      hueEnd: 180,
      rotationSpeed: 1,
      flickerIntensity: 0.2,
      ringThickness: 2
    };
    render(<SignalVisualizer data={mockData} />);
    const circles = screen.getAllByRole('circle');
    expect(circles).toHaveLength(mockData.numRings);
  });

  test('each circle has the correct stroke-width based on ringThickness prop', () => {
    const mockData = {
      numRings: 3,
      hueStart: 0,
      hueEnd: 180,
      rotationSpeed: 1,
      flickerIntensity: 0.2,
      ringThickness: 3
    };
    render(<SignalVisualizer data={mockData} />);
    const circles = screen.getAllByRole('circle');
    circles.forEach(circle => {
      expect(circle).toHaveAttribute('stroke-width', String(mockData.ringThickness));
    });
  });

  test('each circle has a unique radius', () => {
    const mockData = {
      numRings: 4,
      hueStart: 0,
      hueEnd: 180,
      rotationSpeed: 1,
      flickerIntensity: 0.2,
      ringThickness: 1
    };
    render(<SignalVisualizer data={mockData} />);
    const circles = screen.getAllByRole('circle');
    const radii = circles.map(circle => circle.getAttribute('r'));
    const uniqueRadii = new Set(radii);
    expect(uniqueRadii.size).toBe(mockData.numRings);
  });

  test('circles have correct animation properties set via style', () => {
    const mockData = {
      numRings: 1,
      hueStart: 0,
      hueEnd: 180,
      rotationSpeed: 2,
      flickerIntensity: 0.4,
      ringThickness: 1
    };
    render(<SignalVisualizer data={mockData} />);
    const circle = screen.getByRole('circle');
    expect(circle).toHaveStyle(`animation-duration: ${4 / mockData.rotationSpeed}s`);
    expect(circle).toHaveStyle(`--flicker-intensity: ${mockData.flickerIntensity}`);
  });
});
