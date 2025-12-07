import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import MutantPetGenerator from '../src/MutantPetGenerator';

// Mock random to ensure deterministic tests
jest.spyOn(Math, 'random').mockReturnValue(0.5);

describe('MutantPetGenerator', () => {
  test('generates valid pet with all traits', () => {
    render(<MutantPetGenerator />);
    expect(screen.getByText(/_MUTANT PET GENERATOR_/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Generate New Mutant/i })).toBeInTheDocument();
  });

  test('has valid DNA code encoding', () => {
    render(<MutantPetGenerator />);
    const input = screen.getByRole('textbox');
    expect(input.value).toBeTruthy();
    expect(atob(input.value)).toBeInstanceOf(Object);
  });

  test('regenerates different traits', () => {
    jest.spyOn(Math, 'random').mockReturnValue(0.75);
    render(<MutantPetGenerator />);
    const button = screen.getByRole('button');
    fireEvent.click(button);
    expect(screen.getAllByRole('div', { className: 'trait' }).length).toBeGreaterThan(3);
  });
});
