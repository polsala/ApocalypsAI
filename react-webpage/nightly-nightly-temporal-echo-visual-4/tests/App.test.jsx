import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../src/App';
import { generateEchoes } from '../src/EchoGenerator';

// Mock rationale: We mock the EchoGenerator to ensure deterministic test results
// and to isolate the App component's behavior from the complex logic of echo generation.
// This allows us to test the UI's interaction with the generator without worrying
// about the randomness or specific content of the generated echoes.
jest.mock('../src/EchoGenerator', () => ({
  generateEchoes: jest.fn((phrase) => [
    { type: 'Mock Glitched Echo', text: `Mock Glitch of: ${phrase}` },
    { type: 'Mock Poetic Echo', text: `Mock Poetic take on: ${phrase}` },
  ]),
}));

describe('App Component', () => {
  beforeEach(() => {
    // Clear mock calls before each test
    generateEchoes.mockClear();
  });

  test('renders the main title and input field', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Visualizer/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Enter your phrase or temporal anomaly here.../i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Generate Echoes/i })).toBeInTheDocument();
  });

  test('displays "No echoes yet" initially', () => {
    render(<App />);
    expect(screen.getByText(/No echoes yet\. Enter a phrase to begin\./i)).toBeInTheDocument();
  });

  test('updates input phrase on change', async () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Enter your phrase or temporal anomaly here.../i);
    await userEvent.type(textarea, 'Hello World');
    expect(textarea).toHaveValue('Hello World');
  });

  test('generates and displays echoes when button is clicked with input', async () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Enter your phrase or temporal anomaly here.../i);
    const button = screen.getByRole('button', { name: /Generate Echoes/i });

    await userEvent.type(textarea, 'Test Phrase');
    fireEvent.click(button);

    // Expect generateEchoes to have been called with the input
    expect(generateEchoes).toHaveBeenCalledTimes(1);
    expect(generateEchoes).toHaveBeenCalledWith('Test Phrase');

    // Expect mock echoes to be displayed
    expect(screen.getByText('Mock Glitched Echo')).toBeInTheDocument();
    expect(screen.getByText('Mock Glitch of: Test Phrase')).toBeInTheDocument();
    expect(screen.getByText('Mock Poetic Echo')).toBeInTheDocument();
    expect(screen.getByText('Mock Poetic take on: Test Phrase')).toBeInTheDocument();
    expect(screen.queryByText(/No echoes yet/i)).not.toBeInTheDocument();
  });

  test('does not generate echoes if input is empty', async () => {
    render(<App />);
    const button = screen.getByRole('button', { name: /Generate Echoes/i });

    fireEvent.click(button);

    // Expect generateEchoes not to have been called
    expect(generateEchoes).not.toHaveBeenCalled();
    expect(screen.getByText(/No echoes yet/i)).toBeInTheDocument();
  });

  test('clears echoes if input becomes empty after generation', async () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Enter your phrase or temporal anomaly here.../i);
    const button = screen.getByRole('button', { name: /Generate Echoes/i });

    await userEvent.type(textarea, 'Initial Phrase');
    fireEvent.click(button);

    expect(screen.getByText('Mock Glitched Echo')).toBeInTheDocument();

    // Clear the input
    await userEvent.clear(textarea);
    // Re-click the button (or just rely on state change if it were more reactive)
    // For this specific implementation, clearing input doesn't auto-clear echoes until a new generation attempt.
    // Let's simulate a new generation attempt with empty input.
    fireEvent.click(button); // This will call generateEchoes with empty string, which should return empty array.

    expect(generateEchoes).toHaveBeenCalledWith(''); // Called with empty string
    expect(screen.queryByText('Mock Glitched Echo')).not.toBeInTheDocument();
    expect(screen.getByText(/No echoes yet/i)).toBeInTheDocument();
  });
});
