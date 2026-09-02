import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import SignalVisualizer from '../src/SignalVisualizer';

// Mock rationale: We mock the SignalVisualizer component to isolate the testing
// of the App component's logic. This allows us to verify that App correctly
// generates and passes 'data' props to SignalVisualizer without needing to
// render the complex SVG elements in detail during App's tests.
jest.mock('../src/SignalVisualizer', () => {
  return jest.fn((props) => (
    <div data-testid="mock-signal-visualizer" data-signal-data={JSON.stringify(props.data)} />
  ));
});

describe('App', () => {
  beforeEach(() => {
    // Clear mock calls before each test
    SignalVisualizer.mockClear();
  });

  test('renders the main heading and input field', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Beacon Signal Visualizer/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Beacon Signal Input/i)).toBeInTheDocument();
  });

  test('displays placeholder text when input is empty', () => {
    render(<App />);
    expect(screen.getByText(/Your signal will appear here.../i)).toBeInTheDocument();
    expect(SignalVisualizer).not.toHaveBeenCalled();
  });

  test('updates input value on change', () => {
    render(<App />);
    const inputElement = screen.getByLabelText(/Beacon Signal Input/i);
    fireEvent.change(inputElement, { target: { value: 'test signal' } });
    expect(inputElement.value).toBe('test signal');
  });

  test('renders SignalVisualizer with correct data when input is provided', () => {
    render(<App />);
    const inputElement = screen.getByLabelText(/Beacon Signal Input/i);
    fireEvent.change(inputElement, { target: { value: 'hello' } });

    expect(SignalVisualizer).toHaveBeenCalledTimes(1);
    const visualizerProps = SignalVisualizer.mock.calls[0][0].data;

    // Expected data for 'hello' (sum of char codes: 104+101+108+108+111 = 532)
    // numRings = (532 % 5) + 3 = 2 + 3 = 5
    // hueStart = 532 % 360 = 172
    // hueEnd = (532 * 2) % 360 = 1064 % 360 = 344
    // rotationSpeed = (532 % 3) + 1 = 1 + 1 = 2
    // flickerIntensity = (532 % 5) / 10 + 0.1 = 2 / 10 + 0.1 = 0.2 + 0.1 = 0.3
    // ringThickness = (532 % 3) + 1 = 1 + 1 = 2

    expect(visualizerProps).toEqual({
      numRings: 5,
      hueStart: 172,
      hueEnd: 344,
      rotationSpeed: 2,
      flickerIntensity: 0.3,
      ringThickness: 2
    });
  });

  test('generates different data for different inputs', () => {
    render(<App />);
    const inputElement = screen.getByLabelText(/Beacon Signal Input/i);

    fireEvent.change(inputElement, { target: { value: 'alpha' } });
    const data1 = SignalVisualizer.mock.calls[0][0].data;
    SignalVisualizer.mockClear(); // Clear calls for next input

    fireEvent.change(inputElement, { target: { value: 'beta' } });
    const data2 = SignalVisualizer.mock.calls[0][0].data;

    expect(data1).not.toEqual(data2);
  });

  test('generates same data for same inputs', () => {
    render(<App />);
    const inputElement = screen.getByLabelText(/Beacon Signal Input/i);

    fireEvent.change(inputElement, { target: { value: 'same signal' } });
    const data1 = SignalVisualizer.mock.calls[0][0].data;
    SignalVisualizer.mockClear();

    fireEvent.change(inputElement, { target: { value: 'same signal' } });
    const data2 = SignalVisualizer.mock.calls[0][0].data;

    expect(data1).toEqual(data2);
  });
});
