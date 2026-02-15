import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../src/App'; // Test the App component which contains EchoVisualizer

// Mock rationale: The temporal echo generation is a deterministic simulation
// within the App component. No external APIs or non-deterministic functions
// are called that would require mocking beyond the component itself.
// The simulation logic is self-contained and produces predictable output
// based on the input 'temporalCoordinate'.

describe('Temporal Echo Visualizer App', () => {
  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Visualizer/i)).toBeInTheDocument();
  });

  test('displays initial message when no echoes are generated', () => {
    render(<App />);
    expect(screen.getByText(/Enter a coordinate and generate echoes to see the temporal ripples./i)).toBeInTheDocument();
  });

  test('allows user to input a temporal coordinate', async () => {
    render(<App />);
    const input = screen.getByLabelText(/Temporal Coordinate:/i);
    await userEvent.type(input, 'Test Event');
    expect(input).toHaveValue('Test Event');
  });

  test('generates and displays echoes after button click', async () => {
    render(<App />);
    const input = screen.getByLabelText(/Temporal Coordinate:/i);
    const button = screen.getByRole('button', { name: /Generate Echoes/i });

    await userEvent.type(input, 'Test Event');
    await userEvent.click(button);

    // After generating, the initial message should be gone
    expect(screen.queryByText(/Enter a coordinate and generate echoes to see the temporal ripples./i)).not.toBeInTheDocument();

    // Check for the presence of echo bars (based on the simulated output logic)
    // The simulation creates 3-5 echoes. We can check for at least one.
    expect(screen.getByText(/Temporal Echoes/i)).toBeInTheDocument();
    // Check for specific distortion types that should appear
    expect(screen.getAllByText(/Ripple|Warp|Flicker|Phase Shift/i).length).toBeGreaterThanOrEqual(3);
  });

  test('generates different echoes for different inputs', async () => {
    render(<App />);
    const input = screen.getByLabelText(/Temporal Coordinate:/i);
    const button = screen.getByRole('button', { name: /Generate Echoes/i });

    // First input
    await userEvent.type(input, 'Event A');
    await userEvent.click(button);
    const echoesA = screen.getAllByText(/Ripple|Warp|Flicker|Phase Shift/i).map(el => el.textContent);

    // Clear input and enter second
    await userEvent.clear(input);
    await userEvent.type(input, 'Event B');
    await userEvent.click(button);
    const echoesB = screen.getAllByText(/Ripple|Warp|Flicker|Phase Shift/i).map(el => el.textContent);

    // The simulation is deterministic based on the coordinate, so different inputs should yield different (or at least differently ordered/typed) echoes.
    // A simple check is that the number of echoes might differ, or the types.
    // Given the seed logic, the number of echoes will likely be different for 'A' vs 'B'.
    expect(echoesA.length).not.toBe(echoesB.length); // This is a strong indicator of different simulation output.
  });
});
