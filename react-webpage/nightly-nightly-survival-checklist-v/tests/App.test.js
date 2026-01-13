import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

test('renders checklist items', () => {
  render(<App />);
  const items = screen.getAllByRole('checkbox');
  expect(items).toHaveLength(5);
});

test('toggles checklist items', () => {
  render(<App />);
  const checkbox = screen.getByLabelText(/Find a safe shelter/i);
  expect(checkbox).not.toBeChecked();
  fireEvent.click(checkbox);
  expect(checkbox).toBeChecked();
  const progressText = screen.getByText(/1 of 5 completed/i);
  expect(progressText).toBeInTheDocument();
});
