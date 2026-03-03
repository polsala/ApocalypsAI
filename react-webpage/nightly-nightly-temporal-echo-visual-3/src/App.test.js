import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';
import * as EchoGenerator from './EchoGenerator'; // Import all exports as an object

describe('App', () => {
  // Mock rationale: The `generateEchoes` function uses `Math.random()`, making its output non-deterministic.
  // To ensure deterministic and reliable tests for the `App` component's behavior (i.e., that it calls
  // `generateEchoes` and displays its results), we mock the `generateEchoes` function to return a fixed,
  // predictable set of echoes. This isolates the `App` component's rendering logic from the echo generation logic.
  beforeEach(() => {
    jest.spyOn(EchoGenerator, 'generateEchoes').mockReturnValue([
      'Mock Echo 1',
      'Mock Echo 2',
      'Mock Echo 3',
      'Mock Echo 4',
      'Mock Echo 5',
      'Mock Echo 6'
    ]);
  });

  afterEach(() => {
    jest.restoreAllMocks(); // Clean up mocks after each test
  });

  test('renders Temporal Echo Visualizer header', () => {
    render(<App />);
    const headerElement = screen.getByText(/Temporal Echo Visualizer/i);
    expect(headerElement).toBeInTheDocument();
  });

  test('input field and button are present', () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter your phrase here.../i);
    const buttonElement = screen.getByRole('button', { name: /Generate Echoes/i });
    expect(inputElement).toBeInTheDocument();
    expect(buttonElement).toBeInTheDocument();
  });

  test('typing into input updates its value', () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter your phrase here.../i);
    fireEvent.change(inputElement, { target: { value: 'hello world' } });
    expect(inputElement.value).toBe('hello world');
  });

  test('clicking button generates echoes and displays them', () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter your phrase here.../i);
    const buttonElement = screen.getByRole('button', { name: /Generate Echoes/i });

    fireEvent.change(inputElement, { target: { value: 'test phrase' } });
    fireEvent.click(buttonElement);

    // Check if the mock echoes are rendered
    expect(screen.getByText('Mock Echo 1')).toBeInTheDocument();
    expect(screen.getByText('Mock Echo 2')).toBeInTheDocument();
    expect(screen.getByText('Mock Echo 3')).toBeInTheDocument();
    expect(screen.getByText('Mock Echo 4')).toBeInTheDocument();
    expect(screen.getByText('Mock Echo 5')).toBeInTheDocument();
    expect(screen.getByText('Mock Echo 6')).toBeInTheDocument();

    // Also verify that generateEchoes was called with the correct phrase
    expect(EchoGenerator.generateEchoes).toHaveBeenCalledWith('test phrase', 6);
  });

  test('no echoes displayed initially', () => {
    render(<App />);
    const echoItems = screen.queryAllByText(/Mock Echo/i);
    expect(echoItems).toHaveLength(0);
  });
});
