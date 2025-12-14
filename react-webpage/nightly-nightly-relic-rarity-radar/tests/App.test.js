import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

describe('App', () => {
  // # Mock rationale: React Testing Library provides a simulated DOM environment (jsdom) for component rendering and interaction. The `assignRarity` function is a pure, deterministic utility and does not require mocking.

  test('renders the main heading', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Relic Rarity Radar/i)).toBeInTheDocument();
  });

  test('allows user to input an item name', () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter item name/i);
    fireEvent.change(inputElement, { target: { value: 'test item' } });
    expect(inputElement.value).toBe('test item');
  });

  test('adds a new relic to the list when Analyze Relic button is clicked', () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter item name/i);
    const analyzeButton = screen.getByRole('button', { name: /Analyze Relic/i });

    fireEvent.change(inputElement, { target: { value: 'Simple Rock' } });
    fireEvent.click(analyzeButton);

    expect(screen.getByText('Simple Rock')).toBeInTheDocument();
    expect(screen.getByText('Common Scavenge')).toBeInTheDocument();
    expect(inputElement.value).toBe(''); // Input should clear after adding
  });

  test('adds multiple relics and displays them in reverse chronological order', () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter item name/i);
    const analyzeButton = screen.getByRole('button', { name: /Analyze Relic/i });

    fireEvent.change(inputElement, { target: { value: 'First Item' } });
    fireEvent.click(analyzeButton);

    fireEvent.change(inputElement, { target: { value: 'Second Item' } });
    fireEvent.click(analyzeButton);

    const listItems = screen.getAllByRole('listitem');
    expect(listItems).toHaveLength(2);
    // Check order: Second Item should be first in the list
    expect(listItems[0]).toHaveTextContent('Second Item');
    expect(listItems[1]).toHaveTextContent('First Item');
  });

  test('assigns correct rarity for a known item (Mythic Echo)', () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter item name/i);
    const analyzeButton = screen.getByRole('button', { name: /Analyze Relic/i });

    fireEvent.change(inputElement, { target: { value: 'Temporal Void Anomaly Core' } });
    fireEvent.click(analyzeButton);

    expect(screen.getByText('Temporal Void Anomaly Core')).toBeInTheDocument();
    expect(screen.getByText('Mythic Echo')).toBeInTheDocument();
    expect(screen.getByText('Mythic Echo')).toHaveStyle('color: #8A2BE2');
  });

  test('does not add empty item names', () => {
    render(<App />);
    const analyzeButton = screen.getByRole('button', { name: /Analyze Relic/i });
    fireEvent.click(analyzeButton);
    expect(screen.getByText('No relics analyzed yet. Start scanning!')).toBeInTheDocument();
  });

  test('adds relic on Enter key press', () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter item name/i);

    fireEvent.change(inputElement, { target: { value: 'Keyboard Relic' } });
    fireEvent.keyPress(inputElement, { key: 'Enter', code: 'Enter', charCode: 13 });

    expect(screen.getByText('Keyboard Relic')).toBeInTheDocument();
    expect(screen.getByText('Uncommon Find')).toBeInTheDocument();
  });
});
