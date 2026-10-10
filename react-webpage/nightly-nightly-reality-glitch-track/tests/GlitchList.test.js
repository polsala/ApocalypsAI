import { render, screen } from '@testing-library/react';
import GlitchList from '../src/components/GlitchList';

describe('GlitchList Component', () => {
  test('renders "No glitches reported yet" message when glitches array is empty', () => {
    render(<GlitchList glitches={[]} />);
    expect(screen.getByText(/No glitches reported yet\. All clear\.\.\. for now\./i)).toBeInTheDocument();
  });

  test('renders a list of glitches when provided', () => {
    // Mock rationale: Using static test data for glitches to ensure deterministic rendering.
    const testGlitches = [
      { id: 1, description: 'Test Glitch 1', type: 'Object Displacement', timestamp: '1/1/2023, 10:00:00 AM' },
      { id: 2, description: 'Test Glitch 2', type: 'Time Skip', timestamp: '1/2/2023, 11:00:00 AM' },
    ];
    render(<GlitchList glitches={testGlitches} />);

    expect(screen.getByText(/Reported Glitches/i)).toBeInTheDocument();
    expect(screen.getByText(/Test Glitch 1/i)).toBeInTheDocument();
    expect(screen.getByText(/Object Displacement/i)).toBeInTheDocument();
    expect(screen.getByText(/Reported: 1\/1\/2023, 10:00:00 AM/i)).toBeInTheDocument();

    expect(screen.getByText(/Test Glitch 2/i)).toBeInTheDocument();
    expect(screen.getByText(/Time Skip/i)).toBeInTheDocument();
    expect(screen.getByText(/Reported: 1\/2\/2023, 11:00:00 AM/i)).toBeInTheDocument();

    expect(screen.queryByText(/No glitches reported yet/i)).not.toBeInTheDocument();
  });
});
