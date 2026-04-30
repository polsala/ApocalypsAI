import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Mock the UtilityCard component to avoid rendering its children during App tests
jest.mock('../src/components/UtilityCard', () => {
  return jest.fn(({ utility }) => (
    <div data-testid="mock-utility-card">
      <h3>{utility.name}</h3>
      <p>{utility.classifier}</p>
      <p>{utility.status}</p>
      <p>Readiness: {Math.round(utility.readiness * 100)}%</p>
    </div>
  ));
});

describe('App Component', () => {
  test('renders the main title', () => {
    render(<App />);
    const titleElement = screen.getByText(/ApocalypsAI Utility Status Dashboard/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders a list of mock utilities as UtilityCards', () => {
    render(<App />);
    // Check if at least one mock utility card is rendered
    const utilityCards = screen.getAllByTestId('mock-utility-card');
    expect(utilityCards.length).toBeGreaterThan(0);
    // Optionally, check for specific mock data presence
    expect(screen.getByText('nightly-shelter-sentry-log')).toBeInTheDocument();
    expect(screen.getByText('python-utils')).toBeInTheDocument();
    expect(screen.getByText('Operational')).toBeInTheDocument();
    expect(screen.getByText('Readiness: 95%')).toBeInTheDocument();
  });

  test('renders the footer', () => {
    render(<App />);
    const footerElement = screen.getByText(/© 2023 ApocalypsAI Collective/i);
    expect(footerElement).toBeInTheDocument();
  });
});
