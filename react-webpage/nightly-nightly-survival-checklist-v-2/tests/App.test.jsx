import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

test('renders checklist and updates progress', () => {
  render(<App />);
  const progressBar = screen.getByRole('progressbar');
  expect(progressBar).toHaveAttribute('value', '0');
  const checkboxes = screen.getAllByRole('checkbox');
  expect(checkboxes.length).toBe(4);
  fireEvent.click(checkboxes[0]);
  expect(progressBar).toHaveAttribute('value', '25');
  fireEvent.click(checkboxes[1]);
  expect(progressBar).toHaveAttribute('value', '50');
});
