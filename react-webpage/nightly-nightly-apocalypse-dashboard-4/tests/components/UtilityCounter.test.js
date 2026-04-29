import React from 'react';
import { render, screen } from '@testing-library/react';
import UtilityCounter from '../../src/components/UtilityCounter';

// Mock rationale: Using mock data to ensure deterministic and offline tests.
// The mock data is directly passed as props to the component.

describe('UtilityCounter Component', () => {
  test('renders utility counts for different classifiers', () => {
    const mockCounts = {
      'python-utils': 120,
      'rust-utils': 30,
      'bash-utils': 80
    };
    render(<UtilityCounter utilityCounts={mockCounts} />);

    expect(screen.getByText(/Utility Counts/i)).toBeInTheDocument();
    expect(screen.getByText(/python-utils: 120/i)).toBeInTheDocument();
    expect(screen.getByText(/rust-utils: 30/i)).toBeInTheDocument();
    expect(screen.getByText(/bash-utils: 80/i)).toBeInTheDocument();
  });

  test('renders an empty list when no utility counts are provided', () => {
    render(<UtilityCounter utilityCounts={{}} />);
    expect(screen.getByText(/Utility Counts/i)).toBeInTheDocument();
    // Check that no specific counts are rendered
    expect(screen.queryByText(/: \d+/i)).not.toBeInTheDocument();
  });
});
