import { render, screen } from '@testing-library/react';
import ClutterItem from '../src/ClutterItem'; // Mock rationale: Using mock data for deterministic tests.

describe('ClutterItem Component', () => {
  const mockItem = {
    id: 'test-id',
    name: 'Test Clutter Item',
    type: 'TestType',
    temporalWeight: 100,
    description: 'This is a test description.',
    link: 'http://example.com/test'
  };

  test('renders item name, type, temporal weight, and description', () => {
    render(<ClutterItem item={mockItem} />);

    expect(screen.getByText(mockItem.name)).toBeInTheDocument();
    expect(screen.getByText(mockItem.type)).toBeInTheDocument();
    expect(screen.getByText(`Temporal Weight: ${mockItem.temporalWeight} days`)).toBeInTheDocument();
    expect(screen.getByText(mockItem.description)).toBeInTheDocument();
  });

  test('renders link if provided', () => {
    render(<ClutterItem item={mockItem} />);
    const linkElement = screen.getByRole('link', { name: mockItem.link });
    expect(linkElement).toBeInTheDocument();
    expect(linkElement).toHaveAttribute('href', mockItem.link);
  });

  test('does not render link if not provided', () => {
    const itemWithoutLink = { ...mockItem, link: undefined };
    render(<ClutterItem item={itemWithoutLink} />);
    expect(screen.queryByRole('link')).not.toBeInTheDocument();
  });

  test('temporal weight color changes based on weight value', () => {
    const itemVeryOld = { ...mockItem, temporalWeight: 400 };
    const itemOld = { ...mockItem, temporalWeight: 200 };
    const itemModeratelyOld = { ...mockItem, temporalWeight: 100 };
    const itemNewer = { ...mockItem, temporalWeight: 50 };

    render(<ClutterItem item={itemVeryOld} />);
    expect(screen.getByText(/Temporal Weight: 400 days/i)).toHaveStyle('color: #ff6b6b'); // Red

    render(<ClutterItem item={itemOld} />);
    expect(screen.getByText(/Temporal Weight: 200 days/i)).toHaveStyle('color: #ffa500'); // Orange

    render(<ClutterItem item={itemModeratelyOld} />);
    expect(screen.getByText(/Temporal Weight: 100 days/i)).toHaveStyle('color: #ffd700'); // Gold

    render(<ClutterItem item={itemNewer} />);
    expect(screen.getByText(/Temporal Weight: 50 days/i)).toHaveStyle('color: #6aff6a'); // Green
  });
});
