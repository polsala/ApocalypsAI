import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: The `generatePalette` function is a pure function
// that deterministically generates colors based on mood. We don't need
// to mock its internal logic, but we can ensure the App component
// correctly calls it and displays its output. For testing purposes,
// we assert against known outputs for specific moods, derived from
// the deterministic color generation logic. We are testing the
// component's rendering and interaction, not the intricate color
// generation algorithm itself, which is a separate unit.

describe('App Component', () => {
  test('renders Nightly Lumina-Loom title', () => {
    render(<App />);
    const titleElement = screen.getByText(/Nightly Lumina-Loom/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('displays default palette for "Scrappy" mood on initial render', () => {
    render(<App />);
    // Expect 5 color swatches to be rendered
    const colorSwatches = screen.getAllByText(/^#/); // Matches any text starting with # (hex codes)
    expect(colorSwatches).toHaveLength(5);

    // Check for a known color from the 'Scrappy' palette (first color generated)
    // This is a deterministic check based on the generatePalette function's logic.
    // The first color for 'Scrappy' (base H=30, S=60, L=40) is #A36629.
    expect(screen.getByText('#A36629')).toBeInTheDocument();
  });

  test('changes palette when a new mood is selected', () => {
    render(<App />);
    const moodSelect = screen.getByLabelText(/Choose your current vibe:/i);

    // Select 'Hope' mood
    fireEvent.change(moodSelect, { target: { value: 'Hope' } });

    // Expect 5 color swatches to be rendered
    const colorSwatches = screen.getAllByText(/^#/);
    expect(colorSwatches).toHaveLength(5);

    // Check for a known color from the 'Hope' palette (first color generated)
    // The first color for 'Hope' (base H=100, S=70, L=60) is #81E052.
    expect(screen.getByText('#81E052')).toBeInTheDocument();

    // Ensure the 'Scrappy' color is no longer present
    expect(screen.queryByText('#A36629')).not.toBeInTheDocument();
  });

  test('displays correct number of color swatches (5) for any selected mood', () => {
    render(<App />);
    const moodSelect = screen.getByLabelText(/Choose your current vibe:/i);

    const moods = ['Despair', 'Hope', 'Scrappy', 'Serene', 'Mysterious'];

    moods.forEach(mood => {
      fireEvent.change(moodSelect, { target: { value: mood } });
      const colorSwatches = screen.getAllByText(/^#/);
      expect(colorSwatches).toHaveLength(5);
    });
  });
});
