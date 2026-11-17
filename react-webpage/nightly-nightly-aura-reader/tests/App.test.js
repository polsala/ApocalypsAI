import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';
import * as sentimentAnalyzer from '../src/sentimentAnalyzer';

// Mock rationale: The sentiment analysis logic is external to the React component's rendering logic.
// Mocking it ensures that tests for the App component are deterministic and do not rely on the
// specific implementation details or potential complexities of the sentiment analysis itself.
// This allows us to test how the UI reacts to different sentiment outcomes (positive, negative, neutral)
// without actually performing a full sentiment analysis in the test environment.
jest.mock('../src/sentimentAnalyzer', () => ({
  analyzeSentiment: jest.fn((text) => {
    if (text.toLowerCase().includes('happy')) return 1;
    if (text.toLowerCase().includes('error')) return -1;
    return 0;
  }),
}));

describe('App Component', () => {
  beforeEach(() => {
    // Clear mock calls before each test
    sentimentAnalyzer.analyzeSentiment.mockClear();
  });

  test('renders the main title and subtitle', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Aura Reader/i)).toBeInTheDocument();
    expect(screen.getByText(/Unveil the emotional essence of your text./i)).toBeInTheDocument();
  });

  test('textarea updates its value on change', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Enter text here.../i);
    fireEvent.change(textarea, { target: { value: 'This is a test message.' } });
    expect(textarea.value).toBe('This is a test message.');
  });

  test('clicking "Read Aura" button calls analyzeSentiment with current text', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Enter text here.../i);
    const button = screen.getByText(/Read Aura/i);

    fireEvent.change(textarea, { target: { value: 'Everything is happy and good.' } });
    fireEvent.click(button);

    expect(sentimentAnalyzer.analyzeSentiment).toHaveBeenCalledTimes(1);
    expect(sentimentAnalyzer.analyzeSentiment).toHaveBeenCalledWith('Everything is happy and good.');
  });

  test('AuraDisplay shows positive sentiment for happy text', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Enter text here.../i);
    const button = screen.getByText(/Read Aura/i);

    fireEvent.change(textarea, { target: { value: 'I am so happy today!' } });
    fireEvent.click(button);

    // Check if AuraDisplay received the correct sentiment prop
    // This requires inspecting the style of the AuraDisplay component.
    // We'll check for a characteristic style of positive sentiment.
    const auraDisplay = screen.getByTestId('aura-display'); // Add data-testid to AuraDisplay for easier selection
    expect(auraDisplay).toHaveStyle('background: linear-gradient(45deg, #a8e063, #56ab2f)');
  });

  test('AuraDisplay shows negative sentiment for error text', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Enter text here.../i);
    const button = screen.getByText(/Read Aura/i);

    fireEvent.change(textarea, { target: { value: 'There was an error in the system.' } });
    fireEvent.click(button);

    const auraDisplay = screen.getByTestId('aura-display');
    expect(auraDisplay).toHaveStyle('background: linear-gradient(45deg, #ff416c, #ff4b2b)');
  });

  test('AuraDisplay shows neutral sentiment for ambiguous text', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Enter text here.../i);
    const button = screen.getByText(/Read Aura/i);

    fireEvent.change(textarea, { target: { value: 'The system processed the request.' } });
    fireEvent.click(button);

    const auraDisplay = screen.getByTestId('aura-display');
    expect(auraDisplay).toHaveStyle('background: linear-gradient(45deg, #4facfe, #00f2fe)');
  });
});

// --- Add data-testid to AuraDisplay for testing purposes ---
// In src/AuraDisplay.js, modify the return statement to include data-testid:
// <div style={auraStyle} data-testid="aura-display"></div>
