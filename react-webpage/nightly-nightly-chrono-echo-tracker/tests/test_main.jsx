import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/main';

// Mock D3
jest.mock('d3', () => ({
  select: jest.fn(() => ({
    selectAll: jest.fn(() => ({
      remove: jest.fn(),
      data: jest.fn(() => ({
        enter: jest.fn(() => ({
          append: jest.fn(() => ({
            attr: jest.fn(() => ({
              attr: jest.fn(() => ({
                attr: jest.fn(() => ({
                  attr: jest.fn(() => ({
                    attr: jest.fn(() => ({
                      transition: jest.fn(() => ({
                        duration: jest.fn(() => ({
                          attr: jest.fn()
                        }))
                      }))
                    }))
                  }))
                }))
              }))
            }))
          })))
        })))
      })),
      append: jest.fn(() => ({
        attr: jest.fn()
      }))
    })),
    append: jest.fn(() => ({
      attr: jest.fn()
    }))
  }))
}));

// Mock Web Audio API
Object.defineProperty(window, 'AudioContext', {
  writable: true,
  value: jest.fn().mockImplementation(() => ({
    createOscillator: jest.fn(() => ({
      type: 'sine',
      frequency: { setValueAtTime: jest.fn() },
      start: jest.fn(),
      stop: jest.fn()
    })),
    createGain: jest.fn(() => ({
      gain: { setValueAtTime: jest.fn(), exponentialRampToValueAtTime: jest.fn() },
      connect: jest.fn()
    })),
    destination: {}
  }))
});

describe('Nightly Chrono Echo Tracker', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders main components', () => {
    render(<App />);
    
    expect(screen.getByText('🌌 Nightly Chrono Echo Tracker 🌌')).toBeInTheDocument();
    expect(screen.getByText('Monitoring temporal distortions across the wasteland')).toBeInTheDocument();
    expect(screen.getByText('Time Zone:')).toBeInTheDocument();
    expect(screen.getByText('⏸️ Pause Detection')).toBeInTheDocument();
    expect(screen.getByText('🎯 Generate Manual Anomaly')).toBeInTheDocument();
  });

  test('displays initial state with no anomalies', () => {
    render(<App />);
    
    expect(screen.getByText('No anomalies detected yet. The timeline is stable... for now.')).toBeInTheDocument();
    expect(screen.getByText('⚠️ Temporal anomalies detected: 0')).toBeInTheDocument();
  });

  test('generates anomaly when manual button is clicked', async () => {
    render(<App />);
    
    const manualBtn = screen.getByText('🎯 Generate Manual Anomaly');
    fireEvent.click(manualBtn);
    
    await waitFor(() => {
      expect(screen.queryByText('No anomalies detected yet. The timeline is stable... for now.')).not.toBeInTheDocument();
    });
    
    expect(screen.getByText(/Temporal anomalies detected: 1/)).toBeInTheDocument();
  });

  test('toggles play/pause state', () => {
    render(<App />);
    
    const playBtn = screen.getByText('⏸️ Pause Detection');
    expect(playBtn).toBeInTheDocument();
    
    fireEvent.click(playBtn);
    
    expect(screen.getByText('▶️ Resume Detection')).toBeInTheDocument();
    
    fireEvent.click(playBtn);
    
    expect(screen.getByText('⏸️ Pause Detection')).toBeInTheDocument();
  });

  test('time zone selector has correct options', () => {
    render(<App />);
    
    const timezoneSelect = screen.getByDisplayValue('UTC');
    expect(timezoneSelect).toBeInTheDocument();
    
    fireEvent.change(timezoneSelect, { target: { value: 'EST' } });
    expect(screen.getByDisplayValue('EST')).toBeInTheDocument();
  });

  test('D3 visualization is initialized', () => {
    render(<App />);
    
    expect(require('d3').select).toHaveBeenCalled();
  });

  test('Web Audio API is used for sound generation', () => {
    render(<App />);
    
    const manualBtn = screen.getByText('🎯 Generate Manual Anomaly');
    fireEvent.click(manualBtn);
    
    expect(window.AudioContext).toHaveBeenCalled();
  });
});
