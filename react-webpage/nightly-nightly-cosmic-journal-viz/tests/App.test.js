import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../App';

// Mock localStorage
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: jest.fn((key) => store[key] || null),
    setItem: jest.fn((key, value) => {
      store[key] = value.toString();
    }),
    clear: jest.fn(() => {
      store = {};
    }),
    removeItem: jest.fn((key) => {
      delete store[key];
    }),
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('App Component', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
    render(<App />);
  });

  test('renders the main title', () => {
    expect(screen.getByText(/Cosmic Journal Visualizer/i)).toBeInTheDocument();
  });

  test('allows adding a new journal entry', () => {
    const titleInput = screen.getByPlaceholderText(/Title \(e.g., A Starry Revelation\)/i);
    const dateInput = screen.getByLabelText(/date/i);
    const contentTextarea = screen.getByPlaceholderText(/Your cosmic musings.../i);
    const submitButton = screen.getByRole('button', { name: /Record Entry/i });

    fireEvent.change(titleInput, { target: { value: 'My First Thought' } });
    fireEvent.change(dateInput, { target: { value: '2023-10-27' } });
    fireEvent.change(contentTextarea, { target: { value: 'This is a test entry.' } });
    fireEvent.click(submitButton);

    expect(screen.getByText('My First Thought')).toBeInTheDocument();
    expect(screen.getByText('(2023-10-27)')).toBeInTheDocument();
    expect(screen.getByText('This is a test entry.')).toBeInTheDocument();
  });

  test('shows a message when no entries are present', () => {
    expect(screen.getByText(/Your cosmic journey is just beginning.../i)).toBeInTheDocument();
    expect(screen.getByText(/No words yet to form a nebula./i)).toBeInTheDocument();
  });

  test('updates word cloud based on entries', () => {
    const titleInput = screen.getByPlaceholderText(/Title \(e.g., A Starry Revelation\)/i);
    const dateInput = screen.getByLabelText(/date/i);
    const contentTextarea = screen.getByPlaceholderText(/Your cosmic musings.../i);
    const submitButton = screen.getByRole('button', { name: /Record Entry/i });

    fireEvent.change(titleInput, { target: { value: 'Cosmic Vibes' } });
    fireEvent.change(dateInput, { target: { value: '2023-10-26' } });
    fireEvent.change(contentTextarea, { target: { value: 'The universe is vast and full of wonder. Wonder is key.' } });
    fireEvent.click(submitButton);

    // Wait for the word cloud to potentially update (though it's synchronous here)
    // We expect 'universe', 'vast', 'wonder', 'key' to be present
    expect(screen.getByText('universe')).toBeInTheDocument();
    expect(screen.getByText('vast')).toBeInTheDocument();
    expect(screen.getByText('wonder')).toBeInTheDocument();
    expect(screen.getByText('key')).toBeInTheDocument();
  });

  test('persists entries to localStorage', () => {
    const titleInput = screen.getByPlaceholderText(/Title \(e.g., A Starry Revelation\)/i);
    const dateInput = screen.getByLabelText(/date/i);
    const contentTextarea = screen.getByPlaceholderText(/Your cosmic musings.../i);
    const submitButton = screen.getByRole('button', { name: /Record Entry/i });

    fireEvent.change(titleInput, { target: { value: 'Persistence Test' } });
    fireEvent.change(dateInput, { target: { value: '2023-10-28' } });
    fireEvent.change(contentTextarea, { target: { value: 'This should be saved.' } });
    fireEvent.click(submitButton);

    // Mock rationale: Verify that localStorage.setItem was called with the correct data.
    expect(localStorageMock.setItem).toHaveBeenCalledWith(
      'cosmicJournalEntries',
      expect.stringContaining('"title":"Persistence Test"')
    );
  });

  test('loads entries from localStorage on mount', () => {
    const mockEntries = [
      { id: 1, title: 'Loaded Entry', date: '2023-10-25', content: 'This was loaded.' },
    ];
    // Mock rationale: Set localStorage before rendering the component to simulate a saved state.
    localStorage.setItem('cosmicJournalEntries', JSON.stringify(mockEntries));

    // Re-render the component to trigger the useEffect that loads from localStorage
    render(<App />);

    expect(screen.getByText('Loaded Entry')).toBeInTheDocument();
    expect(screen.getByText('(2023-10-25)')).toBeInTheDocument();
    expect(screen.getByText('This was loaded.')).toBeInTheDocument();
  });

  test('handles form validation', () => {
    // Mock rationale: Spy on alert to check if it's called.
    const alertSpy = jest.spyOn(window, 'alert').mockImplementation(() => {});

    const submitButton = screen.getByRole('button', { name: /Record Entry/i });

    // Try to submit with empty fields
    fireEvent.click(submitButton);
    expect(alertSpy).toHaveBeenCalledWith('Please fill in all fields!');

    // Fill only title and date
    fireEvent.change(screen.getByPlaceholderText(/Title \(e.g., A Starry Revelation\)/i), { target: { value: 'Partial Entry' } });
    fireEvent.change(screen.getByLabelText(/date/i), { target: { value: '2023-10-29' } });
    fireEvent.click(submitButton);
    expect(alertSpy).toHaveBeenCalledWith('Please fill in all fields!');

    // Clean up the spy
    alertSpy.mockRestore();
  });
});
