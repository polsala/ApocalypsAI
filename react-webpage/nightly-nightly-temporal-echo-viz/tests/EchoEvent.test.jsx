import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import EchoEvent from '../src/components/EchoEvent';

describe('EchoEvent', () => {
  const mockEvent = {
    id: 'e1',
    date: '2023-04-20T10:30:00Z',
    title: 'Critical System Update',
    description: 'Applied security patches and performance enhancements.',
    type: 'system-update'
  };

  test('renders event title, description, and formatted date/time', () => {
    render(<EchoEvent event={mockEvent} />);

    expect(screen.getByText(mockEvent.title)).toBeInTheDocument();
    expect(screen.getByText(mockEvent.description)).toBeInTheDocument();
    expect(screen.getByText(/April 20, 2023/)).toBeInTheDocument();
    expect(screen.getByText(/10:30 AM/)).toBeInTheDocument();
  });

  test('renders the correct emoji for the event type', () => {
    render(<EchoEvent event={mockEvent} />);
    expect(screen.getByText('⚙️')).toBeInTheDocument(); // system-update type
  });

  test('applies type-specific class name', () => {
    const { container } = render(<EchoEvent event={mockEvent} />);
    expect(container.firstChild).toHaveClass('echo-event--system-update');
  });

  test('renders default emoji for unknown event type', () => {
    const unknownTypeEvent = { ...mockEvent, type: 'unknown' };
    render(<EchoEvent event={unknownTypeEvent} />);
    expect(screen.getByText('📜')).toBeInTheDocument(); // default emoji
  });
});
