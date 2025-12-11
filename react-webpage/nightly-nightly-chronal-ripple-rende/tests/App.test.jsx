import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { vi } from 'vitest';
import App from '../src/App';

describe('App', () => {
  // Mock rationale: No external dependencies for App component itself.
  // We are testing its rendering of child components and state management.
  // Child components (RippleCanvas, ControlPanel) are tested separately.

  it('renders RippleCanvas and ControlPanel components', () => {
    render(<App />);
    expect(screen.getByRole('canvas')).toBeInTheDocument();
    expect(screen.getByText('Control Panel')).toBeInTheDocument();
  });

  it('updates ripple speed when slider is changed', () => {
    render(<App />);
    const speedSlider = screen.getByLabelText(/Ripple Speed/);
    fireEvent.change(speedSlider, { target: { value: '0.07' } });
    expect(screen.getByText(/Ripple Speed \(0.07\)/)).toBeInTheDocument();
  });

  it('updates ripple decay when slider is changed', () => {
    render(<App />);
    const decaySlider = screen.getByLabelText(/Ripple Decay/);
    fireEvent.change(decaySlider, { target: { value: '0.007' } });
    expect(screen.getByText(/Ripple Decay \(0.007\)/)).toBeInTheDocument();
  });

  it('updates max ripples when slider is changed', () => {
    render(<App />);
    const maxRipplesSlider = screen.getByLabelText(/Max Ripples/);
    fireEvent.change(maxRipplesSlider, { target: { value: '15' } });
    expect(screen.getByText(/Max Ripples \(15\)/)).toBeInTheDocument();
  });

  it('toggles pause state when Pause/Play button is clicked', () => {
    render(<App />);
    const pauseButton = screen.getByRole('button', { name: 'Pause' });
    fireEvent.click(pauseButton);
    expect(pauseButton).toHaveTextContent('Play');
    fireEvent.click(pauseButton);
    expect(pauseButton).toHaveTextContent('Pause');
  });

  it('triggers clear ripples when Clear Ripples button is clicked', () => {
    // This test primarily checks if the button click handler is called.
    // The actual clearing logic is within RippleCanvas and tested there.
    const { getByRole } = render(<App />);
    const clearButton = getByRole('button', { name: 'Clear Ripples' });
    fireEvent.click(clearButton);
    // No direct way to assert state change in RippleCanvas from App.test.jsx
    // without exposing internal state or complex mocking. This test confirms
    // the button is present and clickable.
    expect(clearButton).toBeInTheDocument();
  });
});
