import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Timeline from '../src/components/Timeline';

describe('Timeline', () => {
  const mockEchoes = [
    { id: 't1', date: '2023-01-01T00:00:00Z', title: 'Test Event 1', description: 'Description 1', type: 'creation' },
    { id: 't2', date: '2023-01-02T00:00:00Z', title: 'Test Event 2', description: 'Description 2', type: 'anomaly' }
  ];

  test('renders "No temporal echoes detected." when no echoes are provided', () => {
    render(<Timeline echoes={[]} />);
    expect(screen.getByText(/No temporal echoes detected./i)).toBeInTheDocument();
  });

  test('renders all provided echo events', () => {
    render(<Timeline echoes={mockEchoes} />);
    expect(screen.getByText('Test Event 1')).toBeInTheDocument();
    expect(screen.getByText('Description 1')).toBeInTheDocument();
    expect(screen.getByText('Test Event 2')).toBeInTheDocument();
    expect(screen.getByText('Description 2')).toBeInTheDocument();
    expect(screen.getAllByRole('heading', { level: 3 })).toHaveLength(2);
  });

  test('renders correct emoji for event types', () => {
    render(<Timeline echoes={mockEchoes} />);
    expect(screen.getByText('✨')).toBeInTheDocument(); // creation type
    expect(screen.getByText('⚠️')).toBeInTheDocument(); // anomaly type
  });

  test('renders formatted dates and times', () => {
    render(<Timeline echoes={mockEchoes} />);
    expect(screen.getByText(/January 1, 2023/)).toBeInTheDocument();
    expect(screen.getByText(/January 2, 2023/)).toBeInTheDocument();
    expect(screen.getAllByText(/12:00 AM/)).toHaveLength(2);
  });
});
