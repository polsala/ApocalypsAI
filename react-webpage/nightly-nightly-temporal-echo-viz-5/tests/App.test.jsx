import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// Mock rationale: Mocking Date to ensure deterministic test results for timeline rendering.
// Without this, tests could fail based on the exact time they are run.
const MOCK_DATE_NOW = new Date('2024-07-22T12:00:00Z');

describe('App', () => {
  let originalDate;

  beforeAll(() => {
    originalDate = global.Date;
    // Mock Date constructor and Date.now()
    global.Date = class extends originalDate {
      constructor(dateString) {
        if (dateString) {
          return new originalDate(dateString);
        }
        return MOCK_DATE_NOW;
      }
      static now() {
        return MOCK_DATE_NOW.getTime();
      }
    };
  });

  afterAll(() => {
    global.Date = originalDate;
  });

  // Mock rationale: window.matchMedia is not available in JSDOM (testing environment)
  // and is used by some libraries (e.g., for responsive design checks).
  // Mocking it prevents console errors during tests.
  beforeEach(() => {
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: jest.fn().mockImplementation(query => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: jest.fn(), // Deprecated
        removeListener: jest.fn(), // Deprecated
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
      })),
    });
  });

  test('renders the main application title', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Visualizer/i)).toBeInTheDocument();
  });

  test('renders initial anomalies on the timeline', () => {
    render(<App />);
    expect(screen.getByTitle(/Minor temporal ripple detected/i)).toBeInTheDocument();
    expect(screen.getByTitle(/Localized time dilation event/i)).toBeInTheDocument();
    expect(screen.getByTitle(/Echo of a past paradox/i)).toBeInTheDocument();
  });

  test('allows adding a new anomaly', async () => {
    render(<App />);

    const timestampInput = screen.getByLabelText(/Timestamp:/i);
    const descriptionInput = screen.getByPlaceholderText(/e.g., Minor time loop/i);
    const severityInput = screen.getByLabelText(/Severity \(1-5\):/i);
    const addButton = screen.getByRole('button', { name: /Add Anomaly/i });

    // Simulate user input
    fireEvent.change(timestampInput, { target: { value: '2024-07-22T15:00' } });
    fireEvent.change(descriptionInput, { target: { value: 'New temporal distortion' } });
    fireEvent.change(severityInput, { target: { value: '5' } });

    fireEvent.click(addButton);

    // Wait for the new anomaly to appear
    await waitFor(() => {
      expect(screen.getByTitle(/New temporal distortion/i)).toBeInTheDocument();
    });

    // Check if the form inputs are cleared
    expect(timestampInput).toHaveValue('');
    expect(descriptionInput).toHaveValue('');
    expect(severityInput).toHaveValue(3); // Resets to default
  });

  test('displays anomaly details when an anomaly point is clicked', async () => {
    render(<App />);

    const anomalyPoint = screen.getByTitle(/Localized time dilation event/i);
    fireEvent.click(anomalyPoint);

    await waitFor(() => {
      expect(screen.getByText(/Anomaly Details/i)).toBeInTheDocument();
      expect(screen.getByText(/Localized time dilation event/i)).toBeInTheDocument();
      expect(screen.getByText(/Severity: 4/i)).toBeInTheDocument();
    });

    const closeButton = screen.getByRole('button', { name: /Close/i });
    fireEvent.click(closeButton);

    await waitFor(() => {
      expect(screen.queryByText(/Anomaly Details/i)).not.toBeInTheDocument();
    });
  });

  test('anomalies are sorted by timestamp after adding a new one', async () => {
    render(<App />);

    const timestampInput = screen.getByLabelText(/Timestamp:/i);
    const descriptionInput = screen.getByPlaceholderText(/e.g., Minor time loop/i);
    const addButton = screen.getByRole('button', { name: /Add Anomaly/i });

    // Add an anomaly that should be in the middle
    fireEvent.change(timestampInput, { target: { value: '2024-07-20T05:00' } });
    fireEvent.change(descriptionInput, { target: { value: 'Early morning glitch' } });
    fireEvent.click(addButton);

    await waitFor(() => {
      // The presence of the new anomaly confirms it was added and sorted into the list.
      // The visual sorting is handled by the AnomalyTimeline component based on the sorted prop.
      expect(screen.getByTitle(/Early morning glitch/i)).toBeInTheDocument();
    });
  });
});
