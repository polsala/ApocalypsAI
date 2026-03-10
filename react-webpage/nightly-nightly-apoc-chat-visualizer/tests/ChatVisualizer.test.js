import { render, screen, waitFor } from '@testing-library/react';
import ChatVisualizer from '../src/ChatVisualizer';

// Mock rationale: We mock timers to control animation timing in tests
jest.useFakeTimers();

describe('ChatVisualizer', () => {
  const mockMessages = [
    { user: 'Alice', text: 'Hello world!' },
    { user: 'Bob', text: 'Greetings!' }
  ];

  it('renders initial empty state', () => {
    render(<ChatVisualizer messages={[]} />);
    expect(screen.queryByText(/Alice:/)).not.toBeInTheDocument();
  });

  it('displays typing indicator when loading messages', async () => {
    render(<ChatVisualizer messages={mockMessages} />);
    expect(screen.getByText(/Alice is typing/i)).toBeInTheDocument();
    jest.advanceTimersByTime(800);
    await waitFor(() => expect(screen.getByText(/Hello world!/)).toBeInTheDocument());
  });

  it('shows messages after typing delay', async () => {
    render(<ChatVisualizer messages={mockMessages} />);
    jest.advanceTimersByTime(1500);
    jest.advanceTimersByTime(800);
    await waitFor(() => expect(screen.getByText(/Greetings!/)).toBeInTheDocument());
  });
});
