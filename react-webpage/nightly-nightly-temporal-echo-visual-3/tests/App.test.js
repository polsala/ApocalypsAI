import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import { generateEchoData } from '../src/EchoGenerator';

// Mock rationale: We mock the EchoGenerator to ensure deterministic test results
// and prevent actual data generation logic from affecting component tests.
jest.mock('../src/EchoGenerator', () => ({
  generateEchoData: jest.fn(() => [
    { offset: -1, intensity: 0.5, distortionType: 'Chronal Ripple' },
    { offset: 0, intensity: 0.8, distortionType: 'Paradox Pulse' },
    { offset: 1, intensity: 0.3, distortionType: 'Void Whisper' },
  ]),
}));

describe('App Component', () => {
  beforeEach(() => {
    // Clear mocks before each test to ensure isolation
    generateEchoData.mockClear();
  });

  test('renders header and input fields', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Visualizer/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Location:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Time:/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Visualize Temporal Echoes/i })).toBeInTheDocument();
  });

  test('shows placeholder text initially', () => {
    render(<App />);
    expect(screen.getByText(/Enter location and time to visualize echoes./i)).toBeInTheDocument();
  });

  test('calls generateEchoData and renders EchoVisualizer on button click with valid inputs', () => {
    render(<App />);

    const locationInput = screen.getByLabelText(/Location:/i);
    const timeInput = screen.getByLabelText(/Time:/i);
    const visualizeButton = screen.getByRole('button', { name: /Visualize Temporal Echoes/i });

    fireEvent.change(locationInput, { target: { value: 'Test Location' } });
    fireEvent.change(timeInput, { target: { value: '2023-01-01T12:00' } });
    fireEvent.click(visualizeButton);

    expect(generateEchoData).toHaveBeenCalledWith('Test Location', '2023-01-01T12:00');
    expect(screen.queryByText(/Enter location and time to visualize echoes./i)).not.toBeInTheDocument();
    expect(screen.getByText(/Offset: -1s, Intensity: 0.50, Type: Chronal Ripple/i)).toBeInTheDocument(); // Checks title of first echo bar
  });

  test('shows alert if location is missing', () => {
    const alertMock = jest.spyOn(window, 'alert').mockImplementation(() => {});
    render(<App />);

    const timeInput = screen.getByLabelText(/Time:/i);
    const visualizeButton = screen.getByRole('button', { name: /Visualize Temporal Echoes/i });

    fireEvent.change(timeInput, { target: { value: '2023-01-01T12:00' } });
    fireEvent.click(visualizeButton);

    expect(alertMock).toHaveBeenCalledWith('Please enter both location and time.');
    expect(generateEchoData).not.toHaveBeenCalled();
    alertMock.mockRestore();
  });

  test('shows alert if time is missing', () => {
    const alertMock = jest.spyOn(window, 'alert').mockImplementation(() => {});
    render(<App />);

    const locationInput = screen.getByLabelText(/Location:/i);
    const visualizeButton = screen.getByRole('button', { name: /Visualize Temporal Echoes/i });

    fireEvent.change(locationInput, { target: { value: 'Test Location' } });
    fireEvent.click(visualizeButton);

    expect(alertMock).toHaveBeenCalledWith('Please enter both location and time.');
    expect(generateEchoData).not.toHaveBeenCalled();
    alertMock.mockRestore();
  });
});
