import { render, screen } from '@testing-library/react';
import EchoVisualizer from '../src/EchoVisualizer';

describe('EchoVisualizer Component', () => {
  const mockData = [
    { offset: -1, intensity: 0.5, distortionType: 'Chronal Ripple' },
    { offset: 0, intensity: 0.8, distortionType: 'Paradox Pulse' },
    { offset: 1, intensity: 0.3, distortionType: 'Void Whisper' },
    { offset: 2, intensity: 1.0, distortionType: 'Chronal Ripple' },
  ];

  test('renders "No echo data" message when data is empty', () => {
    render(<EchoVisualizer data={[]} />);
    expect(screen.getByText(/No echo data to display./i)).toBeInTheDocument();
  });

  test('renders correct number of echo bars when data is provided', () => {
    render(<EchoVisualizer data={mockData} />);
    const echoBars = screen.getAllByTitle(/Offset: .*s, Intensity: .*, Type: .*/);
    expect(echoBars).toHaveLength(mockData.length);
  });

  test('each echo bar has a title with correct data', () => {
    render(<EchoVisualizer data={mockData} />);
    expect(screen.getByTitle('Offset: -1s, Intensity: 0.50, Type: Chronal Ripple')).toBeInTheDocument();
    expect(screen.getByTitle('Offset: 0s, Intensity: 0.80, Type: Paradox Pulse')).toBeInTheDocument();
    expect(screen.getByTitle('Offset: 1s, Intensity: 0.30, Type: Void Whisper')).toBeInTheDocument();
    expect(screen.getByTitle('Offset: 2s, Intensity: 1.00, Type: Chronal Ripple')).toBeInTheDocument();
  });

  test('renders the legend with distortion types', () => {
    render(<EchoVisualizer data={mockData} />);
    expect(screen.getByText('Chronal Ripple')).toBeInTheDocument();
    expect(screen.getByText('Paradox Pulse')).toBeInTheDocument();
    expect(screen.getByText('Void Whisper')).toBeInTheDocument();
  });

  test('echo bars have dynamic height and background color based on data', () => {
    render(<EchoVisualizer data={mockData} />);

    // Mock rationale: We are checking for the presence of style attributes that would be set
    // based on the data. We don't need to test exact pixel values, just that the logic
    // for setting these styles is applied.

    // The highest intensity is 1.0, so its height should be 100%
    const maxIntensityBar = screen.getByTitle('Offset: 2s, Intensity: 1.00, Type: Chronal Ripple');
    expect(maxIntensityBar).toHaveStyle('height: 100%');
    expect(maxIntensityBar).toHaveStyle('background-color: var(--color-ripple)');
    expect(maxIntensityBar).toHaveStyle('opacity: 1'); // 1.0 * 0.8 + 0.2 = 1.0

    // An intensity of 0.5 should have 50% height relative to max (1.0)
    const halfIntensityBar = screen.getByTitle('Offset: -1s, Intensity: 0.50, Type: Chronal Ripple');
    expect(halfIntensityBar).toHaveStyle('height: 50%');
    expect(halfIntensityBar).toHaveStyle('background-color: var(--color-ripple)');
    expect(halfIntensityBar).toHaveStyle('opacity: 0.6'); // 0.5 * 0.8 + 0.2 = 0.6

    // An intensity of 0.3 should have 30% height relative to max (1.0)
    const lowIntensityBar = screen.getByTitle('Offset: 1s, Intensity: 0.30, Type: Void Whisper');
    expect(lowIntensityBar).toHaveStyle('height: 30%');
    expect(lowIntensityBar).toHaveStyle('background-color: var(--color-whisper)');
    expect(lowIntensityBar).toHaveStyle('opacity: 0.44'); // 0.3 * 0.8 + 0.2 = 0.44
  });
});
