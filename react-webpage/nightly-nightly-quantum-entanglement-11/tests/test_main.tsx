import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import QuantumEntanglementSimulator from '../src/main';

// Mock canvas context
const mockCanvas = {
  getContext: jest.fn(() => ({
    clearRect: jest.fn(),
    beginPath: jest.fn(),
    arc: jest.fn(),
    stroke: jest.fn(),
    fill: jest.fn(),
    strokeStyle: '',
    fillStyle: '',
    lineWidth: 0,
    font: '',
    textAlign: '',
    fillText: jest.fn(),
  })),
  width: 800,
  height: 600,
};

beforeEach(() => {
  // Mock canvas element
  Object.defineProperty(window, 'HTMLCanvasElement', {
    writable: true,
    value: jest.fn(() => mockCanvas),
  });
  
  // Mock requestAnimationFrame
  global.requestAnimationFrame = jest.fn((callback) => {
    setTimeout(callback, 16);
    return 1;
  });
  
  global.cancelAnimationFrame = jest.fn();
});

afterEach(() => {
  jest.clearAllMocks();
});

describe('QuantumEntanglementSimulator', () => {
  test('renders simulator header', () => {
    render(<QuantumEntanglementSimulator />);
    expect(screen.getByText('⚛️ Quantum Entanglement Simulator')).toBeInTheDocument();
    expect(screen.getByText('A whimsical journey into quantum mechanics')).toBeInTheDocument();
  });

  test('renders control buttons', () => {
    render(<QuantumEntanglementSimulator />);
    expect(screen.getByText('➕ Create Particle')).toBeInTheDocument();
    expect(screen.getByText('🌀 Entangle Selected')).toBeInTheDocument();
    expect(screen.getByText('📡 Measure')).toBeInTheDocument();
    expect(screen.getByText('🗑️ Clear Field')).toBeInTheDocument();
  });

  test('renders measurement devices', () => {
    render(<QuantumEntanglementSimulator />);
    expect(screen.getByLabelText('Spin Meter')).toBeInTheDocument();
    expect(screen.getByLabelText('Position Detector')).toBeInTheDocument();
    expect(screen.getByLabelText('Momentum Analyzer')).toBeInTheDocument();
  });

  test('creates particle when button is clicked', async () => {
    render(<QuantumEntanglementSimulator />);
    
    const createButton = screen.getByText('➕ Create Particle');
    fireEvent.click(createButton);
    
    // Wait for canvas to be drawn
    await waitFor(() => {
      expect(mockCanvas.getContext).toHaveBeenCalled();
    });
  });

  test('toggles animation state', () => {
    render(<QuantumEntanglementSimulator />);
    
    const toggleButton = screen.getByText('⏸️ Pause');
    expect(toggleButton).toBeInTheDocument();
    
    fireEvent.click(toggleButton);
    
    expect(screen.getByText('▶️ Play')).toBeInTheDocument();
  });

  test('displays educational concepts', () => {
    render(<QuantumEntanglementSimulator />);
    
    expect(screen.getByText('📚 Quantum Concepts')).toBeInTheDocument();
    expect(screen.getByText('Superposition')).toBeInTheDocument();
    expect(screen.getByText('Entanglement')).toBeInTheDocument();
    expect(screen.getByText('Wave Function Collapse')).toBeInTheDocument();
  });

  test('initializes with empty particle list', () => {
    render(<QuantumEntanglementSimulator />);
    
    // Check stats display initial state
    expect(screen.getByText('Particles: 0')).toBeInTheDocument();
    expect(screen.getByText('Selected: 0')).toBeInTheDocument();
    expect(screen.getByText('Entangled Pairs: 0')).toBeInTheDocument();
  });

  test('canvas element is created', () => {
    render(<QuantumEntanglementSimulator />);
    
    const canvas = screen.getByRole('img', { hidden: true }) || document.querySelector('canvas');
    expect(canvas).toBeInTheDocument();
  });
});
