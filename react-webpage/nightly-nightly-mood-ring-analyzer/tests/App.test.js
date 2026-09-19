import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import * as analyzer from '../src/analyzer';

describe('App', () => {
  // Mock rationale: We are testing the rendering and interaction of the React App component.
  // The `analyzeUtility` function from `analyzer.js` is mocked to control its output,
  // allowing us to test how the UI responds to different 'moods' without relying on the
  // complex keyword analysis logic or needing to provide full utility JSON for every test.
  // This ensures deterministic and focused UI testing.
  const mockAnalyzeUtility = jest.spyOn(analyzer, 'analyzeUtility');

  beforeEach(() => {
    mockAnalyzeUtility.mockClear();
    // Default mock for analyzer, simulating a neutral state
    mockAnalyzeUtility.mockReturnValue({
      name: 'Neutral Stability',
      color: '#808080',
      description: 'Awaiting utility data...'
    });
  });

  test('renders the main application title', () => {
    render(<App />);
    expect(screen.getByText(/ApocalypsAI Nightly Mood Ring/i)).toBeInTheDocument();
  });

  test('renders the textarea for JSON input', () => {
    render(<App />);
    expect(screen.getByPlaceholderText(/Paste Utility JSON Here.../i)).toBeInTheDocument();
  });

  test('displays default mood when no JSON is entered', () => {
    render(<App />);
    expect(screen.getByText('Neutral Stability')).toBeInTheDocument();
    expect(screen.getByText('Awaiting utility data...')).toBeInTheDocument();
  });

  test('updates mood when valid JSON is entered', () => {
    mockAnalyzeUtility.mockReturnValue({
      name: 'Whimsical Whimsy',
      color: '#F5A623',
      description: 'A lighthearted and playful spirit.'
    });

    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste Utility JSON Here.../i);
    const testJson = JSON.stringify({
      util_name: 'nightly-whimsical-emoji-clock',
      summary: 'A clock with emojis.',
      classifier: 'js-utils',
      files: []
    });

    fireEvent.change(textarea, { target: { value: testJson } });

    expect(mockAnalyzeUtility).toHaveBeenCalledWith(JSON.parse(testJson));
    expect(screen.getByText('Whimsical Whimsy')).toBeInTheDocument();
    expect(screen.getByText('A lighthearted and playful spirit.')).toBeInTheDocument();
    // Check if the mood ring style is applied (indirectly via component structure)
    const moodRing = screen.getByText('Whimsical Whimsy').closest('.mood-ring');
    expect(moodRing).toHaveStyle('background-color: #F5A623');
  });

  test('displays error for invalid JSON input', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste Utility JSON Here.../i);
    const invalidJson = '{ "util_name": "test", "summary": "test"'; // Malformed JSON

    fireEvent.change(textarea, { target: { value: invalidJson } });

    expect(screen.getByText(/Invalid JSON format. Please check your input./i)).toBeInTheDocument();
    expect(screen.getByText('Error State')).toBeInTheDocument();
    const moodRing = screen.getByText('Error State').closest('.mood-ring');
    expect(moodRing).toHaveStyle('background-color: #FF0000');
  });

  test('resets to default mood when textarea is cleared', () => {
    mockAnalyzeUtility.mockReturnValueOnce({
      name: 'DevOps Drive',
      color: '#BD10E0',
      description: 'Focused on automation.'
    });

    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste Utility JSON Here.../i);
    const testJson = JSON.stringify({
      util_name: 'nightly-ansible-playbook',
      summary: 'An Ansible playbook.',
      classifier: 'ansible-playbooks',
      files: []
    });

    fireEvent.change(textarea, { target: { value: testJson } });
    expect(screen.getByText('DevOps Drive')).toBeInTheDocument();

    fireEvent.change(textarea, { target: { value: '' } });
    expect(screen.getByText('Neutral Stability')).toBeInTheDocument();
    expect(screen.getByText('Awaiting utility data...')).toBeInTheDocument();
    expect(screen.queryByText(/Invalid JSON format/i)).not.toBeInTheDocument();
  });
});
