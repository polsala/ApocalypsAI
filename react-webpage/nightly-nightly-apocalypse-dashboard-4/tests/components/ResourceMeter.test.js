import React from 'react';
import { render, screen } from '@testing-library/react';
import ResourceMeter from '../../src/components/ResourceMeter';

// Mock rationale: Using mock data to ensure deterministic and offline tests.
// The mock data is directly passed as props to the component.

describe('ResourceMeter Component', () => {
  test('renders scarcity level correctly for medium range', () => {
    render(<ResourceMeter scarcityLevel={50} />);
    expect(screen.getByText(/Resource Scarcity Meter/i)).toBeInTheDocument();
    expect(screen.getByText(/50%/i)).toBeInTheDocument();
    // Check for the presence of the 'medium' class on the bar
    const meterBar = screen.getByText(/50%/i).closest('.meter-bar');
    expect(meterBar).toHaveClass('medium');
  });

  test('renders scarcity level correctly for low range', () => {
    render(<ResourceMeter scarcityLevel={25} />);
    expect(screen.getByText(/25%/i)).toBeInTheDocument();
    const meterBar = screen.getByText(/25%/i).closest('.meter-bar');
    expect(meterBar).toHaveClass('low');
  });

  test('renders scarcity level correctly for high range', () => {
    render(<ResourceMeter scarcityLevel={75} />);
    expect(screen.getByText(/75%/i)).toBeInTheDocument();
    const meterBar = screen.getByText(/75%/i).closest('.meter-bar');
    expect(meterBar).toHaveClass('high');
  });

  test('renders 0% when scarcity level is 0', () => {
    render(<ResourceMeter scarcityLevel={0} />);
    expect(screen.getByText(/0%/i)).toBeInTheDocument();
    const meterBar = screen.getByText(/0%/i).closest('.meter-bar');
    expect(meterBar).toHaveClass('low');
  });
});
