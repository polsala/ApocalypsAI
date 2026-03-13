import React from 'react';
import { render, screen } from '@testing-library/react';
import VoidWhispers from '../src/components/VoidWhispers';

describe('VoidWhispers Component', () => {
  it('renders the title', () => {
    render(<VoidWhispers message="" />);
    expect(screen.getByText('Whispers of the Void')).toBeInTheDocument();
  });

  it('renders the provided whisper message', () => {
    const mockMessage = 'The stars are not in your favor.';
    render(<VoidWhispers message={mockMessage} />);
    expect(screen.getByText(mockMessage)).toBeInTheDocument();
  });

  it('renders a default message when no message is provided', () => {
    render(<VoidWhispers message="" />);
    expect(screen.getByText('The void is silent...')).toBeInTheDocument();
  });

  it('renders a default message when message is null', () => {
    render(<VoidWhispers message={null} />);
    expect(screen.getByText('The void is silent...')).toBeInTheDocument();
  });
});
