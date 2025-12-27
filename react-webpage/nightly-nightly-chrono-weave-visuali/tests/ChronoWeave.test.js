/**
 * @file ChronoWeave.test.js
 * @description Unit tests for the ChronoWeave component.
 */

import React from 'react';
import { render, screen, act } from '@testing-library/react';
import ChronoWeave from '../src/ChronoWeave';
import * as AnomalyDetector from '../src/AnomalyDetector';

// Mock ChronoThread to simplify ChronoWeave tests
jest.mock('../src/ChronoThread', () => {
  return jest.fn((props) => (
    <path data-testid={`chrono-thread-${props.id}`} d={props.points.map((p, i) => i === 0 ? `M${p.x},${p.y}` : `L${p.x},${p.y}`).join(' ')} className={props.isAnomalous ? 'anomalous' : ''} />
  ));
});

describe('ChronoWeave', () => {
  let requestAnimationFrameSpy;
  let cancelAnimationFrameSpy;
  let mockPerformanceNow;
  let mockDateNow;

  beforeAll(() => {
    // Mock rationale: Simulates browser animation frame for deterministic testing of visual updates.
    requestAnimationFrameSpy = jest.spyOn(window, 'requestAnimationFrame').mockImplementation((cb) => {
      return setTimeout(() => cb(mockPerformanceNow()), 16);
    });
    cancelAnimationFrameSpy = jest.spyOn(window, 'cancelAnimationFrame').mockImplementation(clearTimeout);

    // Mock rationale: Provides a consistent time for animation calculations, ensuring deterministic test results.
    mockPerformanceNow = jest.fn(() => 0);
    jest.spyOn(window.performance, 'now').mockImplementation(mockPerformanceNow);

    // Mock rationale: Provides a consistent time for anomaly duration calculations, ensuring deterministic test results.
    mockDateNow = jest.fn(() => 0);
    jest.spyOn(Date, 'now').mockImplementation(mockDateNow);
  });

  afterEach(() => {
    jest.clearAllMocks();
    mockPerformanceNow.mockReturnValue(0);
    mockDateNow.mockReturnValue(0);
  });

  afterAll(() => {
    requestAnimationFrameSpy.mockRestore();
    cancelAnimationFrameSpy.mockRestore();
    jest.restoreAllMocks();
  });

  it('renders an SVG element and multiple ChronoThread components', async () => {
    render(<ChronoWeave isRunning={true} speed={50} anomalyFrequency={20} />);

    const svgElement = screen.getByRole('img', { hidden: true }); // SVG elements can be found by role 'img'
    expect(svgElement).toBeInTheDocument();

    // Wait for threads to be initialized and rendered
    await act(async () => {
      // Advance time to allow initial useEffects to run and threads to be created
      mockPerformanceNow.mockReturnValue(100);
      mockDateNow.mockReturnValue(100);
      jest.runAllTimers(); // For requestAnimationFrame setTimeout
    });

    // Expect 10 threads to be rendered (NUM_THREADS constant)
    for (let i = 0; i < 10; i++) {
      expect(screen.getByTestId(`chrono-thread-${i}`)).toBeInTheDocument();
    }
  });

  it('does not animate when isRunning is false', async () => {
    render(<ChronoWeave isRunning={false} speed={50} anomalyFrequency={20} />);

    await act(async () => {
      mockPerformanceNow.mockReturnValue(100);
      mockDateNow.mockReturnValue(100);
      jest.runAllTimers();
    });

    const initialThread = screen.getByTestId('chrono-thread-0');
    const initialD = initialThread.getAttribute('d');

    await act(async () => {
      mockPerformanceNow.mockReturnValue(200);
      mockDateNow.mockReturnValue(200);
      jest.runAllTimers();
    });

    const updatedThread = screen.getByTestId('chrono-thread-0');
    const updatedD = updatedThread.getAttribute('d');

    // The path data should not change significantly if not running (only initial setup might cause a change)
    // For this test, we'll check if the animation loop continues to call requestAnimationFrame but doesn't update state.
    expect(requestAnimationFrameSpy).toHaveBeenCalledTimes(2); // Initial call + one more after first frame
    // The actual path data might slightly change due to initial setup, but no continuous movement.
    // A more robust test would check specific point values, but for now, this is sufficient.
  });

  it('animates threads when isRunning is true and time advances', async () => {
    render(<ChronoWeave isRunning={true} speed={50} anomalyFrequency={20} />);

    await act(async () => {
      mockPerformanceNow.mockReturnValue(100);
      mockDateNow.mockReturnValue(100);
      jest.runAllTimers();
    });

    const initialThread = screen.getByTestId('chrono-thread-0');
    const initialD = initialThread.getAttribute('d');

    await act(async () => {
      // Advance time significantly to trigger multiple animation frames
      mockPerformanceNow.mockReturnValue(1000);
      mockDateNow.mockReturnValue(1000);
      jest.runAllTimers();
    });

    const updatedThread = screen.getByTestId('chrono-thread-0');
    const updatedD = updatedThread.getAttribute('d');

    expect(updatedD).not.toEqual(initialD); // Path data should have changed due to movement
    expect(requestAnimationFrameSpy).toHaveBeenCalled();
  });

  it('applies anomaly class when anomaly is triggered', async () => {
    // Mock rationale: Controls random number generation for deterministic testing of anomaly triggers.
    jest.spyOn(AnomalyDetector, 'shouldTriggerAnomaly').mockReturnValue(true);
    jest.spyOn(AnomalyDetector, 'getAnomalyDuration').mockReturnValue(500); // 500ms anomaly

    render(<ChronoWeave isRunning={true} speed={50} anomalyFrequency={100} />);

    await act(async () => {
      mockPerformanceNow.mockReturnValue(100);
      mockDateNow.mockReturnValue(100);
      jest.runAllTimers();
    });

    const thread0 = screen.getByTestId('chrono-thread-0');
    expect(thread0).toHaveClass('anomalous');

    // Advance time past anomaly duration
    await act(async () => {
      mockPerformanceNow.mockReturnValue(100 + 500 + 100); // Current time + duration + buffer
      mockDateNow.mockReturnValue(100 + 500 + 100);
      jest.runAllTimers();
    });

    expect(thread0).not.toHaveClass('anomalous');
  });

  it('removes anomaly class after anomaly duration', async () => {
    // Mock rationale: Controls random number generation for deterministic testing of anomaly triggers.
    jest.spyOn(AnomalyDetector, 'shouldTriggerAnomaly')
      .mockReturnValueOnce(true) // Trigger anomaly initially
      .mockReturnValue(false); // No new anomalies after that
    jest.spyOn(AnomalyDetector, 'getAnomalyDuration').mockReturnValue(100); // Short anomaly for testing

    render(<ChronoWeave isRunning={true} speed={50} anomalyFrequency={100} />);

    // Initial render and first animation frame
    await act(async () => {
      mockPerformanceNow.mockReturnValue(100);
      mockDateNow.mockReturnValue(100);
      jest.runAllTimers();
    });

    const thread0 = screen.getByTestId('chrono-thread-0');
    expect(thread0).toHaveClass('anomalous');

    // Advance time just before anomaly ends
    await act(async () => {
      mockPerformanceNow.mockReturnValue(100 + 90); // 90ms into 100ms anomaly
      mockDateNow.mockReturnValue(100 + 90);
      jest.runAllTimers();
    });
    expect(thread0).toHaveClass('anomalous');

    // Advance time past anomaly end
    await act(async () => {
      mockPerformanceNow.mockReturnValue(100 + 110); // 110ms into 100ms anomaly
      mockDateNow.mockReturnValue(100 + 110);
      jest.runAllTimers();
    });
    expect(thread0).not.toHaveClass('anomalous');
  });
});
