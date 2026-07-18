import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import TemporalEchoChamber from '../src/TemporalEchoChamber';
import '@testing-library/jest-dom';

// Mock the echoDataMap import to ensure deterministic test results
jest.mock('../src/data/echoes.json', () => ({
  banana: [
    { term: 'fruit', offset: 10, description: 'A common classification.' },
    { term: 'yellow', offset: 25, description: 'Its characteristic color.' }
  ],
  default: [
    { term: 'concept', offset: 5, description: 'A general idea.' }
  ]
}));

describe('TemporalEchoChamber', () => {
  test('renders input and button', () => {
    // # Mock rationale: Basic rendering test, no external mocks needed beyond the data.
    render(<TemporalEchoChamber />);
    expect(screen.getByPlaceholderText(/Enter a concept/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Generate Echoes/i })).toBeInTheDocument();
  });

  test('updates input value on change', () => {
    // # Mock rationale: Standard React component state update test.
    render(<TemporalEchoChamber />);
    const input = screen.getByPlaceholderText(/Enter a concept/i);
    fireEvent.change(input, { target: { value: 'test' } });
    expect(input.value).toBe('test');
  });

  test('generates echoes and displays them after button click', async () => {
    // # Mock rationale: Simulates user interaction and verifies state update
    // and rendering of child component based on mocked data.
    render(<TemporalEchoChamber />);
    const input = screen.getByPlaceholderText(/Enter a concept/i);
    const button = screen.getByRole('button', { name: /Generate Echoes/i });

    fireEvent.change(input, { target: { value: 'banana' } });
    fireEvent.click(button);

    await waitFor(() => {
      expect(screen.getByText(/Temporal Echoes of "banana"/i)).toBeInTheDocument();
      expect(screen.getByText('fruit')).toBeInTheDocument();
      expect(screen.getByText('yellow')).toBeInTheDocument();
    });
  });

  test('uses default echoes for unknown concepts', async () => {
    // # Mock rationale: Verifies fallback logic for echo generation using mocked data.
    render(<TemporalEchoChamber />);
    const input = screen.getByPlaceholderText(/Enter a concept/i);
    const button = screen.getByRole('button', { name: /Generate Echoes/i });

    fireEvent.change(input, { target: { value: 'unknown' } });
    fireEvent.click(button);

    await waitFor(() => {
      expect(screen.getByText(/Temporal Echoes of "unknown"/i)).toBeInTheDocument();
      expect(screen.getByText('concept')).toBeInTheDocument();
    });
  });

  test('does not display visualization initially', () => {
    // # Mock rationale: Ensures the visualization is hidden before any echoes are generated.
    render(<TemporalEchoChamber />);
    expect(screen.queryByText(/Temporal Echoes of/i)).not.toBeInTheDocument();
  });
});
