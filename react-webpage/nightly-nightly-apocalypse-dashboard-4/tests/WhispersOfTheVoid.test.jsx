import React from 'react';
import { render, screen } from '@testing-library/react';
import WhispersOfTheVoid from '../src/components/WhispersOfTheVoid';

describe('WhispersOfTheVoid Component', () => {
  const mockWhispers = [
    'The end is nigh, but the tea is hot.',
    'Listen to the wind, it carries secrets.',
  ];

  test('renders a list of whispers', () => {
    render(<WhispersOfTheVoid whispers={mockWhispers} />);
    expect(screen.getByText(/The end is nigh, but the tea is hot./i)).toBeInTheDocument();
    expect(screen.getByText(/Listen to the wind, it carries secrets./i)).toBeInTheDocument();
  });

  test('renders a message when there are no whispers', () => {
    render(<WhispersOfTheVoid whispers={[]} />);
    expect(screen.getByText(/The void is silent... for now./i)).toBeInTheDocument();
  });

  test('renders multiple whispers correctly', () => {
    const moreWhispers = [
      'Whisper 1',
      'Whisper 2',
      'Whisper 3',
    ];
    render(<WhispersOfTheVoid whispers={moreWhispers} />);
    expect(screen.getAllByRole('listitem').length).toBe(3);
    expect(screen.getByText(/Whisper 1/i)).toBeInTheDocument();
    expect(screen.getByText(/Whisper 3/i)).toBeInTheDocument();
  });
});
