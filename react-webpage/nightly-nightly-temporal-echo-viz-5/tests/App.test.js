import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import '@testing-library/jest-dom'; // For extended matchers like toBeInTheDocument

// # Mock rationale: The App component directly imports `echoes.json`,
// # making the data source inherently deterministic and offline.
// # No external API calls are made, so no `fetch` or network mocks are needed.

describe('App', () => {
  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Visualizer/i)).toBeInTheDocument();
  });

  test('displays "No echoes found" initially', () => {
    render(<App />);
    expect(screen.getByText(/No echoes found. Try a different keyword!/i)).toBeInTheDocument();
  });

  test('displays echoes for a known keyword', async () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter a keyword/i);
    const buttonElement = screen.getByRole('button', { name: /Find Echoes/i });

    fireEvent.change(inputElement, { target: { value: 'apocalypse' } });
    fireEvent.click(buttonElement);

    // Wait for the echoes to appear.
    // We expect "The Great Fire of London (1666)" to be one of them.
    expect(await screen.findByText(/The Great Fire of London \(1666\)/i)).toBeInTheDocument();
    expect(screen.getByText(/The Tunguska Event \(1908\)/i)).toBeInTheDocument();
    expect(screen.getByText(/Temporal Echoes:/i)).toBeInTheDocument();
  });

  test('displays "No echoes found" for an unknown keyword', async () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter a keyword/i);
    const buttonElement = screen.getByRole('button', { name: /Find Echoes/i });

    fireEvent.change(inputElement, { target: { value: 'nonexistent' } });
    fireEvent.click(buttonElement);

    expect(await screen.findByText(/No echoes found. Try a different keyword!/i)).toBeInTheDocument();
    expect(screen.queryByText(/Temporal Echoes:/i)).not.toBeInTheDocument(); // Ensure the header is gone
  });

  test('clears echoes when input is cleared', async () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter a keyword/i);
    const buttonElement = screen.getByRole('button', { name: /Find Echoes/i });

    fireEvent.change(inputElement, { target: { value: 'hope' } });
    fireEvent.click(buttonElement);
    expect(await screen.findByText(/The first rainbow after a storm/i)).toBeInTheDocument();

    fireEvent.change(inputElement, { target: { value: '' } }); // Clear input
    fireEvent.click(buttonElement); // Click search again (or just let useEffect handle it if input change triggers it)

    // In this setup, useEffect triggers on searchTerm change. If searchTerm becomes empty, it clears echoes.
    // So, just changing the input should be enough.
    expect(await screen.findByText(/No echoes found. Try a different keyword!/i)).toBeInTheDocument();
    expect(screen.queryByText(/The first rainbow after a storm/i)).not.toBeInTheDocument();
  });
});
