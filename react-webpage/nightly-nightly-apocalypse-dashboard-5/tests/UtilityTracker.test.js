import React from 'react';
import { render, screen } from '@testing-library/react';
import UtilityTracker from '../src/components/UtilityTracker';

describe('UtilityTracker Component', () => {
  test('renders message when no data is provided', () => {
    render(<UtilityTracker data={[]} />);
    expect(screen.getByText('No utilities generated yet...')).toBeInTheDocument();
  });

  test('renders utility items correctly', () => {
    const mockData = [
      {
        id: 1,
        name: 'nightly-spark-void',
        classifier: 'python-utils',
        status: 'Success'
      },
      {
        id: 2,
        name: 'nightly-whisper-rift',
        classifier: 'react-webpage',
        status: 'Pending'
      }
    ];
    render(<UtilityTracker data={mockData} />);

    expect(screen.getByText('nightly-spark-void')).toBeInTheDocument();
    expect(screen.getByText('python-utils')).toBeInTheDocument();
    expect(screen.getByText('Success')).toBeInTheDocument();

    expect(screen.getByText('nightly-whisper-rift')).toBeInTheDocument();
    expect(screen.getByText('react-webpage')).toBeInTheDocument();
    expect(screen.getByText('Pending')).toBeInTheDocument();
  });

  test('renders multiple utility items', () => {
    const mockData = [
      { id: 1, name: 'util-a', classifier: 'type-a', status: 'Success' },
      { id: 2, name: 'util-b', classifier: 'type-b', status: 'Failed' },
      { id: 3, name: 'util-c', classifier: 'type-c', status: 'In Progress' }
    ];
    render(<UtilityTracker data={mockData} />);

    expect(screen.getAllByRole('row').length).toBe(4); // Header + 3 rows
  });

  test('applies correct status classes', () => {
    const mockData = [
      { id: 1, name: 'util-success', classifier: 'type-a', status: 'Success' },
      { id: 2, name: 'util-failed', classifier: 'type-b', status: 'Failed' },
      { id: 3, name: 'util-pending', classifier: 'type-c', status: 'Pending' },
      { id: 4, name: 'util-progress', classifier: 'type-d', status: 'In Progress' }
    ];
    render(<UtilityTracker data={mockData} />);

    expect(screen.getByText('util-success').closest('tr')).toHaveClass('status-success');
    expect(screen.getByText('util-failed').closest('tr')).toHaveClass('status-failed');
    expect(screen.getByText('util-pending').closest('tr')).toHaveClass('status-pending');
    expect(screen.getByText('util-progress').closest('tr')).toHaveClass('status-in-progress');
  });
});
