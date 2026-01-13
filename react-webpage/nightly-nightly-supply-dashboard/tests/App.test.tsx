import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

test('renders app and adds a supply item', () => {
  render(<App />);
  expect(screen.getByText(/Supply Dashboard/i)).toBeInTheDocument();

  const nameInput = screen.getByPlaceholderText('Item name') as HTMLInputElement;
  const qtyInput = screen.getByDisplayValue('1') as HTMLInputElement;
  const addButton = screen.getByText('Add');

  fireEvent.change(nameInput, { target: { value: 'Water' } });
  fireEvent.change(qtyInput, { target: { value: '5' } });
  fireEvent.click(addButton);

  expect(screen.getByText('Water: 5')).toBeInTheDocument();
});
