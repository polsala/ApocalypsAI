import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import * as SentimentAnalyzer from '../src/SentimentAnalyzer';

describe('App', () => {
  // Mock rationale: The SentimentAnalyzer module is an external dependency for the App component.
  // To ensure deterministic and isolated testing of the React component's UI and state logic,
  // the SentimentAnalyzer.analyze function is mocked. This prevents actual sentiment analysis
  // logic from affecting UI tests and allows specific sentiment outcomes to be simulated.

  beforeEach(() => {
    // Mock the SentimentAnalyzer module before each test
    jest.spyOn(SentimentAnalyzer, 'analyze').mockReturnValue({
      sentiment: 'neutral',
      score: 0,
      description: 'Awaiting input...',
    });
  });

  afterEach(() => {
    // Restore the original implementation after each test
    jest.restoreAllMocks();
  });

  test('renders Nightly Aura Analyzer title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Aura Analyzer/i)).toBeInTheDocument();
  });

  test('renders textarea and initial neutral aura description', () => {
    render(<App />);
    expect(screen.getByPlaceholderText(/Type or paste your message here.../i)).toBeInTheDocument();
    expect(screen.getByText(/Aura: Awaiting input.../i)).toBeInTheDocument();
    const auraContainer = screen.getByRole('main').querySelector('.aura-container');
    expect(auraContainer).toHaveStyle('background: linear-gradient(135deg, #61dafb, #2196f3)'); // Default neutral color
  });

  test('updates aura description and color for positive sentiment', () => {
    SentimentAnalyzer.analyze.mockReturnValue({
      sentiment: 'positive',
      score: 5,
      description: 'Radiant with hope!',
    });

    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type or paste your message here.../i);
    fireEvent.change(textarea, { target: { value: 'This is a great day!' } });

    expect(screen.getByText(/Aura: Radiant with hope!/i)).toBeInTheDocument();
    const auraContainer = screen.getByRole('main').querySelector('.aura-container');
    expect(auraContainer).toHaveStyle('background: linear-gradient(135deg, #a8e063, #56ab2f)'); // Positive color
  });

  test('updates aura description and color for negative sentiment', () => {
    SentimentAnalyzer.analyze.mockReturnValue({
      sentiment: 'negative',
      score: -5,
      description: 'Shadows of despair...',
    });

    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type or paste your message here.../i);
    fireEvent.change(textarea, { target: { value: 'This is a terrible day!' } });

    expect(screen.getByText(/Aura: Shadows of despair.../i)).toBeInTheDocument();
    const auraContainer = screen.getByRole('main').querySelector('.aura-container');
    expect(auraContainer).toHaveStyle('background: linear-gradient(135deg, #ff416c, #ff4b2b)'); // Negative color
  });

  test('updates aura description and color for neutral sentiment after input', () => {
    SentimentAnalyzer.analyze.mockReturnValue({
      sentiment: 'neutral',
      score: 0,
      description: 'Feeling balanced.',
    });

    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type or paste your message here.../i);
    fireEvent.change(textarea, { target: { value: 'The quick brown fox.' } });

    expect(screen.getByText(/Aura: Feeling balanced./i)).toBeInTheDocument();
    const auraContainer = screen.getByRole('main').querySelector('.aura-container');
    expect(auraContainer).toHaveStyle('background: linear-gradient(135deg, #61dafb, #2196f3)'); // Neutral color
  });

  test('textarea value reflects user input', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type or paste your message here.../i);
    fireEvent.change(textarea, { target: { value: 'Hello world' } });
    expect(textarea).toHaveValue('Hello world');
  });
});
