import React from 'react';
import { render, screen } from '@testing-library/react';
import ThreatLevel from '../src/components/ThreatLevel';

describe('ThreatLevel Component', () => {
  test('renders threat level percentage', () => {
    render(<ThreatLevel level={50} />);
    expect(screen.getByText(/50%/i)).toBeInTheDocument();
  });

  test('renders appropriate message for low threat level', () => {
    render(<ThreatLevel level={25} />);
    expect(screen.getByText(/Calm Before the Storm/i)).toBeInTheDocument();
  });

  test('renders appropriate message for medium threat level', () => {
    render(<ThreatLevel level={60} />);
    expect(screen.getByText(/Heightened Alert/i)).toBeInTheDocument();
  });

  test('renders appropriate message for high threat level', () => {
    render(<ThreatLevel level={85} />);
    expect(screen.getByText(/Imminent Danger/i)).toBeInTheDocument();
  });

  test('renders the correct color for low threat level', () => {
    render(<ThreatLevel level={20} />);
    const gauge = screen.getByText(/20%/i).parentElement.parentElement;
    expect(gauge).toHaveClass('bg-green-500');
  });

  test('renders the correct color for medium threat level', () => {
    render(<ThreatLevel level={50} />);
    const gauge = screen.getByText(/50%/i).parentElement.parentElement;
    expect(gauge).toHaveClass('bg-yellow-500');
  });

  test('renders the correct color for high threat level', () => {
    render(<ThreatLevel level={90} />);
    const gauge = screen.getByText(/90%/i).parentElement.parentElement;
    expect(gauge).toHaveClass('bg-red-500');
  });

  test('renders 0% correctly', () => {
    render(<ThreatLevel level={0} />);
    expect(screen.getByText(/0%/i)).toBeInTheDocument();
    expect(screen.getByText(/Calm Before the Storm/i)).toBeInTheDocument();
  });

  test('renders 100% correctly', () => {
    render(<ThreatLevel level={100} />);
    expect(screen.getByText(/100%/i)).toBeInTheDocument();
    expect(screen.getByText(/Imminent Danger/i)).toBeInTheDocument();
  });
});
