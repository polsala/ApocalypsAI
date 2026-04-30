import React from 'react';
import { render, screen } from '@testing-library/react';
import UtilityCard from '../src/components/UtilityCard';

describe('UtilityCard Component', () => {
  const mockUtility = {
    name: "nightly-test-utility",
    classifier: "test-utils",
    status: "Testing",
    readiness: 0.78
  };

  test('renders utility name, classifier, and status', () => {
    render(<UtilityCard utility={mockUtility} />);
    expect(screen.getByText('nightly-test-utility')).toBeInTheDocument();
    expect(screen.getByText('Classifier: test-utils')).toBeInTheDocument();
    expect(screen.getByText('Status: Testing')).toBeInTheDocument();
  });

  test('renders readiness percentage correctly', () => {
    render(<UtilityCard utility={mockUtility} />);
    expect(screen.getByText('Readiness: 78%')).toBeInTheDocument();
  });

  test('applies correct CSS class for high readiness', () => {
    const highReadinessUtility = { ...mockUtility, readiness: 0.95 };
    render(<UtilityCard utility={highReadinessUtility} />);
    const cardElement = screen.getByText('nightly-test-utility').closest('.utility-card');
    expect(cardElement).toHaveClass('high-readiness');
  });

  test('applies correct CSS class for medium readiness', () => {
    const mediumReadinessUtility = { ...mockUtility, readiness: 0.80 };
    render(<UtilityCard utility={mediumReadinessUtility} />);
    const cardElement = screen.getByText('nightly-test-utility').closest('.utility-card');
    expect(cardElement).toHaveClass('medium-readiness');
  });

  test('applies correct CSS class for low readiness', () => {
    const lowReadinessUtility = { ...mockUtility, readiness: 0.50 };
    render(<UtilityCard utility={lowReadinessUtility} />);
    const cardElement = screen.getByText('nightly-test-utility').closest('.utility-card');
    expect(cardElement).toHaveClass('low-readiness');
  });
});
