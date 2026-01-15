import React from 'react';
import { render, screen } from '@testing-library/react';
import SurvivalTip from '../src/components/SurvivalTip';

// Mocking CSS modules
jest.mock('../src/components/SurvivalTip.css', () => ({}));

describe('SurvivalTip', () => {
  const mockTip = 'This is a sample survival tip.';

  test('renders the survival tip text', () => {
    render(<SurvivalTip tip={mockTip} />);
    expect(screen.getByText('This is a sample survival tip.')).toBeInTheDocument();
  });

  test('renders with correct CSS class', () => {
    const { container } = render(<SurvivalTip tip={mockTip} />);
    const tipElement = container.querySelector('.survival-tip');
    expect(tipElement).toHaveClass('survival-tip');
    expect(tipElement.querySelector('p')).toHaveTextContent(mockTip);
  });
});
