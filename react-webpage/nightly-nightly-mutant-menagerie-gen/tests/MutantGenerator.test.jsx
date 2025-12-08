import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import MutantGenerator from '../src/MutantGenerator';

// Mock console.log for output verification
jest.spyOn(console, 'log').mockImplementation(() => {});

describe('MutantGenerator', () => {
  test('renders with default traits', () => {
    render(<MutantGenerator />);
    expect(screen.getByText('Mutant Traits')).toBeInTheDocument();
    expect(screen.getByDisplayValue('glowing green')).toBeInTheDocument();
  });

  test('updates traits when selecting options', () => {
    render(<MutantGenerator />);
    const eyeSelect = screen.getByLabelText('Eyes:');
    fireEvent.change(eyeSelect, { target: { value: 'radioactive blue' } });
    expect(eyeSelect.value).toBe('radioactive blue');
  });

  test('generates mutant with selected traits', () => {
    render(<MutantGenerator />);
    fireEvent.change(screen.getByLabelText('Eyes:'), { target: { value: 'laser vision' } });
    fireEvent.change(screen.getByLabelText('Limbs:'), { target: { value: 'crushing claws' } });
    fireEvent.change(screen.getByLabelText('Skin:'), { target: { value: 'bioluminescent' } });
    fireEvent.change(screen.getByLabelText('Mutation Level:'), { target: { value: 75 } });
    
    fireEvent.click(screen.getByText('Generate Mutant'));
    expect(console.log).toHaveBeenCalledWith(
      expect.objectContaining({
        name: expect.stringMatching(/Mutant [A-Z][a-z]+/),
        eyes: 'laser vision',
        limbs: 'crushing claws',
        skin: 'bioluminescent',
        mutationLevel: 75
      })
    );
  });
});
