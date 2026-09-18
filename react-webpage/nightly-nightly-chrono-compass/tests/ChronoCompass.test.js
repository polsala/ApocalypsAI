import { render, screen } from '@testing-library/react';
import ChronoCompass from '../src/ChronoCompass';

describe('ChronoCompass Component', () => {
  // Mock rationale: We provide deterministic task data to ensure the component
  // renders correctly based on specific inputs, without relying on external state
  // or random values. This allows for consistent and repeatable test results.
  const mockTasks = [
    { id: 1, name: 'Positive Task', duration: 30, charge: 'Positive' },
    { id: 2, name: 'Neutral Task', duration: 60, charge: 'Neutral' },
    { id: 3, name: 'Negative Task', duration: 90, charge: 'Negative' },
  ];

  test('renders without crashing', () => {
    render(<ChronoCompass tasks={[]} />);
    expect(screen.getByText(/Add tasks to see your compass!/i)).toBeInTheDocument();
  });

  test('renders correct number of segments for given tasks', () => {
    render(<ChronoCompass tasks={mockTasks} />);
    const segments = screen.getAllByRole('graphics-document'); // circles are graphics-document
    expect(segments.length).toBe(mockTasks.length);
  });

  test('displays total duration correctly', () => {
    render(<ChronoCompass tasks={mockTasks} />);
    const totalDuration = mockTasks.reduce((sum, task) => sum + task.duration, 0);
    expect(screen.getByText(`Total Temporal Energy: ${totalDuration} minutes`)).toBeInTheDocument();
  });

  test('segments have correct colors based on charge', () => {
    render(<ChronoCompass tasks={mockTasks} />);
    const positiveSegment = screen.getByTitle(/Positive Task/i);
    const neutralSegment = screen.getByTitle(/Neutral Task/i);
    const negativeSegment = screen.getByTitle(/Negative Task/i);

    expect(positiveSegment).toHaveAttribute('stroke', '#4CAF50'); // Green
    expect(neutralSegment).toHaveAttribute('stroke', '#9E9E9E');  // Grey
    expect(negativeSegment).toHaveAttribute('stroke', '#F44336');  // Red
  });

  test('segments have correct dasharray based on duration percentage', () => {
    render(<ChronoCompass tasks={mockTasks} />);
    const totalDuration = mockTasks.reduce((sum, task) => sum + task.duration, 0);
    const radius = 100;
    const circumference = 2 * Math.PI * radius;

    // Test Positive Task (30 min out of 180 total)
    const positiveSegment = screen.getByTitle(/Positive Task/i);
    const expectedPositiveDasharray = (30 / totalDuration) * circumference;
    expect(positiveSegment).toHaveAttribute('stroke-dasharray', `${expectedPositiveDasharray} ${circumference - expectedPositiveDasharray}`);

    // Test Neutral Task (60 min out of 180 total)
    const neutralSegment = screen.getByTitle(/Neutral Task/i);
    const expectedNeutralDasharray = (60 / totalDuration) * circumference;
    expect(neutralSegment).toHaveAttribute('stroke-dasharray', `${expectedNeutralDasharray} ${circumference - expectedNeutralDasharray}`);

    // Test Negative Task (90 min out of 180 total)
    const negativeSegment = screen.getByTitle(/Negative Task/i);
    const expectedNegativeDasharray = (90 / totalDuration) * circumference;
    expect(negativeSegment).toHaveAttribute('stroke-dasharray', `${expectedNegativeDasharray} ${circumference - expectedNegativeDasharray}`);
  });

  test('renders default message when no tasks are provided', () => {
    render(<ChronoCompass tasks={[]} />);
    expect(screen.getByText(/Add tasks to see your compass!/i)).toBeInTheDocument();
    const segments = screen.queryAllByRole('graphics-document');
    expect(segments.length).toBe(1); // Only the background circle
    expect(segments[0]).toHaveAttribute('stroke', '#555'); // Background circle color
  });
});
