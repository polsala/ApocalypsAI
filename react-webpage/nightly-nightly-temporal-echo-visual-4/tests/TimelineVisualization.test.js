import { render, screen } from '@testing-library/react';
import TimelineVisualization from '../src/TimelineVisualization';
import '@testing-library/jest-dom';

describe('TimelineVisualization', () => {
  const mockEchoes = [
    { id: 'e1', term: 'Alpha', offset: 20, description: 'First echo', strength: 80 },
    { id: 'e2', term: 'Beta', offset: 50, description: 'Second echo', strength: 60 },
    { id: 'e3', term: 'Gamma', offset: 80, description: 'Third echo', strength: 90 }
  ];

  test('renders message when no echoes are provided', () => {
    // # Mock rationale: Tests the empty state of the component.
    render(<TimelineVisualization echoes={[]} />);
    expect(screen.getByText(/No echoes to display/i)).toBeInTheDocument();
  });

  test('renders all provided echoes', () => {
    // # Mock rationale: Verifies that each echo object passed as prop is rendered.
    render(<TimelineVisualization echoes={mockEchoes} />);

    expect(screen.getByText('Alpha')).toBeInTheDocument();
    expect(screen.getByText('(20 units)')).toBeInTheDocument();
    expect(screen.getByTitle('First echo')).toBeInTheDocument();

    expect(screen.getByText('Beta')).toBeInTheDocument();
    expect(screen.getByText('(50 units)')).toBeInTheDocument();
    expect(screen.getByTitle('Second echo')).toBeInTheDocument();

    expect(screen.getByText('Gamma')).toBeInTheDocument();
    expect(screen.getByText('(80 units)')).toBeInTheDocument();
    expect(screen.getByTitle('Third echo')).toBeInTheDocument();
  });

  test('echoes are sorted by offset', () => {
    // # Mock rationale: Ensures the sorting logic within the component works correctly.
    const unsortedEchoes = [
      { id: 'e2', term: 'Beta', offset: 50, description: 'Second echo', strength: 60 },
      { id: 'e1', term: 'Alpha', offset: 20, description: 'First echo', strength: 80 }
    ];
    render(<TimelineVisualization echoes={unsortedEchoes} />);

    const container = screen.getByTestId('timeline-container');
    const events = container.querySelectorAll('.timeline-event');
    expect(events[0]).toHaveTextContent('Alpha');
    expect(events[1]).toHaveTextContent('Beta');
  });

  test('each echo event has a unique key', () => {
    // # Mock rationale: React best practice for list rendering.
    const { container } = render(<TimelineVisualization echoes={mockEchoes} />);
    const events = container.querySelectorAll('.timeline-event');
    const keys = Array.from(events).map(event => event.getAttribute('key'));
    expect(new Set(keys).size).toBe(mockEchoes.length);
  });
});
