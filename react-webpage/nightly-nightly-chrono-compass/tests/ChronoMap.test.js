import { render, screen, fireEvent } from '@testing-library/react';
import ChronoMap from '../src/components/ChronoMap';

// Mock rationale: We are testing the ChronoMap component in isolation.
// The `mockTemporalData` provides a fixed, deterministic dataset for rendering
// and interaction tests, ensuring tests are offline and repeatable.
const mockTemporalData = [
  { id: 'region-a', name: 'Region A', stability: 0.9, drift: 0.01, coordinates: { x: 50, y: 50 } },
  { id: 'region-b', name: 'Region B', stability: 0.4, drift: 0.2, coordinates: { x: 100, y: 100 } }
];

describe('ChronoMap', () => {
  test('renders map title', () => {
    render(<ChronoMap data={[]} onRegionClick={() => {}} />);
    expect(screen.getByText(/Temporal Stability Map/i)).toBeInTheDocument();
  });

  test('renders regions based on provided data', () => {
    render(<ChronoMap data={mockTemporalData} onRegionClick={() => {}} />);
    expect(screen.getByText('Region A')).toBeInTheDocument();
    expect(screen.getByText('Region B')).toBeInTheDocument();
  });

  test('calls onRegionClick when a region is clicked', () => {
    const handleClick = jest.fn();
    render(<ChronoMap data={mockTemporalData} onRegionClick={handleClick} />);

    fireEvent.click(screen.getByText('Region A'));
    expect(handleClick).toHaveBeenCalledTimes(1);
    expect(handleClick).toHaveBeenCalledWith('region-a');
  });

  test('highlights selected region', () => {
    const { container } = render(
      <ChronoMap data={mockTemporalData} onRegionClick={() => {}} selectedRegionId="region-a" />
    );
    const selectedCircle = container.querySelector('g:has(text:contains("Region A")) circle');
    expect(selectedCircle).toHaveAttribute('stroke', '#61dafb');
    expect(selectedCircle).toHaveAttribute('stroke-width', '3');

    const unselectedCircle = container.querySelector('g:has(text:contains("Region B")) circle');
    expect(unselectedCircle).toHaveAttribute('stroke', '#888');
    expect(unselectedCircle).toHaveAttribute('stroke-width', '1');
  });

  test('displays correct color for stable region', () => {
    const { container } = render(
      <ChronoMap data={[{ id: 'stable-region', name: 'Stable', stability: 0.9, drift: 0.01, coordinates: { x: 10, y: 10 } }]} onRegionClick={() => {}} />
    );
    const circle = container.querySelector('circle');
    expect(circle).toHaveAttribute('fill', '#4CAF50');
  });

  test('displays correct color for unstable region', () => {
    const { container } = render(
      <ChronoMap data={[{ id: 'unstable-region', name: 'Unstable', stability: 0.3, drift: 0.3, coordinates: { x: 10, y: 10 } }]} onRegionClick={() => {}} />
    );
    const circle = container.querySelector('circle');
    expect(circle).toHaveAttribute('fill', '#F44336');
  });
});
