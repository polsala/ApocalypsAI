import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// Mock rationale: Mock localStorage to ensure tests are deterministic and isolated.
// This prevents tests from interfering with actual browser storage or relying on its presence.
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: jest.fn((key) => store[key] || null),
    setItem: jest.fn((key, value) => { store[key] = value.toString(); }),
    clear: jest.fn(() => { store = {}; }),
    removeItem: jest.fn((key) => { delete store[key]; })
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Mock rationale: Mock window.alert to prevent it from blocking tests and to allow
// us to assert if it was called with the correct message.
const mockAlert = jest.fn();
Object.defineProperty(window, 'alert', { value: mockAlert });

describe('App', () => {
  beforeEach(() => {
    localStorageMock.clear(); // Clear storage before each test
    mockAlert.mockClear(); // Clear alert mock before each test
  });

  test('renders the main title and initial dust count', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Cosmic Dust Collector/i)).toBeInTheDocument();
    expect(screen.getByText(/Cosmic Dust Collected: 0/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Collect Cosmic Dust/i })).toBeInTheDocument();
  });

  test('collecting dust increases the count', () => {
    render(<App />);
    const collectButton = screen.getByRole('button', { name: /Collect Cosmic Dust/i });

    fireEvent.click(collectButton);
    expect(screen.getByText(/Cosmic Dust Collected: 1/i)).toBeInTheDocument();

    fireEvent.click(collectButton);
    expect(screen.getByText(/Cosmic Dust Collected: 2/i)).toBeInTheDocument();
  });

  test('dust count persists across renders (simulated by re-rendering)', () => {
    render(<App />);
    const collectButton = screen.getByRole('button', { name: /Collect Cosmic Dust/i });

    fireEvent.click(collectButton);
    fireEvent.click(collectButton);
    expect(screen.getByText(/Cosmic Dust Collected: 2/i)).toBeInTheDocument();

    // Simulate re-render (e.g., component unmount/mount or page refresh)
    localStorageMock.setItem('cosmicDustCount', '2'); // Ensure localStorage has the value
    const { unmount } = render(<App />);
    unmount();
    render(<App />);

    expect(screen.getByText(/Cosmic Dust Collected: 2/i)).toBeInTheDocument();
    expect(localStorageMock.getItem).toHaveBeenCalledWith('cosmicDustCount');
  });

  test('unlocks an artifact at the first threshold', () => {
    render(<App />);
    const collectButton = screen.getByRole('button', { name: /Collect Cosmic Dust/i });

    // Collect 9 dust (below threshold)
    for (let i = 0; i < 9; i++) {
      fireEvent.click(collectButton);
    }
    expect(screen.queryByText(/Discovered Artifacts/i)).not.toBeInTheDocument();
    expect(mockAlert).not.toHaveBeenCalled();

    // Collect 10th dust (at threshold)
    fireEvent.click(collectButton);
    expect(screen.getByText(/Cosmic Dust Collected: 10/i)).toBeInTheDocument();
    expect(screen.getByText(/Discovered Artifacts/i)).toBeInTheDocument();
    expect(screen.getByText(/Glimmering Shard/i)).toBeInTheDocument();
    expect(mockAlert).toHaveBeenCalledWith(expect.stringContaining('Glimmering Shard'));
  });

  test('unlocks multiple artifacts at different thresholds', () => {
    render(<App />);
    const collectButton = screen.getByRole('button', { name: /Collect Cosmic Dust/i });

    // Collect enough dust to unlock the first two artifacts (10 and 50)
    for (let i = 0; i < 50; i++) {
      fireEvent.click(collectButton);
    }

    expect(screen.getByText(/Cosmic Dust Collected: 50/i)).toBeInTheDocument();
    expect(screen.getByText(/Glimmering Shard/i)).toBeInTheDocument();
    expect(screen.getByText(/Nebula Whisper/i)).toBeInTheDocument();
    expect(mockAlert).toHaveBeenCalledTimes(2); // One for each artifact
    expect(mockAlert).toHaveBeenCalledWith(expect.stringContaining('Glimmering Shard'));
    expect(mockAlert).toHaveBeenCalledWith(expect.stringContaining('Nebula Whisper'));
  });

  test('artifacts persist across renders (simulated by re-rendering)', () => {
    // Pre-set localStorage for artifacts
    const initialArtifacts = [
      { threshold: 10, name: 'Glimmering Shard', description: 'A tiny piece of a forgotten star.' }
    ];
    localStorageMock.setItem('cosmicDustCount', '10');
    localStorageMock.setItem('unlockedCosmicArtifacts', JSON.stringify(initialArtifacts));

    const { unmount } = render(<App />);
    unmount();
    render(<App />);

    expect(screen.getByText(/Cosmic Dust Collected: 10/i)).toBeInTheDocument();
    expect(screen.getByText(/Discovered Artifacts/i)).toBeInTheDocument();
    expect(screen.getByText(/Glimmering Shard/i)).toBeInTheDocument();
    expect(localStorageMock.getItem).toHaveBeenCalledWith('unlockedCosmicArtifacts');
  });

  test('does not re-alert for already unlocked artifacts', () => {
    // Pre-set localStorage for artifacts
    const initialArtifacts = [
      { threshold: 10, name: 'Glimmering Shard', description: 'A tiny piece of a forgotten star.' }
    ];
    localStorageMock.setItem('cosmicDustCount', '10');
    localStorageMock.setItem('unlockedCosmicArtifacts', JSON.stringify(initialArtifacts));

    render(<App />);
    expect(mockAlert).not.toHaveBeenCalled(); // Should not alert on load for existing artifacts

    const collectButton = screen.getByRole('button', { name: /Collect Cosmic Dust/i });
    fireEvent.click(collectButton); // Collect more dust, but not enough for a new artifact
    expect(screen.getByText(/Cosmic Dust Collected: 11/i)).toBeInTheDocument();
    expect(mockAlert).not.toHaveBeenCalled(); // Still no new alert
  });
});
