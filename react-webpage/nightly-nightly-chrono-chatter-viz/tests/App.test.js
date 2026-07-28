import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../src/App';
import * as echoGenerator from '../src/utils/echoGenerator'; // Import the module to mock it

// Mock rationale: We want to test the App component's rendering and state management
// independently of the complex logic within echoGenerator. This ensures deterministic
// tests and focuses the App.test.js on UI interactions.
jest.mock('../src/utils/echoGenerator', () => ({
  generateEchoes: jest.fn((message) => {
    if (message.trim() === '') return [];
    return [
      { factionName: 'Mock Scavengers', originalMessage: message, echoMessage: `Mocked: ${message} (scav)` },
      { factionName: 'Mock Vault Dwellers', originalMessage: message, echoMessage: `Mocked: ${message} (vault)` },
    ];
  }),
}));

describe('App', () => {
  beforeEach(() => {
    // Clear mock calls before each test
    echoGenerator.generateEchoes.mockClear();
  });

  it('renders the main header', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Chrono-Chatter Visualizer/i)).toBeInTheDocument();
  });

  it('allows user to type into the input field', () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter a short message/i);
    userEvent.type(inputElement, 'Test message');
    expect(inputElement).toHaveValue('Test message');
  });

  it('generates echoes when the button is clicked', async () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter a short message/i);
    const buttonElement = screen.getByRole('button', { name: /Generate Echoes/i });

    userEvent.type(inputElement, 'Hello there');
    fireEvent.click(buttonElement);

    // Wait for the mock function to be called and the UI to update
    await waitFor(() => {
      expect(echoGenerator.generateEchoes).toHaveBeenCalledTimes(1);
      expect(echoGenerator.generateEchoes).toHaveBeenCalledWith('Hello there');
      expect(screen.getByText(/Mock Scavengers/i)).toBeInTheDocument();
      expect(screen.getByText(/Mocked: Hello there \(scav\)/i)).toBeInTheDocument();
      expect(screen.getByText(/Mock Vault Dwellers/i)).toBeInTheDocument();
      expect(screen.getByText(/Mocked: Hello there \(vault\)/i)).toBeInTheDocument();
    });
  });

  it('generates echoes when Enter key is pressed in the input field', async () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter a short message/i);

    userEvent.type(inputElement, 'Another message{enter}');

    await waitFor(() => {
      expect(echoGenerator.generateEchoes).toHaveBeenCalledTimes(1);
      expect(echoGenerator.generateEchoes).toHaveBeenCalledWith('Another message');
      expect(screen.getByText(/Mock Scavengers/i)).toBeInTheDocument();
      expect(screen.getByText(/Mocked: Another message \(scav\)/i)).toBeInTheDocument();
    });
  });

  it('does not generate echoes for empty input', async () => {
    render(<App />);
    const buttonElement = screen.getByRole('button', { name: /Generate Echoes/i });

    fireEvent.click(buttonElement);

    await waitFor(() => {
      expect(echoGenerator.generateEchoes).toHaveBeenCalledWith('');
      expect(screen.queryByText(/Mock Scavengers/i)).not.toBeInTheDocument();
      expect(screen.queryByText(/Mock Vault Dwellers/i)).not.toBeInTheDocument();
    });
  });
});
