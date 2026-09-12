import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

describe('App', () => {
  test('renders Chrono-Ripple Visualizer title', () => {
    render(<App />);
    expect(screen.getByText(/Chrono-Ripple Visualizer/i)).toBeInTheDocument();
  });

  test('renders the form and canvas components', () => {
    render(<App />);
    expect(screen.getByLabelText(/Event Date:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Description:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Magnitude:/i)).toBeInTheDocument();
    expect(screen.getByRole('canvas', { name: /Chrono Ripple Visualization/i })).toBeInTheDocument();
  });

  test('updates event summary after form submission', () => {
    render(<App />);
    const descriptionInput = screen.getByLabelText(/Description:/i);
    const magnitudeSlider = screen.getByLabelText(/Magnitude: \d+/i);
    const visualizeButton = screen.getByRole('button', { name: /Visualize Ripples/i });

    fireEvent.change(descriptionInput, { target: { value: 'Temporal Anomaly Detected' } });
    fireEvent.change(magnitudeSlider, { target: { value: '8' } });
    fireEvent.click(visualizeButton);

    expect(screen.getByText(/Event: "Temporal Anomaly Detected"/i)).toBeInTheDocument();
    expect(screen.getByText(/Magnitude: 8/i)).toBeInTheDocument();
  });
});
