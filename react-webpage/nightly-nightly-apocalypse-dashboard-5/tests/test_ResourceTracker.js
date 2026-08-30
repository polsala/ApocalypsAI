import React from 'react';
import { render, screen } from '@testing-library/react';
import ResourceTracker from '../src/components/ResourceTracker';

describe('ResourceTracker Component', () => {
  test('renders resource names and percentages', () => {
    const mockResources = {
      water: 75,
      food: 60,
      medicine: 90,
      ammo: 45
    };
    render(<ResourceTracker resources={mockResources} />);

    expect(screen.getByText(/Water: 75%/i)).toBeInTheDocument();
    expect(screen.getByText(/Food: 60%/i)).toBeInTheDocument();
    expect(screen.getByText(/Medicine: 90%/i)).toBeInTheDocument();
    expect(screen.getByText(/Ammo: 45%/i)).toBeInTheDocument();
  });

  test('renders progress bars with correct widths and colors', () => {
    const mockResources = {
      water: 80,
      food: 30,
      medicine: 10
    };
    render(<ResourceTracker resources={mockResources} />);

    // Check for the presence of progress bar elements and their styles
    const waterProgressBar = screen.getByText(/Water: 80%/i).closest('li').querySelector('.progress-bar');
    expect(waterProgressBar).toHaveStyle('width: 80%');
    expect(waterProgressBar).toHaveStyle('background-color: lightgreen');

    const foodProgressBar = screen.getByText(/Food: 30%/i).closest('li').querySelector('.progress-bar');
    expect(foodProgressBar).toHaveStyle('width: 30%');
    expect(foodProgressBar).toHaveStyle('background-color: gold');

    const medicineProgressBar = screen.getByText(/Medicine: 10%/i).closest('li').querySelector('.progress-bar');
    expect(medicineProgressBar).toHaveStyle('width: 10%');
    expect(medicineProgressBar).toHaveStyle('background-color: salmon');
  });

  test('renders correctly with empty resources object', () => {
    render(<ResourceTracker resources={{}} />);
    // Expecting no resource list items to be rendered, but the section header should be there.
    expect(screen.getByText(/Survival Resource Status/i)).toBeInTheDocument();
    expect(screen.queryByRole('listitem')).not.toBeInTheDocument();
  });
});
