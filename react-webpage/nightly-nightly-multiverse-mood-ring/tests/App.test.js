import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// Mock rationale: The App component uses Math.random() to generate random moods.
// To ensure deterministic and repeatable tests, we mock Math.random() to return
// a fixed sequence of values. This allows us to predict the exact moods that
// will be generated, making the tests reliable and independent of random outcomes.
const mockMathRandom = (values) => {
  let i = 0;
  const originalMathRandom = Math.random;
  Math.random = jest.fn(() => {
    const value = values[i % values.length];
    i++;
    return value;
  });
  return () => { Math.random = originalMathRandom; }; // Cleanup function
};

describe('App', () => {
  let restoreMathRandom;

  beforeEach(() => {
    // Reset the mock before each test to ensure isolation
    restoreMathRandom = mockMathRandom([
      0.1, 0.2, // Initial moods for 3 rings:
      0.3, 0.4, // Ring 1: COMPONENT_NAMES[0] (Temporal Stability), MOOD_TYPES[0] (Stable)
      0.5, 0.6, // Ring 2: COMPONENT_NAMES[1] (Agent Activity), MOOD_TYPES[1] (Fluctuating)
                // Ring 3: COMPONENT_NAMES[2] (Resource Flux), MOOD_TYPES[2] (Anomalous)
      0.7, 0.8, // Refresh moods:
      0.9, 0.0, // Ring 1: COMPONENT_NAMES[3] (Void Echoes), MOOD_TYPES[3] (Unknown)
                // Ring 2: COMPONENT_NAMES[4] (Reality Weave), MOOD_TYPES[0] (Stable)
                // Ring 3: COMPONENT_NAMES[0] (Temporal Stability), MOOD_TYPES[1] (Fluctuating)
    ]);
  });

  afterEach(() => {
    restoreMathRandom(); // Restore original Math.random after each test
  });

  test('renders the main title and description', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Multiverse Mood Ring/i)).toBeInTheDocument();
    expect(screen.getByText(/Gauging the cosmic vibes of ApocalypsAI operations./i)).toBeInTheDocument();
  });

  test('displays initial mood rings', async () => {
    render(<App />);

    // Based on mockMathRandom values:
    // Ring 1: COMPONENT_NAMES[0] (Temporal Stability), MOOD_TYPES[0] (Stable)
    // Ring 2: COMPONENT_NAMES[1] (Agent Activity), MOOD_TYPES[1] (Fluctuating)
    // Ring 3: COMPONENT_NAMES[2] (Resource Flux), MOOD_TYPES[2] (Anomalous)

    await waitFor(() => {
      expect(screen.getByText('Temporal Stability')).toBeInTheDocument();
      expect(screen.getByText('Stable')).toBeInTheDocument();
      expect(screen.getByText('Agent Activity')).toBeInTheDocument();
      expect(screen.getByText('Fluctuating')).toBeInTheDocument();
      expect(screen.getByText('Resource Flux')).toBeInTheDocument();
      expect(screen.getByText('Anomalous')).toBeInTheDocument();
    });
  });

  test('refreshes moods when the button is clicked', async () => {
    render(<App />);

    // Initial moods (from previous test, just to be sure they are there)
    await waitFor(() => {
      expect(screen.getByText('Temporal Stability')).toBeInTheDocument();
      expect(screen.getByText('Stable')).toBeInTheDocument();
    });

    const refreshButton = screen.getByRole('button', { name: /Refresh Multiverse Vibes/i });
    fireEvent.click(refreshButton);

    // After refresh, based on mockMathRandom values:
    // Ring 1: COMPONENT_NAMES[3] (Void Echoes), MOOD_TYPES[3] (Unknown)
    // Ring 2: COMPONENT_NAMES[4] (Reality Weave), MOOD_TYPES[0] (Stable)
    // Ring 3: COMPONENT_NAMES[0] (Temporal Stability), MOOD_TYPES[1] (Fluctuating)

    await waitFor(() => {
      expect(screen.getByText('Void Echoes')).toBeInTheDocument();
      expect(screen.getByText('Unknown')).toBeInTheDocument();
      expect(screen.getByText('Reality Weave')).toBeInTheDocument();
      expect(screen.getAllByText('Stable').length).toBeGreaterThanOrEqual(1); // One 'Stable' from Reality Weave
      expect(screen.getByText('Temporal Stability')).toBeInTheDocument();
      expect(screen.getByText('Fluctuating')).toBeInTheDocument();
    });

    // Ensure old moods are gone (or at least not the primary ones)
    expect(screen.queryByText('Agent Activity')).not.toBeInTheDocument();
    expect(screen.queryByText('Resource Flux')).not.toBeInTheDocument();
  });

  test('mood rings have correct background colors based on status', async () => {
    render(<App />);

    // Initial moods:
    // Ring 1: Temporal Stability (Stable, #4CAF50)
    // Ring 2: Agent Activity (Fluctuating, #FFC107)
    // Ring 3: Resource Flux (Anomalous, #F44336)

    await waitFor(() => {
      const stableRing = screen.getByText('Temporal Stability').closest('.mood-ring');
      expect(stableRing).toHaveStyle('background-color: #4CAF50');

      const fluctuatingRing = screen.getByText('Agent Activity').closest('.mood-ring');
      expect(fluctuatingRing).toHaveStyle('background-color: #FFC107');

      const anomalousRing = screen.getByText('Resource Flux').closest('.mood-ring');
      expect(anomalousRing).toHaveStyle('background-color: #F44336');
    });
  });
});
