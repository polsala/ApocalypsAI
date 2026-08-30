import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ResourceMap from '../src/components/ResourceMap';

// Mock Rationale: The mockResources array is hardcoded directly within ResourceMap.js.
// This ensures the component's behavior is deterministic and testable offline without
// needing to mock external data sources. We are testing how the component renders
// based on this internal mock data and the provided filter prop.
describe('ResourceMap', () => {
  test('renders a 10x10 grid of map cells', () => {
    render(<ResourceMap filter="All" />);
    const mapCells = screen.getAllByRole('generic', { className: 'map-cell' }); // map-cell is a div, so generic role
    expect(mapCells).toHaveLength(100);
  });

  test('displays all resources when filter is "All"', () => {
    render(<ResourceMap filter="All" />);
    expect(screen.getByTitle('Water at (1, 3)')).toBeInTheDocument();
    expect(screen.getByTitle('Food at (5, 8)')).toBeInTheDocument();
    expect(screen.getByTitle('Scrap at (9, 1)')).toBeInTheDocument();
    expect(screen.getByTitle('Fuel at (2, 7)')).toBeInTheDocument();
    expect(screen.getByTitle('Meds at (3, 6)')).toBeInTheDocument();
    expect(screen.getByTitle('Tools at (6, 9)')).toBeInTheDocument();
  });

  test('displays only "Water" resources when filter is "Water"', () => {
    render(<ResourceMap filter="Water" />);
    expect(screen.getByTitle('Water at (1, 3)')).toBeInTheDocument();
    expect(screen.getByTitle('Water at (7, 2)')).toBeInTheDocument();
    expect(screen.getByTitle('Water at (0, 9)')).toBeInTheDocument();

    // Ensure other types are not present
    expect(screen.queryByTitle('Food at (5, 8)')).not.toBeInTheDocument();
    expect(screen.queryByTitle('Scrap at (9, 1)')).not.toBeInTheDocument();
  });

  test('displays only "Food" resources when filter is "Food"', () => {
    render(<ResourceMap filter="Food" />);
    expect(screen.getByTitle('Food at (5, 8)')).toBeInTheDocument();
    expect(screen.getByTitle('Food at (0, 0)')).toBeInTheDocument();
    expect(screen.getByTitle('Food at (9, 0)')).toBeInTheDocument();

    // Ensure other types are not present
    expect(screen.queryByTitle('Water at (1, 3)')).not.toBeInTheDocument();
    expect(screen.queryByTitle('Scrap at (9, 1)')).not.toBeInTheDocument();
  });

  test('displays no resources if a non-existent filter is applied', () => {
    render(<ResourceMap filter="NonExistentType" />);
    expect(screen.queryByTitle(/Water/i)).not.toBeInTheDocument();
    expect(screen.queryByTitle(/Food/i)).not.toBeInTheDocument();
    expect(screen.queryByTitle(/Scrap/i)).not.toBeInTheDocument();
  });
});
