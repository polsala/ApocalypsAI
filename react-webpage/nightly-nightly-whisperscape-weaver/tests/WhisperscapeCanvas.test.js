import { render, screen } from '@testing-library/react';
import WhisperscapeCanvas from '../src/components/WhisperscapeCanvas';
import '@testing-library/jest-dom';

describe('WhisperscapeCanvas', () => {
  test('renders "No whispers yet" message when whispers array is empty', () => {
    render(<WhisperscapeCanvas whispers={[]} />);
    expect(screen.getByText(/No whispers yet. Be the first to weave one!/i)).toBeInTheDocument();
  });

  test('renders whispers when provided', () => {
    const testWhispers = [
      { id: 1, text: 'First whisper' },
      { id: 2, text: 'Second whisper' },
    ];
    render(<WhisperscapeCanvas whispers={testWhispers} />);
    expect(screen.getByText(/First whisper/i)).toBeInTheDocument();
    expect(screen.getByText(/Second whisper/i)).toBeInTheDocument();
    expect(screen.queryByText(/No whispers yet/i)).not.toBeInTheDocument();
  });

  test('renders correct number of whisper bubbles', () => {
    const testWhispers = [
      { id: 1, text: 'A' },
      { id: 2, text: 'B' },
      { id: 3, text: 'C' },
    ];
    render(<WhisperscapeCanvas whispers={testWhispers} />);
    const whisperBubbles = screen.getAllByText(/whisper/i, { selector: '.whisper-bubble' }); // # Mock rationale: Use a specific selector to ensure we're counting the actual whisper elements.
    expect(whisperBubbles).toHaveLength(3);
  });
});
