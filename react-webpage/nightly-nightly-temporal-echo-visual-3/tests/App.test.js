import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import { mockEchoes } from '../src/data/mockEchoes'; // # Mock rationale: Using internal mock data for deterministic and offline component testing.

describe('App Component', () => {
  test('renders the main title', () => {
    render(<App />);
    const titleElement = screen.getByText(/ApocalypsAI Temporal Echo Visualizer/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders all mock echoes in the grid', () => {
    render(<App />);
    mockEchoes.forEach(echo => {
      const echoItem = screen.getByTitle(echo.description);
      expect(echoItem).toBeInTheDocument();
    });
  });

  test('displays echo details when an echo is clicked', () => {
    render(<App />);
    const firstEcho = mockEchoes[0];
    const echoItem = screen.getByTitle(firstEcho.description);

    fireEvent.click(echoItem);

    // Check if details are displayed
    expect(screen.getByText(/Echo Details/i)).toBeInTheDocument();
    expect(screen.getByText(new RegExp(firstEcho.id, 'i'))).toBeInTheDocument();
    expect(screen.getByText(new RegExp(firstEcho.location, 'i'))).toBeInTheDocument();
    expect(screen.getByText(new RegExp(firstEcho.severity, 'i'))).toBeInTheDocument();
    expect(screen.getByText(new RegExp(firstEcho.type, 'i'))).toBeInTheDocument();
    expect(screen.getByText(new RegExp(firstEcho.description, 'i'))).toBeInTheDocument();
  });

  test('changes selected echo details when a different echo is clicked', () => {
    render(<App />);
    const firstEcho = mockEchoes[0];
    const secondEcho = mockEchoes[1];

    // Click first echo
    fireEvent.click(screen.getByTitle(firstEcho.description));
    expect(screen.getByText(new RegExp(firstEcho.id, 'i'))).toBeInTheDocument();

    // Click second echo
    fireEvent.click(screen.getByTitle(secondEcho.description));
    expect(screen.queryByText(new RegExp(firstEcho.id, 'i'))).not.toBeInTheDocument(); // First echo details should be gone
    expect(screen.getByText(new RegExp(secondEcho.id, 'i'))).toBeInTheDocument(); // Second echo details should be present
  });

  test('initially prompts to select an echo', () => {
    render(<App />);
    expect(screen.getByText(/Select an echo from the grid to see its details./i)).toBeInTheDocument();
  });
});
