import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';
import * as EchoGenerator from '../src/EchoGenerator';

// Mock rationale: We mock the EchoVisualizer component to simplify testing of the App's state and rendering logic.
// This prevents needing to render complex SVG elements in a Jest DOM environment, focusing on App's behavior.
// We also mock EchoGenerator to ensure deterministic parameter generation for testing purposes.
jest.mock('../src/EchoVisualizer', () => {
  return jest.fn(({ params }) => (
    <div data-testid="mock-echo-visualizer">
      {params ? JSON.stringify(params) : 'No params'}
    </div>
  ));
});

describe('App', () => {
  beforeEach(() => {
    // Mock generateEchoParameters to return a consistent value for testing
    jest.spyOn(EchoGenerator, 'generateEchoParameters').mockReturnValue({
      rippleCount: 5,
      baseFrequency: 0.7,
      colorHue: 180,
      distortionMagnitude: 0.5,
      animationSpeed: 1.5,
      seed: 123
    });
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('renders the main heading and input field', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Signature Visualizer/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Type your temporal signature here.../i)).toBeInTheDocument();
  });

  test('displays placeholder text when input is empty', () => {
    render(<App />);
    expect(screen.getByText(/Your echo awaits.../i)).toBeInTheDocument();
    expect(screen.queryByTestId('mock-echo-visualizer')).not.toBeInTheDocument();
  });

  test('calls generateEchoParameters and renders EchoVisualizer when input changes', () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/Type your temporal signature here.../i);
    fireEvent.change(input, { target: { value: 'test input' } });

    expect(EchoGenerator.generateEchoParameters).toHaveBeenCalledWith('test input');
    const visualizer = screen.getByTestId('mock-echo-visualizer');
    expect(visualizer).toBeInTheDocument();
    expect(visualizer).toHaveTextContent(JSON.stringify({
      rippleCount: 5,
      baseFrequency: 0.7,
      colorHue: 180,
      distortionMagnitude: 0.5,
      animationSpeed: 1.5,
      seed: 123
    }));
  });

  test('clears visualizer when input becomes empty', () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/Type your temporal signature here.../i);

    fireEvent.change(input, { target: { value: 'some text' } });
    expect(screen.queryByText(/Your echo awaits.../i)).not.toBeInTheDocument();
    expect(screen.getByTestId('mock-echo-visualizer')).toBeInTheDocument();

    fireEvent.change(input, { target: { value: '' } });
    expect(screen.getByText(/Your echo awaits.../i)).toBeInTheDocument();
    expect(screen.queryByTestId('mock-echo-visualizer')).not.toBeInTheDocument();
  });
});
