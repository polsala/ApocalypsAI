import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// Mock Rationale: We are testing the App component's rendering and state management.
// Child components (ResourceMap, ResourceFilter, ResourceLegend) are implicitly tested
// for their presence and interaction, but their internal logic is tested in their own files.
// No external dependencies or complex mocks needed for App.
describe('App', () => {
  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Resource Nexus Map/i)).toBeInTheDocument();
  });

  test('renders ResourceFilter and ResourceLegend components', () => {
    render(<App />);
    expect(screen.getByText('All')).toBeInTheDocument(); // From ResourceFilter
    expect(screen.getByText('Resource Legend')).toBeInTheDocument(); // From ResourceLegend
  });

  test('filter buttons change the active filter state', () => {
    render(<App />);
    const foodButton = screen.getByRole('button', { name: /Food/i });
    fireEvent.click(foodButton);
    expect(foodButton).toHaveClass('active');

    const waterButton = screen.getByRole('button', { name: /Water/i });
    fireEvent.click(waterButton);
    expect(waterButton).toHaveClass('active');
    expect(foodButton).not.toHaveClass('active'); // Ensure only one is active
  });

  test('map updates when filter changes (implicitly via prop passing)', () => {
    render(<App />);
    // Initially, Water at (1,3) should be visible
    expect(screen.getByTitle('Water at (1, 3)')).toBeInTheDocument();
    // Initially, Food at (5,8) should be visible
    expect(screen.getByTitle('Food at (5, 8)')).toBeInTheDocument();

    // Click on 'Food' filter
    fireEvent.click(screen.getByRole('button', { name: /Food/i }));

    // Now, Water at (1,3) should NOT be visible
    expect(screen.queryByTitle('Water at (1, 3)')).not.toBeInTheDocument();
    // Food at (5,8) should still be visible
    expect(screen.getByTitle('Food at (5, 8)')).toBeInTheDocument();

    // Click on 'All' filter
    fireEvent.click(screen.getByRole('button', { name: /All/i }));
    // Both should be visible again
    expect(screen.getByTitle('Water at (1, 3)')).toBeInTheDocument();
    expect(screen.getByTitle('Food at (5, 8)')).toBeInTheDocument();
  });
});
