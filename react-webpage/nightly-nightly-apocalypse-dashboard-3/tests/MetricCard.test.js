import React from 'react';
import { render, screen } from '@testing-library/react';
import MetricCard from '../src/components/MetricCard';

// Mocking CSS modules
jest.mock('../src/components/MetricCard.css', () => ({}));

describe('MetricCard', () => {
  const mockMetric = {
    id: 1,
    name: 'Test Metric Name',
    value: 'Test Value',
    description: 'This is a test description.'
  };

  test('renders metric name, value, and description', () => {
    render(<MetricCard metric={mockMetric} />);

    expect(screen.getByText('Test Metric Name')).toBeInTheDocument();
    expect(screen.getByText('Test Value')).toBeInTheDocument();
    expect(screen.getByText('This is a test description.')).toBeInTheDocument();
  });

  test('renders with correct CSS classes', () => {
    const { container } = render(<MetricCard metric={mockMetric} />);
    const cardElement = container.querySelector('.metric-card');
    expect(cardElement).toHaveClass('metric-card');
    expect(cardElement.querySelector('h3')).toHaveClass(''); // Assuming no specific class for h3
    expect(cardElement.querySelector('.value')).toHaveClass('value');
    expect(cardElement.querySelector('.description')).toHaveClass('description');
  });
});
