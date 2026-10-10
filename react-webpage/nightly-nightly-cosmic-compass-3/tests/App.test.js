import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import App from '../src/App';

// Mock the Date object to ensure deterministic results for useEffect
const realDate = Date;

// Mock the celestial event data used in App.js
const mockCelestialEvents = [
  {
    name: 'The Great Nebula Bloom',
    description: 'A spectacular unfurling of cosmic dust, painting the void with vibrant hues. Your alignment is... surprisingly harmonious!',
    alignmentScore: 85,
    visual: '🌸'
  },
  {
    name: 'The Comet's Whisper',
    description: 'A fleeting visitor, leaving trails of stardust and a subtle hum in the ether. You feel a gentle nudge from the universe.',
    alignmentScore: 72,
    visual: '☄️'
  },
  {
    name: 'The Binary Star Waltz',
    description: 'Two celestial bodies locked in an eternal dance, their gravitational pull creating ripples of energy. You are caught in a delightful cosmic pirouette!',
    alignmentScore: 91,
    visual: '💫'
  },
  {
    name: 'The Void's Embrace',
    description: 'A moment of profound stillness, where the vast emptiness offers a unique perspective. Embrace the quiet, your alignment is introspective.',
    alignmentScore: 60,
    visual: '🌌'
  },
  {
    name: 'The Supernova's Echo',
    description: 'A distant explosion, its light reaching you as a reminder of creation and destruction. Your alignment is... explosive!',
    alignmentScore: 78,
    visual: '💥'
  }
];

describe('Cosmic Compass App', () => {
  beforeAll(() => {
    // Mock Date.getDay() to return a fixed value for consistent testing.
    // We'll use a specific day (e.g., Monday, which is day 1) to ensure we hit a predictable mock event.
    global.Date = class extends Date {
      constructor(date) {
        if (date) {
          super(date);
        } else {
          // Mock a specific date to control getDay()
          super('2023-10-23T10:00:00Z'); // This is a Monday
        }
      }
      getDay() {
        // Mock.getDay() to return 1 (Monday)
        return 1;
      }
    };
  });

  afterAll(() => {
    // Restore the original Date object after all tests are done
    global.Date = realDate;
  });

  test('renders the main title and initial loading message', () => {
    render(<App />);
    expect(screen.getByText('The Cosmic Compass')).toBeInTheDocument();
    expect(screen.getByText('Loading cosmic energies...')).toBeInTheDocument();
  });

  test('displays the correct celestial event and alignment after loading', async () => {
    render(<App />);

    // Wait for the useEffect to complete and the state to update
    await waitFor(() => {
      expect(screen.queryByText('Loading cosmic energies...')).not.toBeInTheDocument();
    });

    // Based on our mock Date.getDay() returning 1 (Monday), it should pick the second event (index 1)
    const expectedEvent = mockCelestialEvents[1]; // The Comet's Whisper

    expect(screen.getByText(expectedEvent.name)).toBeInTheDocument();
    expect(screen.getByText(expectedEvent.description)).toBeInTheDocument();
    expect(screen.getByText(`${expectedEvent.alignmentScore}%`)).toBeInTheDocument();

    // Check if the visual element is rendered
    expect(screen.getByText(expectedEvent.visual)).toBeInTheDocument();

    // Check if the meter bar has the correct width style
    const meterBar = screen.getByRole('progressbar', { name: /cosmic alignment/i }); // Assuming a role for accessibility, or find by class
    // We need to find the actual meter bar element within the container
    const meterBarElement = screen.getByText(`${expectedEvent.alignmentScore}%`).parentElement.previousElementSibling.querySelector('.meter-bar');
    expect(meterBarElement).toHaveStyle(`width: ${expectedEvent.alignmentScore}%`);
  });

  test('renders footer with copyright information', () => {
    render(<App />);
    expect(screen.getByText(/© 2023 ApocalypsAI - For entertainment purposes only./i)).toBeInTheDocument();
  });
});
