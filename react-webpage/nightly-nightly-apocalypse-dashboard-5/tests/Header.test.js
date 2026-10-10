import React from 'react';
import { render, screen } from '@testing-library/react';
import Header from '../src/components/Header';

describe('Header Component', () => {
  test('renders the correct title', () => {
    const testTitle = 'ApocalypsAI Dashboard';
    render(<Header title={testTitle} />);
    const headerElement = screen.getByText(testTitle);
    expect(headerElement).toBeInTheDocument();
  });

  test('renders the apocalypse icon', () => {
    render(<Header title="Test Title" />);
    const iconElement = screen.getByText('🌌');
    expect(iconElement).toBeInTheDocument();
  });
});
