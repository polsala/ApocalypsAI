import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import '@testing-library/jest-dom';

// Mock localStorage for deterministic tests
const localStorageMock = (function () {
  let store = {};
  return {
    getItem(key) {
      return store[key] || null;
    },
    setItem(key, value) {
      store[key] = value.toString();
    },
    clear() {
      store = {};
    },
    removeItem(key) {
      delete store[key];
    },
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('App', () => {
  beforeEach(() => {
    localStorage.clear(); // # Mock rationale: Clear localStorage before each test to ensure test isolation and deterministic state.
  });

  test('renders App title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Whisperscape Weaver/i)).toBeInTheDocument();
  });

  test('adds a whisper and displays it', () => {
    render(<App />);
    const inputElement = screen.getByLabelText(/Whisper input/i);
    const buttonElement = screen.getByRole('button', { name: /Weave Whisper/i });

    fireEvent.change(inputElement, { target: { value: 'Test whisper 1' } });
    fireEvent.click(buttonElement);

    expect(screen.getByText(/Test whisper 1/i)).toBeInTheDocument();
    expect(inputElement).toHaveValue(''); // Input should clear after submission
  });

  test('persists whispers to local storage', () => {
    render(<App />);
    const inputElement = screen.getByLabelText(/Whisper input/i);
    const buttonElement = screen.getByRole('button', { name: /Weave Whisper/i });

    fireEvent.change(inputElement, { target: { value: 'Persistent whisper' } });
    fireEvent.click(buttonElement);

    // # Mock rationale: Directly check the mocked localStorage to verify persistence.
    // This avoids needing to re-render the component to check state.
    const savedWhispers = JSON.parse(localStorage.getItem('whisperscape-whispers'));
    expect(savedWhispers).toHaveLength(1);
    expect(savedWhispers[0].text).toBe('Persistent whisper');
  });

  test('loads whispers from local storage on initial render', () => {
    // # Mock rationale: Pre-populate localStorage before rendering to simulate existing data.
    localStorage.setItem('whisperscape-whispers', JSON.stringify([{ id: 1, text: 'Loaded whisper' }]));
    render(<App />);
    expect(screen.getByText(/Loaded whisper/i)).toBeInTheDocument();
  });
});
