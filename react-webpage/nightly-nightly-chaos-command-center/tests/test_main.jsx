import { render, screen, fireEvent } from '@testing-library/react';
import ChaosCenter from '../src/main';

// Mock rationale: Testing basic component behavior without external dependencies
// Verifies UI elements render and event handlers work

test('renders chaos center with interactive elements', () => {
  render(<ChaosCenter />);
  expect(screen.getByText('🚀 Chaos Command Center')).toBeInTheDocument();
  const button = screen.getByRole('button', { name: /trigger chaos/i });
  fireEvent.click(button);
  expect(screen.getAllByRole('div').length).toBeGreaterThan(0);
});

test('displays event intensity visualization', () => {
  render(<ChaosCenter />);
  const button = screen.getByRole('button');
  fireEvent.click(button);
  const eventBox = screen.getAllByRole('div').find(d => d.style.backgroundColor);
  expect(eventBox.style.backgroundColor).toContain('rgba');
});
