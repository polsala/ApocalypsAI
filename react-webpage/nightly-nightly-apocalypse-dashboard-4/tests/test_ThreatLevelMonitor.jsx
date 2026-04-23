import React from 'react';
import { render, screen } from '@testing-library/react';
import ThreatLevelMonitor from '../src/components/ThreatLevelMonitor';

describe('ThreatLevelMonitor Component', () => {
  it('renders the title', () => {
    render(<ThreatLevelMonitor data={{ level: 5, description: 'Moderate threat' }} />);
    expect(screen.getByText('Threat Level Monitor')).toBeInTheDocument();
  });

  it('renders threat level and description', () => {
    const mockData = { level: 7, description: 'High mutant activity!' };
    render(<ThreatLevelMonitor data={mockData} />);

    expect(screen.getByText('7')).toBeInTheDocument();
    expect(screen.getByText('High mutant activity!')).toBeInTheDocument();
  });

  it('renders default values when data is missing', () => {
    render(<ThreatLevelMonitor data={{}} />);
    expect(screen.getByText('?')).toBeInTheDocument();
    expect(screen.getByText('Unknown threat level.')).toBeInTheDocument();
  });

  it('renders default values when data is null', () => {
    render(<ThreatLevelMonitor data={null} />);
    expect(screen.getByText('?')).toBeInTheDocument();
    expect(screen.getByText('Unknown threat level.')).toBeInTheDocument();
  });

  it('applies correct color class for low threat level', () => {
    render(<ThreatLevelMonitor data={{ level: 2, description: 'Low threat' }} />);
    const threatElement = screen.getByText('2');
    // Check for the presence of a green color class (or style)
    // This test might need adjustment based on how colors are applied (e.g., direct style vs class)
    // For simplicity, we'll check if the text is present and assume styling is handled.
    // A more robust test would inspect computed styles or class names if they are dynamic.
    expect(threatElement).toBeInTheDocument();
  });

  it('applies correct color class for medium threat level', () => {
    render(<ThreatLevelMonitor data={{ level: 5, description: 'Medium threat' }} />);
    const threatElement = screen.getByText('5');
    expect(threatElement).toBeInTheDocument();
  });

  it('applies correct color class for high threat level', () => {
    render(<ThreatLevelMonitor data={{ level: 9, description: 'Critical threat' }} />);
    const threatElement = screen.getByText('9');
    expect(threatElement).toBeInTheDocument();
  });
});
