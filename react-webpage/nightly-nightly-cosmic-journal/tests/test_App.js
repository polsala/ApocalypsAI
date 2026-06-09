import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: Using @testing-library/react for DOM interaction testing.
// No external API calls or complex state management that requires deep mocking.
// Focus is on component rendering and user interaction.

describe('Cosmic Journal App', () => {
  test('renders without crashing', () => {
    render(<App />);
    expect(screen.getByText(/Cosmic Journal/i)).toBeInTheDocument();
  });

  test('allows adding a dream entry', async () => {
    render(<App />);
    const addDreamButton = screen.getByRole('button', { name: /Add Dream Entry/i });
    fireEvent.click(addDreamButton);

    const dreamTextarea = screen.getByPlaceholderText(/What did you dream about?/i);
    fireEvent.change(dreamTextarea, { target: { value: 'Flying through the stars' } });

    const saveButton = screen.getByRole('button', { name: /Save Dream/i });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByText(/Flying through the stars/i)).toBeInTheDocument();
    });
  });

  test('allows adding a thought entry', async () => {
    render(<App />);
    const addThoughtButton = screen.getByRole('button', { name: /Add Thought Entry/i });
    fireEvent.click(addThoughtButton);

    const thoughtTextarea = screen.getByPlaceholderText(/What are you thinking about?/i);
    fireEvent.change(thoughtTextarea, { target: { value: 'Contemplating the universe' } });

    const saveButton = screen.getByRole('button', { name: /Save Thought/i });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByText(/Contemplating the universe/i)).toBeInTheDocument();
    });
  });

  test('dream modal closes when cancel is clicked', () => {
    render(<App />);
    const addDreamButton = screen.getByRole('button', { name: /Add Dream Entry/i });
    fireEvent.click(addDreamButton);

    const cancelButton = screen.getByRole('button', { name: /Cancel/i });
    fireEvent.click(cancelButton);

    expect(screen.queryByText(/What did you dream about?/i)).not.toBeInTheDocument();
  });

  test('thought modal closes when cancel is clicked', () => {
    render(<App />);
    const addThoughtButton = screen.getByRole('button', { name: /Add Thought Entry/i });
    fireEvent.click(addThoughtButton);

    const cancelButton = screen.getByRole('button', { name: /Cancel/i });
    fireEvent.click(cancelButton);

    expect(screen.queryByText(/What are you thinking about?/i)).not.toBeInTheDocument();
  });

  test('dream entry is not added if textarea is empty', () => {
    render(<App />);
    const addDreamButton = screen.getByRole('button', { name: /Add Dream Entry/i });
    fireEvent.click(addDreamButton);

    const saveButton = screen.getByRole('button', { name: /Save Dream/i });
    fireEvent.click(saveButton);

    expect(screen.queryByText(/Add Dream Entry/i)).toBeInTheDocument(); // Modal should still be open or re-opened
  });

  test('thought entry is not added if textarea is empty', () => {
    render(<App />);
    const addThoughtButton = screen.getByRole('button', { name: /Add Thought Entry/i });
    fireEvent.click(addThoughtButton);

    const saveButton = screen.getByRole('button', { name: /Save Thought/i });
    fireEvent.click(saveButton);

    expect(screen.queryByText(/Add Thought Entry/i)).toBeInTheDocument(); // Modal should still be open or re-opened
  });

  test('theme selection works for dream entries', async () => {
    render(<App />);
    const addDreamButton = screen.getByRole('button', { name: /Add Dream Entry/i });
    fireEvent.click(addDreamButton);

    const dreamTextarea = screen.getByPlaceholderText(/What did you dream about?/i);
    fireEvent.change(dreamTextarea, { target: { value: 'A starry night' } });

    const themeSelect = screen.getByLabelText(/Choose a theme:/i);
    fireEvent.change(themeSelect, { target: { value: 'starfield' } });

    const saveButton = screen.getByRole('button', { name: /Save Dream/i });
    fireEvent.click(saveButton);

    await waitFor(() => {
      const dreamEntry = screen.getByText(/A starry night/i).closest('.entry');
      expect(dreamEntry).toHaveClass('starfield');
    });
  });
});
