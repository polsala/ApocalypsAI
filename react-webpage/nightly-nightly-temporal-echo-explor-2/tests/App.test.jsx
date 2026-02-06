import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: Simulate DOM environment for React component testing

test('renders timeline with echo events', () => {
  render(<App />);
  const echoEvents = screen.getAllByText(/Whispering Winds|Shattered Clocktower|Void Bloom/);
  expect(echoEvents).toHaveLength(3);
});

test('clicking echo event shows details', () => {
  render(<App />);
  const echoEvent = screen.getByText('Whispering Winds');
  fireEvent.click(echoEvent);
  expect(screen.getByText('A faint echo of voices carried by the wind.')).toBeInTheDocument();
});

test('simulate button triggers animation', () => {
  render(<App />);
  const simulateButton = screen.getByText('Simulate Echo Propagation');
  fireEvent.click(simulateButton);
  expect(screen.getByText('Echo propagation in progress...')).toBeInTheDocument();
});
