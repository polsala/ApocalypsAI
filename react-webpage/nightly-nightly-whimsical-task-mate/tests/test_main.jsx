import { render, screen, fireEvent } from '@testing-library/react';
import TaskMate from '../src/main';

// Mock random message selection for deterministic tests
jest.spyOn(Math, 'random').mockReturnValue(0.5);

describe('Whimsical Task Mate', () => {
  test('adds and completes tasks', () => {
    render(<TaskMate />);

    // Add task
    fireEvent.change(screen.getByPlaceholderText('Add survival task...'), {
      target: { value: 'Find water' }
    });
    fireEvent.click(screen.getByRole('button', { name: '➕' }));

    expect(screen.getByText('Find water')).toBeInTheDocument();

    // Complete task
    fireEvent.click(screen.getByText('Find water'));
    expect(screen.getByText('Find water')).toHaveClass('completed');
    expect(screen.getByText('That's the way! Now go find some snacks! 🍞')).toBeInTheDocument();
  });

  test('shows whimsical message on task completion', () => {
    render(<TaskMate />);

    fireEvent.change(screen.getByPlaceholderText('Add survival task...'), {
      target: { value: 'Build shelter' }
    });
    fireEvent.click(screen.getByRole('button', { name: '➕' }));

    fireEvent.click(screen.getByText('Build shelter'));
    expect(screen.getByText('Survival points +1! Keep it up! ⚔️')).toBeInTheDocument();
  });
});
