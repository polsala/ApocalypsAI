import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// Mock localStorage
let store = {};
const mockLocalStorage = {
  getItem: jest.fn(() => (store['apocalypseArtPrompts'] ? JSON.stringify(store['apocalypseArtPrompts']) : null)),
  setItem: jest.fn((key, value) => {
    store[key] = JSON.parse(value);
  }),
  clear: jest.fn(() => {
    store = {};
  })
};
Object.defineProperty(window, 'localStorage', {
  value: mockLocalStorage
});

describe('App', () => {
  beforeEach(() => {
    // Clear mocks and store before each test
    mockLocalStorage.clear();
    jest.clearAllMocks();
    store = {}; // Reset the mock store
  });

  test('renders without crashing', () => {
    render(<App />);
    expect(screen.getByText(/Apocalypse Art Generator/i)).toBeInTheDocument();
  });

  test('generates a prompt when button is clicked', () => {
    render(<App />);
    const generateButton = screen.getByRole('button', { name: /Generate Prompt/i });
    fireEvent.click(generateButton);
    expect(screen.getByText(/Your Prompt:/i)).toBeInTheDocument();
    expect(screen.getByText(/A .* depiction of .*/i)).toBeInTheDocument();
  });

  test('surprise me button generates a different prompt', () => {
    render(<App />);
    const generateButton = screen.getByRole('button', { name: /Generate Prompt/i });
    fireEvent.click(generateButton);
    const initialPrompt = screen.getByText(/Your Prompt:/i).nextSibling.textContent;

    const surpriseButton = screen.getByRole('button', { name: /Surprise Me!/i });
    fireEvent.click(surpriseButton);
    const surprisedPrompt = screen.getByText(/Your Prompt:/i).nextSibling.textContent;

    expect(initialPrompt).not.toBe(surprisedPrompt);
  });

  test('can save a generated prompt', () => {
    render(<App />);
    const generateButton = screen.getByRole('button', { name: /Generate Prompt/i });
    fireEvent.click(generateButton);
    const promptText = screen.getByText(/Your Prompt:/i).nextSibling.textContent;

    const saveButton = screen.getByRole('button', { name: /Save Prompt/i });
    fireEvent.click(saveButton);

    expect(screen.getByText(/Saved Prompts/i)).toBeInTheDocument();
    expect(screen.getByText(promptText)).toBeInTheDocument();
    expect(mockLocalStorage.setItem).toHaveBeenCalledWith('apocalypseArtPrompts', JSON.stringify([promptText]));
  });

  test('does not save duplicate prompts', () => {
    const existingPrompt = 'A Surrealism depiction of A lone survivor in the context of a Cosmic Horror apocalypse.';
    mockLocalStorage.getItem.mockReturnValueOnce(JSON.stringify([existingPrompt]));

    render(<App />);
    expect(screen.getByText(existingPrompt)).toBeInTheDocument();

    const generateButton = screen.getByRole('button', { name: /Generate Prompt/i });
    fireEvent.click(generateButton);
    const newPromptText = screen.getByText(/Your Prompt:/i).nextSibling.textContent;

    const saveButton = screen.getByRole('button', { name: /Save Prompt/i });
    fireEvent.click(saveButton);

    // Try to save the same prompt again
    fireEvent.click(saveButton);

    expect(screen.getAllByText(newPromptText).length).toBe(1);
    expect(mockLocalStorage.setItem).toHaveBeenCalledTimes(1); // Should only be called once for the initial load and once for the new prompt
  });

  test('can delete a saved prompt', () => {
    const prompt1 = 'Prompt 1';
    const prompt2 = 'Prompt 2';
    mockLocalStorage.getItem.mockReturnValueOnce(JSON.stringify([prompt1, prompt2]));

    render(<App />);
    expect(screen.getByText(prompt1)).toBeInTheDocument();
    expect(screen.getByText(prompt2)).toBeInTheDocument();

    const deleteButtons = screen.getAllByRole('button', { name: /X/i });
    fireEvent.click(deleteButtons[0]); // Click delete for prompt1

    expect(screen.queryByText(prompt1)).not.toBeInTheDocument();
    expect(screen.getByText(prompt2)).toBeInTheDocument();
    expect(mockLocalStorage.setItem).toHaveBeenCalledWith('apocalypseArtPrompts', JSON.stringify([prompt2]));
  });

  test('loads saved prompts from localStorage on mount', () => {
    const saved = ['Saved Prompt 1', 'Saved Prompt 2'];
    mockLocalStorage.getItem.mockReturnValue(JSON.stringify(saved));

    render(<App />);
    expect(screen.getByText('Saved Prompts')).toBeInTheDocument();
    expect(screen.getByText(saved[0])).toBeInTheDocument();
    expect(screen.getByText(saved[1])).toBeInTheDocument();
  });

  test('handles empty localStorage gracefully', () => {
    mockLocalStorage.getItem.mockReturnValue(null);
    render(<App />);
    expect(screen.getByText('No prompts saved yet.')).toBeInTheDocument();
  });

  test('custom subject overrides base subject', () => {
    render(<App />);
    const customSubjectInput = screen.getByPlaceholderText(/e.g., a sentient toaster/i);
    fireEvent.change(customSubjectInput, { target: { value: 'a sentient toaster' } });

    const generateButton = screen.getByRole('button', { name: /Generate Prompt/i });
    fireEvent.click(generateButton);

    const promptText = screen.getByText(/Your Prompt:/i).nextSibling.textContent;
    expect(promptText).toContain('a sentient toaster');
    expect(promptText).not.toContain('A lone survivor'); // Ensure base subject is overridden
  });

  test('additional details are appended to the prompt', () => {
    render(<App />);
    const additionalDetailsInput = screen.getByPlaceholderText(/e.g., glowing eyes, raining ash/i);
    fireEvent.change(additionalDetailsInput, { target: { value: 'glowing eyes and a broken umbrella' } });

    const generateButton = screen.getByRole('button', { name: /Generate Prompt/i });
    fireEvent.click(generateButton);

    const promptText = screen.getByText(/Your Prompt:/i).nextSibling.textContent;
    expect(promptText).toContain('glowing eyes and a broken umbrella');
  });
});
