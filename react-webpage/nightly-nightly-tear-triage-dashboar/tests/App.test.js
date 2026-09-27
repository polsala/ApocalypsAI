import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: We are testing the React component's rendering and state management,
// not actual browser drag-and-drop events or external API calls. Mocking allows
// deterministic and offline testing of component logic.

describe('App Component', () => {
  test('renders the main dashboard title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Temporal Tear Triage Dashboard/i)).toBeInTheDocument();
  });

  test('renders initial temporal tears in their correct columns', () => {
    render(<App />);

    // Check 'Detected' column
    const detectedColumn = screen.getByTestId('triage-column-Detected');
    expect(detectedColumn).toHaveTextContent('Minor Chronal Ripple');
    expect(detectedColumn).toHaveTextContent('Localized Time Loop');
    expect(detectedColumn).toHaveTextContent('Paradoxical Pocket Dimension');

    // Check 'Investigating' column
    const investigatingColumn = screen.getByTestId('triage-column-Investigating');
    expect(investigatingColumn).toHaveTextContent('Echo of a Forgotten Tuesday');

    // Check 'Stabilized' column
    const stabilizedColumn = screen.getByTestId('triage-column-Stabilized');
    expect(stabilizedColumn).toHaveTextContent('Temporal Echo Cascade');
  });

  test('allows dragging a tear from Detected to Investigating column', () => {
    render(<App />);

    const tearCard = screen.getByTestId('tear-card-001'); // Minor Chronal Ripple
    const detectedColumn = screen.getByTestId('triage-column-Detected');
    const investigatingColumn = screen.getByTestId('triage-column-Investigating');

    // Simulate drag start
    fireEvent.dragStart(tearCard, {
      dataTransfer: { setData: jest.fn() }
    });
    expect(tearCard).toHaveAttribute('draggable', 'true');

    // Simulate drop on Investigating column
    fireEvent.drop(investigatingColumn, {
      dataTransfer: { getData: jest.fn().mockReturnValue('tear-001') }
    });

    // Assert that the tear is no longer in the Detected column
    expect(detectedColumn).not.toHaveTextContent('Minor Chronal Ripple');
    // Assert that the tear is now in the Investigating column
    expect(investigatingColumn).toHaveTextContent('Minor Chronal Ripple');
  });

  test('allows dragging a tear from Investigating to Stabilized column', () => {
    render(<App />);

    const tearCard = screen.getByTestId('tear-card-003'); // Echo of a Forgotten Tuesday
    const investigatingColumn = screen.getByTestId('triage-column-Investigating');
    const stabilizedColumn = screen.getByTestId('triage-column-Stabilized');

    // Simulate drag start
    fireEvent.dragStart(tearCard, {
      dataTransfer: { setData: jest.fn() }
    });

    // Simulate drop on Stabilized column
    fireEvent.drop(stabilizedColumn, {
      dataTransfer: { getData: jest.fn().mockReturnValue('tear-003') }
    });

    // Assert that the tear is no longer in the Investigating column
    expect(investigatingColumn).not.toHaveTextContent('Echo of a Forgotten Tuesday');
    // Assert that the tear is now in the Stabilized column
    expect(stabilizedColumn).toHaveTextContent('Echo of a Forgotten Tuesday');
  });
});
