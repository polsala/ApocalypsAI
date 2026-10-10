// tests/App.test.js
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import EchoGenerator from '../src/EchoGenerator';

// Mock rationale: We want to test the App component's rendering and interaction logic
// independently of the complex, deterministic string manipulation logic in EchoGenerator.
// By mocking EchoGenerator, we ensure that our App tests are fast, predictable, and
// isolated from potential changes or bugs in the echo generation itself.
jest.mock('../src/EchoGenerator', () => ({
  generateEchoes: jest.fn((phrase) => {
    if (phrase.trim() === '') {
      return {
        wasteland: '',
        verdant: '',
        cybernetic: '',
      };
    }
    return {
      wasteland: `Wasteland echo of: ${phrase}`,
      verdant: `Verdant echo of: ${phrase}`,
      cybernetic: `Cybernetic echo of: ${phrase}`,
    };
  }),
}));

describe('App', () => {
  beforeEach(() => {
    // Clear mock calls before each test
    EchoGenerator.generateEchoes.mockClear();
  });

  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Chamber Visualizer/i)).toBeInTheDocument();
  });

  test('displays initial placeholder messages', () => {
    render(<App />);
    expect(screen.getAllByText(/Enter a phrase to hear its echo...|A desolate silence...|Nature's gentle hum...|Static in the data stream.../i).length).toBeGreaterThanOrEqual(3);
  });

  test('updates input value on change', () => {
    render(<App />);
    const inputElement = screen.getByLabelText(/Phrase input/i);
    fireEvent.change(inputElement, { target: { value: 'Test phrase' } });
    expect(inputElement.value).toBe('Test phrase');
  });

  test('calls EchoGenerator and displays echoes when "Echo!" button is clicked', () => {
    render(<App />);
    const inputElement = screen.getByLabelText(/Phrase input/i);
    const buttonElement = screen.getByRole('button', { name: /Echo!/i });

    fireEvent.change(inputElement, { target: { value: 'Hello' } });
    fireEvent.click(buttonElement);

    expect(EchoGenerator.generateEchoes).toHaveBeenCalledTimes(1);
    expect(EchoGenerator.generateEchoes).toHaveBeenCalledWith('Hello');

    expect(screen.getByText('Wasteland echo of: Hello')).toBeInTheDocument();
    expect(screen.getByText('Verdant echo of: Hello')).toBeInTheDocument();
    expect(screen.getByText('Cybernetic echo of: Hello')).toBeInTheDocument();
  });

  test('displays default messages if input is empty and button is clicked', () => {
    render(<App />);
    const inputElement = screen.getByLabelText(/Phrase input/i);
    const buttonElement = screen.getByRole('button', { name: /Echo!/i });

    // Ensure input is empty
    fireEvent.change(inputElement, { target: { value: '' } });
    fireEvent.click(buttonElement);

    expect(EchoGenerator.generateEchoes).toHaveBeenCalledTimes(0); // Should not call generator for empty input
    expect(screen.getAllByText(/Enter a phrase to hear its echo.../i).length).toBe(3);
  });

  test('clears previous echoes when new input is processed', () => {
    render(<App />);
    const inputElement = screen.getByLabelText(/Phrase input/i);
    const buttonElement = screen.getByRole('button', { name: /Echo!/i });

    // First input
    fireEvent.change(inputElement, { target: { value: 'First' } });
    fireEvent.click(buttonElement);
    expect(screen.getByText('Wasteland echo of: First')).toBeInTheDocument();

    // Second input
    fireEvent.change(inputElement, { target: { value: 'Second' } });
    fireEvent.click(buttonElement);
    expect(screen.queryByText('Wasteland echo of: First')).not.toBeInTheDocument();
    expect(screen.getByText('Wasteland echo of: Second')).toBeInTheDocument();
  });
});
