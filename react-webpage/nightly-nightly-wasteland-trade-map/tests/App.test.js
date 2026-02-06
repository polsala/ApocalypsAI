import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: We are testing the React component's rendering and interaction logic,
// not the actual pathfinding algorithm itself. The graph utility is tested separately.
// We'll mock the prompt for location naming.
const mockPrompt = jest.fn();
const originalPrompt = window.prompt;

beforeAll(() => {
  window.prompt = mockPrompt;
});

afterAll(() => {
  window.prompt = originalPrompt;
});

describe('App Component', () => {
  test('renders main heading', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Wasteland Trade Map/i)).toBeInTheDocument();
  });

  test('allows adding a new location by clicking map cell', async () => {
    mockPrompt.mockReturnValueOnce('Test Oasis');
    render(<App />);

    const cell = screen.getAllByRole('graphics-document')[0]; // First SVG rect cell
    fireEvent.click(cell);

    await waitFor(() => {
      expect(mockPrompt).toHaveBeenCalledWith('Name your new resource location at (0,0):');
      expect(screen.getByText('T')).toBeInTheDocument(); // Initial of 'Test Oasis'
      expect(screen.getByText(/Test Oasis \(0,0\)/i)).toBeInTheDocument(); // In dropdown
    });
  });

  test('allows selecting start and end locations and calculating route', async () => {
    mockPrompt.mockReturnValueOnce('Start Point');
    mockPrompt.mockReturnValueOnce('End Point');
    render(<App />);

    // Add Start Point at (0,0)
    fireEvent.click(screen.getAllByRole('graphics-document')[0]);

    // Add End Point at (0,1)
    fireEvent.click(screen.getAllByRole('graphics-document')[1]);

    // Select Start Point
    fireEvent.change(screen.getByLabelText(/Start Location:/i), {
      target: { value: '1' }, // Assuming ID 1 for 'Start Point'
    });
    expect(screen.getByLabelText(/Start Location:/i).value).toBe('1');

    // Select End Point
    fireEvent.change(screen.getByLabelText(/End Location:/i), {
      target: { value: '2' }, // Assuming ID 2 for 'End Point'
    });
    expect(screen.getByLabelText(/End Location:/i).value).toBe('2');

    // Calculate route
    fireEvent.click(screen.getByRole('button', { name: /Calculate Route/i }));

    await waitFor(() => {
      expect(screen.getByText(/Total Route Risk Cost:/i)).toBeInTheDocument();
      // The exact cost depends on risk zones, but we expect it to be a number
      expect(screen.getByText(/Total Route Risk Cost: \d+/i)).toBeInTheDocument();
    });
  });

  test('allows removing a location by clicking its marker', async () => {
    mockPrompt.mockReturnValueOnce('Location to Remove');
    render(<App />);

    // Add location at (0,0)
    fireEvent.click(screen.getAllByRole('graphics-document')[0]);

    await waitFor(() => {
      expect(screen.getByText('L')).toBeInTheDocument();
    });

    // Click the marker to remove it
    fireEvent.click(screen.getByText('L'));

    await waitFor(() => {
      expect(screen.queryByText('L')).not.toBeInTheDocument();
      expect(screen.queryByText(/Location to Remove/i)).not.toBeInTheDocument();
    });
  });
});
