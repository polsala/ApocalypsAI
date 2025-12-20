import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// Mock the CSS imports
jest.mock('../src/App.css', () => ({}));
jest.mock('../src/index.css', () => ({}));

describe('Nightly Quantum Cache Visualizer', () => {
  beforeEach(() => {
    render(<App />);
  });

  test('renders main title and header', () => {
    expect(screen.getByText('🌌 Nightly Quantum Cache Visualizer')).toBeInTheDocument();
    expect(screen.getByText('Watch your cache performance as quantum waves')).toBeInTheDocument();
  });

  test('displays initial metrics correctly', () => {
    expect(screen.getByText(/Current Item: —/)).toBeInTheDocument();
    expect(screen.getByText(/Cache Size: 0/8/)).toBeInTheDocument();
    expect(screen.getByText(/Hits: 0/)).toBeInTheDocument();
    expect(screen.getByText(/Misses: 0/)).toBeInTheDocument();
    expect(screen.getByText(/Hit Rate: 0.0%/)).toBeInTheDocument();
  });

  test('cache bins display correctly', () => {
    const cacheBins = screen.getAllByText('—');
    expect(cacheBins.length).toBeGreaterThan(0);
  });

  test('policy selector has correct options', () => {
    const policySelect = screen.getByDisplayValue('LRU');
    expect(policySelect).toBeInTheDocument();
    
    fireEvent.change(policySelect, { target: { value: 'LFU' } });
    expect(policySelect.value).toBe('LFU');
    
    fireEvent.change(policySelect, { target: { value: 'FIFO' } });
    expect(policySelect.value).toBe('FIFO');
  });

  test('cache size input works', () => {
    const cacheSizeInput = screen.getByDisplayValue('8');
    expect(cacheSizeInput).toBeInTheDocument();
    
    fireEvent.change(cacheSizeInput, { target: { value: '12' } });
    expect(cacheSizeInput.value).toBe('12');
  });

  test('workload input works', () => {
    const workloadInput = screen.getByDisplayValue('1 2 3 4 1 2 5 1 2 3 4 5 6 7 8 1 2 3');
    expect(workloadInput).toBeInTheDocument();
    
    fireEvent.change(workloadInput, { target: { value: '1 1 2 2 3 3' } });
    expect(workloadInput.value).toBe('1 1 2 2 3 3');
  });

  test('speed slider works', () => {
    const speedSlider = screen.getByDisplayValue('500');
    expect(speedSlider).toBeInTheDocument();
    
    fireEvent.change(speedSlider, { target: { value: '1000' } });
    expect(speedSlider.value).toBe('1000');
  });

  test('play button toggles correctly', () => {
    const playButton = screen.getByText('▶️ Play');
    expect(playButton).toBeInTheDocument();
    
    fireEvent.click(playButton);
    expect(screen.getByText('⏸ Pause')).toBeInTheDocument();
    
    fireEvent.click(screen.getByText('⏸ Pause'));
    expect(screen.getByText('▶️ Play')).toBeInTheDocument();
  });

  test('step button works when not playing', () => {
    const stepButton = screen.getByText('⏭ Step');
    expect(stepButton).not.toBeDisabled();
    
    fireEvent.click(stepButton);
    
    // After one step, cache should have one item
    expect(screen.getByText(/Cache Size: 1/8/)).toBeInTheDocument();
    expect(screen.getByText(/Misses: 1/)).toBeInTheDocument();
  });

  test('reset button works', () => {
    // First do a step
    fireEvent.click(screen.getByText('⏭ Step'));
    expect(screen.getByText(/Cache Size: 1/8/)).toBeInTheDocument();
    
    // Then reset
    fireEvent.click(screen.getByText('🔄 Reset'));
    expect(screen.getByText(/Cache Size: 0/8/)).toBeInTheDocument();
    expect(screen.getByText(/Misses: 0/)).toBeInTheDocument();
  });

  test('timeline shows entries after steps', async () => {
    // Do a few steps
    fireEvent.click(screen.getByText('⏭ Step'));
    fireEvent.click(screen.getByText('⏭ Step'));
    fireEvent.click(screen.getByText('⏭ Step'));
    
    await waitFor(() => {
      expect(screen.getByText('Step 1')).toBeInTheDocument();
      expect(screen.getByText('Step 2')).toBeInTheDocument();
      expect(screen.getByText('Step 3')).toBeInTheDocument();
    });
  });

  test('hit rate calculation is correct', async () => {
    // Simulate a hit by repeating the first item
    const workloadInput = screen.getByDisplayValue('1 2 3 4 1 2 5 1 2 3 4 5 6 7 8 1 2 3');
    fireEvent.change(workloadInput, { target: { value: '1 1 2 2' } });
    
    // First step - miss
    fireEvent.click(screen.getByText('⏭ Step'));
    expect(screen.getByText(/Misses: 1/)).toBeInTheDocument();
    
    // Second step - hit
    fireEvent.click(screen.getByText('⏭ Step'));
    expect(screen.getByText(/Hits: 1/)).toBeInTheDocument();
    expect(screen.getByText(/Hit Rate: 50.0%/)).toBeInTheDocument();
  });

  test('visualization shows quantum wave', () => {
    const waveContainer = screen.getByRole('img', { hidden: true }) ||
                         document.querySelector('.wave-container');
    expect(waveContainer).toBeInTheDocument();
  });

  test('legend displays correctly', () => {
    expect(screen.getByText('🟢 Hit')).toBeInTheDocument();
    expect(screen.getByText('🔴 Miss')).toBeInTheDocument();
  });

  // Mock rationale: These tests verify the React component renders correctly,
  // handles user interactions, and maintains proper state. They use Jest and
  // React Testing Library for deterministic, offline testing without external
  // dependencies.
});
