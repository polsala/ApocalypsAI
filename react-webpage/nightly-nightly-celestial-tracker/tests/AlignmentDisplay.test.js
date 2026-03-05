import { render, screen } from '@testing-library/react';
import AlignmentDisplay from '../src/AlignmentDisplay';

describe('AlignmentDisplay', () => {
  // Mock rationale: This is a presentational component. We test its rendering based on props.
  // No external dependencies or complex logic to mock, just prop-driven rendering.

  test('renders a list of influences when provided', () => {
    const influences = [
      'Solara-Lunaris Conjunction: A day of heightened emotional resonance!',
      'Terra Nova-Aetheria Opposition: Expect challenges in communication!'
    ];
    render(<AlignmentDisplay influences={influences} />);

    expect(screen.getByText('Cosmic Influences Today:')).toBeInTheDocument();
    expect(screen.getByText(/Solara-Lunaris Conjunction/)).toBeInTheDocument();
    expect(screen.getByText(/Terra Nova-Aetheria Opposition/)).toBeInTheDocument();
    expect(screen.getAllByRole('listitem')).toHaveLength(2);
  });

  test('renders a default message when no influences are provided', () => {
    render(<AlignmentDisplay influences={[]} />);

    expect(screen.getByText('Cosmic Influences Today:')).toBeInTheDocument();
    expect(screen.getByText('No significant alignments detected. A calm day awaits.')).toBeInTheDocument();
    expect(screen.queryByRole('listitem')).not.toBeInTheDocument();
  });

  test('renders correctly with a single influence', () => {
    const influences = ['Umbra-Solara Square: A period of introspection!'];
    render(<AlignmentDisplay influences={influences} />);

    expect(screen.getByText(/Umbra-Solara Square/)).toBeInTheDocument();
    expect(screen.getAllByRole('listitem')).toHaveLength(1);
  });
});
