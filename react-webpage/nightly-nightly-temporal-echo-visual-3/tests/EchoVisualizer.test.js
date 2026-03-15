import { render, screen } from '@testing-library/react';
import EchoVisualizer from '../src/components/EchoVisualizer';

describe('EchoVisualizer Component', () => {
  test('renders correct number of echo bars based on echoData prop', () => {
    const testEchoData = [0.1, 0.5, 0.9];
    render(<EchoVisualizer echoData={testEchoData} />);

    const echoBars = screen.getAllByLabelText(/Echo bar \d+ with strength \d+\.\d+/i);
    expect(echoBars).toHaveLength(testEchoData.length);
  });

  test('renders no echo bars when echoData is empty', () => {
    render(<EchoVisualizer echoData={[]} />);
    const echoBars = screen.queryAllByLabelText(/Echo bar/i);
    expect(echoBars).toHaveLength(0);
  });

  test('each echo bar has a title with its strength', () => {
    const testEchoData = [0.25, 0.75];
    render(<EchoVisualizer echoData={testEchoData} />);

    const firstBar = screen.getByLabelText(/Echo bar 1 with strength 0\.25/i);
    expect(firstBar).toHaveAttribute('title', 'Echo Strength: 0.25');

    const secondBar = screen.getByLabelText(/Echo bar 2 with strength 0\.75/i);
    expect(secondBar).toHaveAttribute('title', 'Echo Strength: 0.75');
  });

  test('echo bar height and opacity are set correctly based on strength', () => {
    const testEchoData = [0.3, 0.6];
    render(<EchoVisualizer echoData={testEchoData} />);

    const firstBar = screen.getByLabelText(/Echo bar 1 with strength 0\.30/i);
    expect(firstBar).toHaveStyle('height: 30%');
    expect(firstBar).toHaveStyle('opacity: 0.4'); // strength + 0.1

    const secondBar = screen.getByLabelText(/Echo bar 2 with strength 0\.60/i);
    expect(secondBar).toHaveStyle('height: 60%');
    expect(secondBar).toHaveStyle('opacity: 0.7'); // strength + 0.1
  });
});
