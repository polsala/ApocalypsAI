import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';
import MoodRing from '../src/MoodRing';

// Mock rationale: For component testing, we want to ensure the component renders correctly
// based on its props. We mock the sentiment analysis module to provide deterministic
// mood values, avoiding reliance on complex string analysis or external data.
// This ensures tests are fast, isolated, and predictable.
jest.mock('../src/SentimentAnalyzer', () => ({
  analyzeSentiment: jest.fn((messages) => {
    // Simplified mock logic for testing purposes, mimicking the App.js mockEvents outcome
    if (messages.some(msg => msg.toLowerCase().includes('bug')) && messages.some(msg => msg.toLowerCase().includes('error')) && messages.length > 2) return 'Tense';
    if (messages.some(msg => msg.toLowerCase().includes('feature'))) return 'Active';
    if (messages.some(msg => msg.toLowerCase().includes('fix'))) return 'Calm';
    if (messages.some(msg => msg.toLowerCase().includes('awesome'))) return 'Joyful';
    return 'Neutral';
  }),
}));

describe('App Component', () => {
  test('renders the main heading', () => {
    render(<App />);
    expect(screen.getByText(/ApocalypsAI Community Aura Ring/i)).toBeInTheDocument();
  });

  test('displays the current mood based on mocked sentiment', async () => {
    // The mock in SentimentAnalyzer.js will return 'Tense' because mockEvents in App.js
    // contain 'bug' and 'error' and have more than 2 messages, matching the mock logic.
    render(<App />);
    // Wait for the useEffect to run and update the state
    expect(await screen.findByText(/The current collective aura of ApocalypsAI is: Tense/i)).toBeInTheDocument();
  });
});

describe('MoodRing Component', () => {
  test('renders with "Calm" mood', () => {
    render(<MoodRing mood="Calm" />);
    expect(screen.getByText('Calm')).toBeInTheDocument();
    expect(screen.getByText('Calm').closest('.mood-ring')).toHaveStyle('border-color: #8BC34A');
  });

  test('renders with "Active" mood', () => {
    render(<MoodRing mood="Active" />);
    expect(screen.getByText('Active')).toBeInTheDocument();
    expect(screen.getByText('Active').closest('.mood-ring')).toHaveStyle('border-color: #FFC107');
  });

  test('renders with "Tense" mood', () => {
    render(<MoodRing mood="Tense" />);
    expect(screen.getByText('Tense')).toBeInTheDocument();
    expect(screen.getByText('Tense').closest('.mood-ring')).toHaveStyle('border-color: #F44336');
  });

  test('renders with "Joyful" mood', () => {
    render(<MoodRing mood="Joyful" />);
    expect(screen.getByText('Joyful')).toBeInTheDocument();
    expect(screen.getByText('Joyful').closest('.mood-ring')).toHaveStyle('border-color: #03A9F4');
  });

  test('renders with "Neutral" mood if an unknown mood is provided', () => {
    render(<MoodRing mood="Unknown" />);
    expect(screen.getByText('Unknown')).toBeInTheDocument(); // The text itself is rendered
    expect(screen.getByText('Unknown').closest('.mood-ring')).toHaveStyle('border-color: #9E9E9E'); // But the color defaults to Neutral
  });
});
