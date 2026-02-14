import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../src/App';
import * as voidSentiment from '../src/utils/voidSentiment'; // Import the module

// Mock rationale: We mock the sentiment analysis function to ensure tests are deterministic
// and do not rely on the actual (whimsical) implementation details or any potential randomness
// if it were to be introduced. This allows us to control the output for predictable testing.
jest.mock('../src/utils/voidSentiment', () => ({
  analyzeVoidSentiment: jest.fn((text) => {
    if (text.toLowerCase().includes('hope')) {
      return { hope: 8, despair: 1, whimsy: 2, dread: 1 };
    }
    if (text.toLowerCase().includes('doom')) {
      return { hope: 1, despair: 9, whimsy: 1, dread: 7 };
    }
    if (text.toLowerCase().includes('banana')) {
      return { hope: 3, despair: 0, whimsy: 10, dread: 0 };
    }
    return { hope: 2, despair: 2, whimsy: 2, dread: 2 }; // Default
  }),
}));

describe('App', () => {
  beforeEach(() => {
    // Clear mock calls before each test
    voidSentiment.analyzeVoidSentiment.mockClear();
  });

  test('renders the main title and input elements', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Void Whispers Visualizer/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Type your message to the Void here.../i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Analyze Whispers/i })).toBeInTheDocument();
  });

  test('updates input text on change', async () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type your message to the Void here.../i);
    await userEvent.type(textarea, 'Hello Void');
    expect(textarea).toHaveValue('Hello Void');
  });

  test('calls analyzeVoidSentiment and displays results on button click', async () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type your message to the Void here.../i);
    const button = screen.getByRole('button', { name: /Analyze Whispers/i });

    await userEvent.type(textarea, 'I bring hope');
    fireEvent.click(button);

    expect(voidSentiment.analyzeVoidSentiment).toHaveBeenCalledTimes(1);
    expect(voidSentiment.analyzeVoidSentiment).toHaveBeenCalledWith('I bring hope');

    // Check if sentiment display is rendered with mocked values
    expect(await screen.findByText(/Void's Whispers:/i)).toBeInTheDocument();
    expect(screen.getByText(/Hope:/i)).toBeInTheDocument();
    expect(screen.getByText('8.00')).toBeInTheDocument(); // From mock
    expect(screen.getByText(/Despair:/i)).toBeInTheDocument();
    expect(screen.getByText('1.00')).toBeInTheDocument(); // From mock
  });

  test('displays different sentiment for different inputs', async () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type your message to the Void here.../i);
    const button = screen.getByRole('button', { name: /Analyze Whispers/i });

    await userEvent.type(textarea, 'Impending doom');
    fireEvent.click(button);

    expect(voidSentiment.analyzeVoidSentiment).toHaveBeenCalledWith('Impending doom');
    expect(await screen.findByText(/Void's Whispers:/i)).toBeInTheDocument();
    expect(screen.getByText(/Despair:/i)).toBeInTheDocument();
    expect(screen.getByText('9.00')).toBeInTheDocument(); // From mock
    expect(screen.getByText(/Dread:/i)).toBeInTheDocument();
    expect(screen.getByText('7.00')).toBeInTheDocument(); // From mock

    // Clear input and try another
    fireEvent.change(textarea, { target: { value: '' } }); // Clear previous input
    await userEvent.type(textarea, 'A silly banana');
    fireEvent.click(button);

    expect(voidSentiment.analyzeVoidSentiment).toHaveBeenCalledWith('A silly banana');
    expect(screen.getByText(/Whimsy:/i)).toBeInTheDocument();
    expect(screen.getByText('10.00')).toBeInTheDocument(); // From mock
  });

  test('does not display sentiment before analysis', () => {
    render(<App />);
    expect(screen.queryByText(/Void's Whispers:/i)).not.toBeInTheDocument();
  });
});
