import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

test('initial rating is average of default values', () => {
  render(<App />);
  const rating = screen.getByText(/Survival Rating:/i);
  expect(rating).toHaveTextContent('Survival Rating: 50%');
});

test('changing water slider updates rating', () => {
  render(<App />);
  const sliders = screen.getAllByRole('slider');
  const waterSlider = sliders[0]; // first slider corresponds to water
  fireEvent.change(waterSlider, { target: { value: '80' } });
  const rating = screen.getByText(/Survival Rating:/i);
  // water 80, food 50, ammo 50 => average = 60
  expect(rating).toHaveTextContent('Survival Rating: 60%');
});
