import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import CosmicCompass from '../src/components/CosmicCompass';

// Mock rationale: Math.random is mocked to ensure deterministic scores and locations
// for testing purposes. This prevents tests from failing due to random outcomes.
const mockMath = Object.create(global.Math);
mockMath.random = () => 0.5; // Always returns 0.5 for predictable outcomes
global.Math = mockMath;

describe('CosmicCompass Component', () => {
  test('renders initial state with scan button', () => {
    render(<CosmicCompass />);
    expect(screen.getByText(/Consult the cosmic currents/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Scan for Cosmic Alignment/i })).toBeInTheDocument();
    expect(screen.queryByText(/Cosmic Alignment Score/i)).not.toBeInTheDocument();
  });

  test('shows loading state when scanning', async () => {
    render(<CosmicCompass />);
    const scanButton = screen.getByRole('button', { name: /Scan for Cosmic Alignment/i });
    fireEvent.click(scanButton);
    expect(scanButton).toHaveTextContent('Scanning...');
    expect(scanButton).toBeDisabled();
    // Wait for the simulated async operation to complete
    await waitFor(() => expect(scanButton).not.toBeDisabled()));
  });

  test('displays alignment results after scanning', async () => {
    render(<CosmicCompass />);
    const scanButton = screen.getByRole('button', { name: /Scan for Cosmic Alignment/i });
    fireEvent.click(scanButton);

    await waitFor(() => {
      expect(screen.getByText(/Cosmic Alignment Score: 51\/100/i)).toBeInTheDocument(); // 0.5 * 100 + 1 = 51
      expect(screen.getByText(/A gentle cosmic breeze guides your path./i)).toBeInTheDocument();
      // The recommended location will be the middle one due to Math.random() = 0.5
      expect(screen.getByText(/Recommended Location: The Void-Touched Veranda/i)).toBeInTheDocument();
      expect(screen.getByText(/Coordinates: Lat 51.5074, Lon -0.1278/i)).toBeInTheDocument();
    }, { timeout: 2000 }); // Increased timeout for async wait
  });

  test('MapDisplay receives correct props', async () => {
    render(<CosmicCompass />);
    const scanButton = screen.getByRole('button', { name: /Scan for Cosmic Alignment/i });
    fireEvent.click(scanButton);

    await waitFor(() => {
      const mapDisplay = screen.getByText(/Map Display \(Simulated\):/i);
      expect(mapDisplay).toBeInTheDocument();
      expect(screen.getByText(/Location: The Void-Touched Veranda/i)).toBeInTheDocument();
      expect(screen.getByText(/Coordinates: Lat 51.5074, Lon -0.1278/i)).toBeInTheDocument();
    }, { timeout: 2000 });
  });
});
