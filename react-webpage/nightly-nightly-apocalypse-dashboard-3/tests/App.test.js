import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import App from '../src/App';

// Mocking the data modules
jest.mock('../src/data/mockMetrics', () => [
  { id: 1, name: 'Mock Metric 1', value: 'High', description: 'A test metric.' },
  { id: 2, name: 'Mock Metric 2', value: 'Low', description: 'Another test metric.' }
]);

jest.mock('../src/data/mockTips', () => [
  'Mock Tip 1',
  'Mock Tip 2'
]);

// Mocking CSS modules to prevent import errors during tests
jest.mock('../src/App.css', () => ({}));
jest.mock('../src/components/MetricCard.css', () => ({}));
jest.mock('../src/components/SurvivalTip.css', () => ({}));

describe('App', () => {
  test('renders the main title and header', () => {
    render(<App />);
    expect(screen.getByText(/Apocalypse Dashboard/i)).toBeInTheDocument();
    expect(screen.getByText(/Keeping you informed, one disaster at a time./i)).toBeInTheDocument();
  });

  test('renders mock metrics', async () => {
    render(<App />);
    // Wait for the mock data to be set
    await waitFor(() => {
      expect(screen.getByText('Mock Metric 1')).toBeInTheDocument();
      expect(screen.getByText('High')).toBeInTheDocument();
      expect(screen.getByText('Mock Metric 2')).toBeInTheDocument();
      expect(screen.getByText('Low')).toBeInTheDocument();
    });
  });

  test('renders a survival tip', async () => {
    render(<App />);
    // Wait for the mock tip to be set
    await waitFor(() => {
      // We can't predict which tip will be chosen, so we check for the presence of one of them.
      // A more robust test might mock Math.random to ensure a specific tip is chosen.
      const tipElement = screen.getByText(/Mock Tip/i);
      expect(tipElement).toBeInTheDocument();
    });
  });

  test('renders the footer', () => {
    render(<App />);
    expect(screen.getByText(/© 2023 ApocalypsAI. Stay safe out there!/i)).toBeInTheDocument();
  });
});
