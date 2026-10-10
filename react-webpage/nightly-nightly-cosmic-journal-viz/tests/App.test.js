import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import { generateCosmicEntries, searchEntries } from '../src/utils/mockData';

// Mock rationale: Mocking the data generation and search functions to ensure deterministic tests.
// This prevents reliance on the actual implementation details of mockData.js and ensures
// the App component's rendering and state management are tested in isolation.
jest.mock('../src/utils/mockData', () => ({
  generateCosmicEntries: jest.fn(),
  searchEntries: jest.fn(),
}));

describe('App Component', () => {
  const mockEntries = [
    { origin: 'Alpha Centauri', timestamp: '2023-01-01T10:00:00Z', content: 'Hello from the stars!', theme: 'Stellar Sentiments' },
    { origin: 'Orion Nebula', timestamp: '2023-01-01T11:00:00Z', content: 'Dust motes dance.', theme: 'Nebula Musings' },
    { origin: 'Deep Space', timestamp: '2023-01-01T12:00:00Z', content: 'The void whispers secrets.', theme: 'Void Echoes' },
  ];

  beforeEach(() => {
    // Reset mocks before each test
    generateCosmicEntries.mockClear();
    searchEntries.mockClear();

    // Set default mock implementation for generateCosmicEntries
    generateCosmicEntries.mockReturnValue(mockEntries);
  });

  test('renders header and initial entries', () => {
    render(<App />);
    expect(screen.getByText('Cosmic Journal Explorer')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Search cosmic whispers...')).toBeInTheDocument();

    // Check if the mock entries are rendered
    mockEntries.forEach(entry => {
      expect(screen.getByText(entry.content)).toBeInTheDocument();
      expect(screen.getByText(`From: ${entry.origin}`)).toBeInTheDocument();
    });
  });

  test('filters entries when search term is entered', () => {
    const searchTerm = 'stars';
    const filtered = [
      { origin: 'Alpha Centauri', timestamp: '2023-01-01T10:00:00Z', content: 'Hello from the stars!', theme: 'Stellar Sentiments' },
    ];

    // Set mock implementation for searchEntries
    searchEntries.mockReturnValue(filtered);

    render(<App />);
    const searchInput = screen.getByPlaceholderText('Search cosmic whispers...');
    fireEvent.change(searchInput, { target: { value: searchTerm } });

    // Verify that searchEntries was called with the correct arguments
    expect(searchEntries).toHaveBeenCalledWith(mockEntries, searchTerm);

    // Verify that only the filtered entry is displayed
    expect(screen.getByText('Hello from the stars!')).toBeInTheDocument();
    expect(screen.queryByText('Dust motes dance.')).not.toBeInTheDocument();
    expect(screen.queryByText('The void whispers secrets.')).not.toBeInTheDocument();
  });

  test('displays all entries when search term is cleared', () => {
    render(<App />);
    const searchInput = screen.getByPlaceholderText('Search cosmic whispers...');

    // First, simulate a search
    const searchTerm = 'stars';
    const filtered = [
      { origin: 'Alpha Centauri', timestamp: '2023-01-01T10:00:00Z', content: 'Hello from the stars!', theme: 'Stellar Sentiments' },
    ];
    searchEntries.mockReturnValue(filtered);
    fireEvent.change(searchInput, { target: { value: searchTerm } });

    // Then, clear the search input
    fireEvent.change(searchInput, { target: { value: '' } });

    // Verify that all original mock entries are now displayed
    mockEntries.forEach(entry => {
      expect(screen.getByText(entry.content)).toBeInTheDocument();
    });
  });
});
