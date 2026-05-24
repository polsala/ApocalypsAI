import React from 'react';
import { render, screen, fireEvent, cleanup } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// Mock rationale: localStorage is a browser API and needs to be mocked for deterministic, offline tests.
const localStorageMock = (function() {
  let store = {};
  return {
    getItem: jest.fn(key => store[key] || null),
    setItem: jest.fn((key, value) => { store[key] = value.toString(); }),
    removeItem: jest.fn(key => { delete store[key]; }),
    clear: jest.fn(() => { store = {}; })
  };
})();

Object.defineProperty(window, 'localStorage', { value: localStorageMock });

describe('App', () => {
  beforeEach(() => {
    localStorage.clear(); // Clear mock storage before each test
    localStorage.getItem.mockClear();
    localStorage.setItem.mockClear();
  });

  afterEach(cleanup);

  test('renders the main title and tagline', () => {
    render(<App />);
    expect(screen.getByText('Nightly Resource Barometer')).toBeInTheDocument();
    expect(screen.getByText('Keep your post-apocalyptic supplies in check!')).toBeInTheDocument();
  });

  test('renders all initial resource gauges', () => {
    render(<App />);
    expect(screen.getByText('Hydro-Essence')).toBeInTheDocument();
    expect(screen.getByText('Sustenance Scraps')).toBeInTheDocument();
    expect(screen.getByText('Spirit Spark')).toBeInTheDocument();
    expect(screen.getByText('Mind Mettle')).toBeInTheDocument();
    expect(screen.getByText('Salvage Shards')).toBeInTheDocument();
  });

  test('resource value increases when + button is clicked', () => {
    render(<App />);
    const initialWaterValue = screen.getByText('50%'); // Initial value for Hydro-Essence
    const increaseButton = screen.getAllByRole('button', { name: '+' })[0]; // First '+' button (Hydro-Essence)

    expect(initialWaterValue).toBeInTheDocument();
    fireEvent.click(increaseButton);
    expect(screen.getByText('55%')).toBeInTheDocument();
    expect(localStorage.setItem).toHaveBeenCalledWith('apocalypsai_resources', expect.stringContaining('"Hydro-Essence":55'));
  });

  test('resource value decreases when - button is clicked', () => {
    render(<App />);
    const initialFoodValue = screen.getByText('50%'); // Initial value for Sustenance Scraps
    const decreaseButton = screen.getAllByRole('button', { name: '-' })[1]; // Second '-' button (Sustenance Scraps)

    expect(initialFoodValue).toBeInTheDocument();
    fireEvent.click(decreaseButton);
    expect(screen.getByText('45%')).toBeInTheDocument();
    expect(localStorage.setItem).toHaveBeenCalledWith('apocalypsai_resources', expect.stringContaining('"Sustenance Scraps":45'));
  });

  test('resource value does not go below 0', () => {
    render(<App />);
    const decreaseButton = screen.getAllByRole('button', { name: '-' })[4]; // Salvage Shards (initial 30%)

    // Click 6 times to go from 30 -> 0
    for (let i = 0; i < 6; i++) {
      fireEvent.click(decreaseButton);
    }
    expect(screen.getByText('0%')).toBeInTheDocument();
    fireEvent.click(decreaseButton); // Try to go below 0
    expect(screen.getByText('0%')).toBeInTheDocument(); // Should still be 0
    expect(decreaseButton).toBeDisabled();
  });

  test('resource value does not go above 100', () => {
    render(<App />);
    const increaseButton = screen.getAllByRole('button', { name: '+' })[3]; // Mind Mettle (initial 80%)

    // Click 4 times to go from 80 -> 100
    for (let i = 0; i < 4; i++) {
      fireEvent.click(increaseButton);
    }
    expect(screen.getByText('100%')).toBeInTheDocument();
    fireEvent.click(increaseButton); // Try to go above 100
    expect(screen.getByText('100%')).toBeInTheDocument(); // Should still be 100
    expect(increaseButton).toBeDisabled();
  });

  test('loads initial state from localStorage if available', () => {
    // Mock rationale: localStorage is a browser API and needs to be mocked for deterministic, offline tests.
    localStorage.setItem('apocalypsai_resources', JSON.stringify({
      'Hydro-Essence': 75,
      'Sustenance Scraps': 20,
      'Spirit Spark': 90,
      'Mind Mettle': 10,
      'Salvage Shards': 55,
    }));

    render(<App />);

    expect(localStorage.getItem).toHaveBeenCalledWith('apocalypsai_resources');
    expect(screen.getByText('75%')).toBeInTheDocument(); // Hydro-Essence
    expect(screen.getByText('20%')).toBeInTheDocument(); // Sustenance Scraps
    expect(screen.getByText('90%')).toBeInTheDocument(); // Spirit Spark
    expect(screen.getByText('10%')).toBeInTheDocument(); // Mind Mettle
    expect(screen.getByText('55%')).toBeInTheDocument(); // Salvage Shards
  });

  test('saves state to localStorage on resource change', () => {
    render(<App />);
    const increaseButton = screen.getAllByRole('button', { name: '+' })[0]; // Hydro-Essence

    fireEvent.click(increaseButton);
    expect(localStorage.setItem).toHaveBeenCalledTimes(2); // Initial save + one update
    expect(localStorage.setItem).toHaveBeenCalledWith('apocalypsai_resources', expect.stringContaining('"Hydro-Essence":55'));
  });
});
