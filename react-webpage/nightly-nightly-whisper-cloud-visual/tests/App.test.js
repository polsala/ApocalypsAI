import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: No external dependencies or complex state management requiring mocks beyond standard React testing utilities.
// We are testing the component's rendering and state updates based on user interaction.

describe('App', () => {
  test('renders the main heading', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Whisper Cloud Visualizer/i)).toBeInTheDocument();
  });

  test('renders the textarea and button', () => {
    render(<App />);
    expect(screen.getByPlaceholderText(/Paste your wasteland whispers/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Generate Whispers/i })).toBeInTheDocument();
  });

  test('displays "No whispers yet" initially', () => {
    render(<App />);
    expect(screen.getByText(/No whispers yet. Type something above!/i)).toBeInTheDocument();
  });

  test('processes text and displays word cloud', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your wasteland whispers/i);
    const button = screen.getByRole('button', { name: /Generate Whispers/i });

    fireEvent.change(textarea, { target: { value: 'The quick brown fox jumps over the lazy dog. Fox, fox, fox!' } });
    fireEvent.click(button);

    expect(screen.queryByText(/No whispers yet/i)).not.toBeInTheDocument();
    expect(screen.getByText('fox')).toBeInTheDocument();
    expect(screen.getByText('quick')).toBeInTheDocument();
    expect(screen.getByText('brown')).toBeInTheDocument();
    expect(screen.getByText('jumps')).toBeInTheDocument();
    expect(screen.getByText('lazy')).toBeInTheDocument();
    expect(screen.getByText('dog')).toBeInTheDocument();

    const foxWord = screen.getByText('fox');
    const quickWord = screen.getByText('quick');

    expect(foxWord).toHaveStyle('font-size: 3em');
    expect(quickWord).toHaveStyle('font-size: 1.6666666666666667em');
  });

  test('handles empty input gracefully', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your wasteland whispers/i);
    const button = screen.getByRole('button', { name: /Generate Whispers/i });

    fireEvent.change(textarea, { target: { value: '   ' } }); // Empty string with spaces
    fireEvent.click(button);

    expect(screen.getByText(/No whispers yet. Type something above!/i)).toBeInTheDocument();
    expect(screen.queryByText('fox')).not.toBeInTheDocument(); // Ensure no old words linger
  });

  test('filters stop words and short words', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your wasteland whispers/i);
    const button = screen.getByRole('button', { name: /Generate Whispers/i });

    fireEvent.change(textarea, { target: { value: 'a the is and but of in on at for with as by from up down out off over under again further then once here there when where why how all any both each few more most other some such no nor not only own same so than too very s t can will just don should now about into through during before after above below between among across along around behind below beneath beside between beyond during except for from inside into near off on onto out outside over past round since through to under until up upon with within without i me my myself we our ours ourselves you your yours yourself yourselves he him his himself she her hers herself it its itself they them their theirs themselves what which who whom this that these those am is are was were be been being have has had having do does did doing would should could ought i\'m you\'re he\'s she\'s it\'s we\'re they\'re i\'ve you\'ve we\'ve they\'ve i\'d you\'d he\'d she\'d we\'d they\'d i\'ll you\'ll he\'ll she\'ll we\'ll they\'ll isn\'t aren\'t wasn\'t weren\'t hasn\'t haven\'t hadn\'t doesn\'t don\'t didn\'t won\'t wouldn\'t shan\'t shouldn\'t can\'t cannot couldn\'t mustn\'t let\'s that\'s who\'s what\'s here\'s there\'s when\'s where\'s why\'s how\'s d ll m o re ve y ain aren couldn didn doesn hadn hasn haven isn ma mightn mustn needn shan shouldn wasn weren won wouldn and also a short word' } });
    fireEvent.click(button);

    expect(screen.queryByText('a')).not.toBeInTheDocument();
    expect(screen.queryByText('the')).not.toBeInTheDocument();
    expect(screen.queryByText('is')).not.toBeInTheDocument();
    expect(screen.queryByText('short')).toBeInTheDocument(); // 'short' is length 5, not a stop word
    expect(screen.queryByText('word')).toBeInTheDocument(); // 'word' is length 4, not a stop word
  });

  test('handles punctuation correctly', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your wasteland whispers/i);
    const button = screen.getByRole('button', { name: /Generate Whispers/i });

    fireEvent.change(textarea, { target: { value: 'Hello, world! How are you? World-class.' } });
    fireEvent.click(button);

    expect(screen.getByText('hello')).toBeInTheDocument();
    expect(screen.getByText('world')).toBeInTheDocument();
    expect(screen.getByText('world-class')).not.toBeInTheDocument(); // Should be 'worldclass' after punctuation removal and space replacement
    expect(screen.getByText('worldclass')).toBeInTheDocument(); // Test for combined word
  });

  test('word sizes reflect frequency accurately', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your wasteland whispers/i);
    const button = screen.getByRole('button', { name: /Generate Whispers/i });

    fireEvent.change(textarea, { target: { value: 'apple banana apple orange apple banana' } });
    fireEvent.click(button);

    const appleWord = screen.getByText('apple'); // Count 3
    const bananaWord = screen.getByText('banana'); // Count 2
    const orangeWord = screen.getByText('orange'); // Count 1

    // Max frequency is 3 (apple)
    // apple: 1 + (3/3)*2 = 3em
    // banana: 1 + (2/3)*2 = 1 + 1.333... = 2.333...em
    // orange: 1 + (1/3)*2 = 1 + 0.666... = 1.666...em

    expect(appleWord).toHaveStyle('font-size: 3em');
    expect(bananaWord).toHaveStyle('font-size: 2.3333333333333335em');
    expect(orangeWord).toHaveStyle('font-size: 1.6666666666666667em');
  });
});
