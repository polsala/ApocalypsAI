import React from 'react';
import { render, screen } from '@testing-library/react';
import Dashboard from '../src/index';

// Mock deterministic state values
jest.useFakeTimers();

const testValues = {
  cpu: 42,
  memory: 68,
  disk: 85
};

const setup = () => {
  render(<Dashboard />);
  // Force state to test values
  Object.keys(testValues).forEach(key => {
    const input = screen.getByRole('progressbar');
    expect(input).toHaveValue(testValues[key]);
  });
};

test('Displays correct survival status for CPU', () => {
  setup();
  expect(screen.getByText('CRITICAL: Mutant hordes approaching!')).toBeInTheDocument();
});

test('Displays correct survival status for Memory', () => {
  setup();
  expect(screen.getByText('WARNING: Resources thinning...')).toBeInTheDocument();
});

test('Displays correct survival status for Disk', () => {
  setup();
  expect(screen.getByText('CRITICAL: Mutant hordes approaching!')).toBeInTheDocument();
});

test('Button controls exist', () => {
  setup();
  expect(screen.getByText('+10 CPU')).toBeInTheDocument();
  expect(screen.getByText('+10 Memory')).toBeInTheDocument();
  expect(screen.getByText('+10 Disk')).toBeInTheDocument();
});
