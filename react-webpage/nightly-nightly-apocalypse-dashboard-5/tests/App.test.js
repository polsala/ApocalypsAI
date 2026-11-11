import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: We are mocking the entire App component's data and behavior
// as it's a standalone utility and doesn't rely on external APIs in this version.
// This ensures deterministic and offline testing.

describe('App Component', () => {
  test('renders the main title', () => {
    render(<App />);
    const titleElement = screen.getByText(/ApocalypsAI Status Dashboard/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders agent status section', () => {
    render(<App />);
    const agentSection = screen.getByText(/Agent Status/i);
    expect(agentSection).toBeInTheDocument();

    // Check for at least one agent card
    const agentCard = screen.getByText(/Builder/i);
    expect(agentCard).toBeInTheDocument();
  });

  test('renders utility generation section', () => {
    render(<App />);
    const utilitySection = screen.getByText(/Utility Generation/i);
    expect(utilitySection).toBeInTheDocument();

    // Check for total utilities count
    const totalUtilities = screen.getByText(/Total Utilities Generated:/i);
    expect(totalUtilities).toBeInTheDocument();
    expect(totalUtilities.nextSibling).toHaveTextContent('1943'); // Based on mock data
  });

  test('renders workflow monitor section', () => {
    render(<App />);
    const workflowSection = screen.getByText(/Workflow Health/i);
    expect(workflowSection).toBeInTheDocument();

    // Check for at least one workflow card
    const workflowCard = screen.getByText(/gen_openrouter/i);
    expect(workflowCard).toBeInTheDocument();
  });

  test('renders footer', () => {
    render(<App />);
    const footerElement = screen.getByText(/© 2023 ApocalypsAI Collective/i);
    expect(footerElement).toBeInTheDocument();
  });
});
