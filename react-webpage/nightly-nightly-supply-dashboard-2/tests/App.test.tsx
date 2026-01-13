import '@testing-library/jest-dom';
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

test('adds an item and updates totals', () => {
  render(<App />);

  // Fill form fields
  fireEvent.change(screen.getByPlaceholderText('Item name'), { target: { value: 'Water' } });
  fireEvent.change(screen.getByPlaceholderText('Weight (kg)'), { target: { value: '2' } });
  fireEvent.change(screen.getByPlaceholderText('Quantity'), { target: { value: '3' } });
  fireEvent.change(screen.getByPlaceholderText('Value (credits)'), { target: { value: '5' } });

  // Submit the form
  fireEvent.click(screen.getByText('Add'));

  // Verify the new row appears
  expect(screen.getByText('Water')).toBeInTheDocument();
  expect(screen.getAllByText('2')[0]).toBeInTheDocument(); // weight
  expect(screen.getByText('3')).toBeInTheDocument(); // quantity
  expect(screen.getByText('5')).toBeInTheDocument(); // value

  // Verify aggregated totals
  expect(screen.getByText('Total weight: 6 kg')).toBeInTheDocument();
  expect(screen.getByText('Total value: 15 credits')).toBeInTheDocument();
});

