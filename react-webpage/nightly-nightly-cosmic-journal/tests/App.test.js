import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../src/App';

// Mock the current date to ensure deterministic testing for daily wisdom
const mockDate = new Date(2023, 10, 21); // November 21, 2023
const realDate = Date;

beforeAll(() => {
  global.Date = class extends Date {
    constructor(dateString) {
      if (dateString) {
        return new realDate(dateString);
      }
      return mockDate;
    }
  };
});

afterAll(() => {
  global.Date = realDate;
});

describe('Cosmic Journal', () => {
  test('renders the main title and description', () => {
    render(<App />);
    expect(screen.getByText('Cosmic Journal')).toBeInTheDocument();
    expect(screen.getByText('Your personal space for dreams and thoughts among the stars.')).toBeInTheDocument();
  });

  test('displays daily cosmic wisdom based on date', () => {
    render(<App />);
    // Based on the mockDate (Nov 21, 2023), dayOfYear is 325.
    // The wisdom array has 8 elements. 325 % 8 = 5.
    // The 5th element (index 5) is "The cosmos is within us. We are made of star-stuff. We are a way for the universe to know itself."
    expect(screen.getByText(/The cosmos is within us. We are made of star-stuff. We are a way for the universe to know itself./i)).toBeInTheDocument();
  });

  test('allows adding a thought', () => {
    render(<App />);
    const thoughtInput = screen.getByPlaceholderText('Capture a fleeting thought...');
    const addButton = screen.getByRole('button', { name: /Add Thought/i });

    fireEvent.change(thoughtInput, { target: { value: 'A new idea sparked!' } });
    fireEvent.click(addButton);

    expect(screen.getByText('A new idea sparked!')).toBeInTheDocument();
  });

  test('does not add an empty thought', () => {
    render(<App />);
    const addButton = screen.getByRole('button', { name: /Add Thought/i });
    fireEvent.click(addButton);
    expect(screen.queryByText('')).not.toBeInTheDocument(); // Ensure no empty list item is added
  });

  test('allows adding a dream', () => {
    render(<App />);
    const titleInput = screen.getByPlaceholderText('Dream Title');
    const descriptionInput = screen.getByPlaceholderText('Describe your dream...');
    const addButton = screen.getByRole('button', { name: /Log Dream/i });

    fireEvent.change(titleInput, { target: { value: 'Flying Dream' } });
    fireEvent.change(descriptionInput, { target: { value: 'I was soaring over mountains.' } });
    fireEvent.click(addButton);

    expect(screen.getByText('Flying Dream:')).toBeInTheDocument();
    expect(screen.getByText('I was soaring over mountains.')).toBeInTheDocument();
  });

  test('does not add an empty dream', () => {
    render(<App />);
    const addButton = screen.getByRole('button', { name: /Log Dream/i });
    fireEvent.click(addButton);
    expect(screen.queryByText(/Dream Title:/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Describe your dream:/i)).not.toBeInTheDocument();
  });
});
