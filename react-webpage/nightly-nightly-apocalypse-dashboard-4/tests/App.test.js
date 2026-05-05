import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: These tests are deterministic and offline, relying on static mock data.
// No external API calls or network requests are made.

describe('App Component', () => {
  test('renders the main title', () => {
    render(<App />);
    const titleElement = screen.getByText(/ApocalypsAI Command Center/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders agent status cards', () => {
    render(<App />);
    // Check for at least one agent card to be rendered
    const agentCards = screen.getAllByText(/Status:/i);
    expect(agentCards.length).toBeGreaterThan(0);
    // Check for specific agent names if needed, e.g.:
    expect(screen.getByText(/Builder/i)).toBeInTheDocument();
    expect(screen.getByText(/Guardian/i)).toBeInTheDocument();
  });

  test('renders total utility count', () => {
    render(<App />);
    expect(screen.getByText(/Total Utilities Generated:/i)).toBeInTheDocument();
    expect(screen.getByText(/2000/i)).toBeInTheDocument(); // Based on mock data
  });

  test('renders classifier distribution', () => {
    render(<App />);
    expect(screen.getByText(/Utility Distribution by Classifier/i)).toBeInTheDocument();
    expect(screen.getByText(/python-utils:/i)).toBeInTheDocument();
    expect(screen.getByText(/react-webpage:/i)).toBeInTheDocument();
    expect(screen.getByText(/bash-utils:/i)).toBeInTheDocument();
  });

  test('renders workflow status items', () => {
    render(<App />);
    expect(screen.getByText(/Workflow Health/i)).toBeInTheDocument();
    expect(screen.getByText(/gen_openrouter:/i)).toBeInTheDocument();
    expect(screen.getByText(/nightly_self_heal:/i)).toBeInTheDocument();
  });

  test('renders footer text', () => {
    render(<App />);
    expect(screen.getByText(/Stay vigilant. The future is automated./i)).toBeInTheDocument();
  });
});
