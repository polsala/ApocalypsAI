/**
 * @file App.test.js
 * @description Integration tests for the main App component.
 */

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock ChronoWeave to avoid complex SVG rendering and animation logic in App tests
jest.mock('../src/ChronoWeave', () => {
  return jest.fn((props) => (
    <div data-testid="mock-chrono-weave" data-isrunning={props.isRunning.toString()} data-speed={props.speed} data-anomalyfrequency={props.anomalyFrequency}>
      Mock ChronoWeave
    </div>
  ));
});

describe('App', () => {
  it('renders without crashing', () => {
    render(<App />);
    expect(screen.getByText(/Stop Weave/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Speed:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Anomaly Frequency:/i)).toBeInTheDocument();
    expect(screen.getByTestId('mock-chrono-weave')).toBeInTheDocument();
  });

  it('toggles isRunning state when Start/Stop button is clicked', () => {
    render(<App />);
    const startStopButton = screen.getByText(/Stop Weave/i);
    const chronoWeave = screen.getByTestId('mock-chrono-weave');

    expect(chronoWeave).toHaveAttribute('data-isrunning', 'true');
    expect(startStopButton).toHaveTextContent('Stop Weave');

    fireEvent.click(startStopButton);

    expect(chronoWeave).toHaveAttribute('data-isrunning', 'false');
    expect(startStopButton).toHaveTextContent('Start Weave');

    fireEvent.click(startStopButton);

    expect(chronoWeave).toHaveAttribute('data-isrunning', 'true');
    expect(startStopButton).toHaveTextContent('Stop Weave');
  });

  it('updates speed state when speed slider is changed', () => {
    render(<App />);
    const speedSlider = screen.getByLabelText(/Speed:/i);
    const chronoWeave = screen.getByTestId('mock-chrono-weave');

    expect(speedSlider).toHaveValue('50');
    expect(chronoWeave).toHaveAttribute('data-speed', '50');

    fireEvent.change(speedSlider, { target: { value: '75' } });

    expect(speedSlider).toHaveValue('75');
    expect(chronoWeave).toHaveAttribute('data-speed', '75');
  });

  it('updates anomaly frequency state when frequency slider is changed', () => {
    render(<App />);
    const frequencySlider = screen.getByLabelText(/Anomaly Frequency:/i);
    const chronoWeave = screen.getByTestId('mock-chrono-weave');

    expect(frequencySlider).toHaveValue('20');
    expect(chronoWeave).toHaveAttribute('data-anomalyfrequency', '20');

    fireEvent.change(frequencySlider, { target: { value: '60' } });

    expect(frequencySlider).toHaveValue('60');
    expect(chronoWeave).toHaveAttribute('data-anomalyfrequency', '60');
  });
});
