import { render, screen } from '@testing-library/react';
import ChronoCompass from '../src/ChronoCompass';

describe('ChronoCompass Component', () => {
  test('renders a message when no events are present', () => {
    render(<ChronoCompass events={[]} />);
    expect(screen.getByText(/No temporal events logged yet/i)).toBeInTheDocument();
  });

  test('renders a list of events with correct details', () => {
    // Mock rationale: Providing fixed ISO strings for dates ensures deterministic output
    // for testing the ChronoCompass component's rendering logic.
    const mockEvents = [
      {
        id: 1,
        name: 'First Event',
        originalDate: '2024-07-20T10:00:00.000Z',
        shiftedDate: '2024-07-20T13:00:00.000Z',
        echoDate: '2024-07-13T10:00:00.000Z',
      },
      {
        id: 2,
        name: 'Second Event',
        originalDate: '2024-07-21T15:30:00.000Z',
        shiftedDate: '2024-07-21T18:30:00.000Z',
        echoDate: '2024-07-14T15:30:00.000Z',
      },
    ];

    render(<ChronoCompass events={mockEvents} />);

    expect(screen.getByText('First Event')).toBeInTheDocument();
    expect(screen.getByText(/Original: 7\/20\/2024, 10:00:00 AM/i)).toBeInTheDocument();
    expect(screen.getByText(/Shifted: 7\/20\/2024, 1:00:00 PM/i)).toBeInTheDocument();
    expect(screen.getByText(/Echo: 7\/13\/2024, 10:00:00 AM/i)).toBeInTheDocument();

    expect(screen.getByText('Second Event')).toBeInTheDocument();
    expect(screen.getByText(/Original: 7\/21\/2024, 3:30:00 PM/i)).toBeInTheDocument();
    expect(screen.getByText(/Shifted: 7\/21\/2024, 6:30:00 PM/i)).toBeInTheDocument();
    expect(screen.getByText(/Echo: 7\/14\/2024, 3:30:00 PM/i)).toBeInTheDocument();

    expect(screen.queryByText(/No temporal events logged yet/i)).not.toBeInTheDocument();
  });

  test('formats dates correctly', () => {
    const mockEvent = {
      id: 1,
      name: 'Single Event',
      originalDate: '2024-01-01T00:00:00.000Z',
      shiftedDate: '2024-01-01T03:00:00.000Z',
      echoDate: '2023-12-25T00:00:00.000Z',
    };
    render(<ChronoCompass events={[mockEvent]} />);

    // Depending on locale, this might vary slightly, but the core parts should be present.
    // Using a more flexible regex for date matching.
    expect(screen.getByText(/Original: 1\/1\/2024, 12:00:00 AM/i)).toBeInTheDocument();
    expect(screen.getByText(/Shifted: 1\/1\/2024, 3:00:00 AM/i)).toBeInTheDocument();
    expect(screen.getByText(/Echo: 12\/25\/2023, 12:00:00 AM/i)).toBeInTheDocument();
  });
});
