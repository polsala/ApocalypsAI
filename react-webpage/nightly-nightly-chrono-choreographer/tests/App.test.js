import React from 'react';
import { render, screen, fireEvent, cleanup } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// Mock localStorage for deterministic tests
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: (key) => store[key] || null,
    setItem: (key, value) => { store[key] = value.toString(); },
    removeItem: (key) => { delete store[key]; },
    clear: () => { store = {}; }
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Mock rationale: localStorage is a browser-specific API that stores data persistently.
// For unit tests, we need to ensure tests are deterministic and isolated. Mocking
// localStorage prevents actual browser storage interaction, allowing us to control
// its state and verify interactions predictably without side effects or reliance on a real browser environment.

describe('App Component', () => {
  beforeEach(() => {
    localStorage.clear(); // Clear local storage before each test
    cleanup(); // Clean up DOM after each test
  });

  test('renders the main heading', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Chrono-Choreographer/i)).toBeInTheDocument();
  });

  test('allows adding a new task', () => {
    render(<App />);
    const taskNameInput = screen.getByLabelText(/New task name/i);
    const taskDurationInput = screen.getByLabelText(/New task duration in minutes/i);
    const addButton = screen.getByRole('button', { name: /Add Task/i });

    fireEvent.change(taskNameInput, { target: { value: 'Test Task' } });
    fireEvent.change(taskDurationInput, { target: { value: '30' } });
    fireEvent.click(addButton);

    expect(screen.getByText(/Test Task \(30 min\)/i)).toBeInTheDocument();
    expect(screen.getByTitle(/Test Task \(30 min\)/i)).toBeInTheDocument(); // Check dance floor item
    expect(localStorage.getItem('chronoChoreographerTasks')).toContain('Test Task');
  });

  test('does not add a task with empty name or invalid duration', () => {
    const alertMock = jest.spyOn(window, 'alert').mockImplementation(() => {});
    // Mock rationale: window.alert is a browser-specific UI element. Mocking it prevents
    // the test from blocking on an alert dialog and allows us to assert if it was called.

    render(<App />);
    const taskNameInput = screen.getByLabelText(/New task name/i);
    const taskDurationInput = screen.getByLabelText(/New task duration in minutes/i);
    const addButton = screen.getByRole('button', { name: /Add Task/i });

    // Empty name
    fireEvent.change(taskNameInput, { target: { value: '' } });
    fireEvent.change(taskDurationInput, { target: { value: '30' } });
    fireEvent.click(addButton);
    expect(alertMock).toHaveBeenCalledTimes(1);
    expect(screen.queryByText(/ \(30 min\)/i)).not.toBeInTheDocument();

    // Invalid duration
    fireEvent.change(taskNameInput, { target: { value: 'Valid Task' } });
    fireEvent.change(taskDurationInput, { target: { value: 'abc' } });
    fireEvent.click(addButton);
    expect(alertMock).toHaveBeenCalledTimes(2);
    expect(screen.queryByText(/Valid Task/i)).not.toBeInTheDocument();

    alertMock.mockRestore();
  });

  test('allows removing a task', () => {
    render(<App />);
    const taskNameInput = screen.getByLabelText(/New task name/i);
    const taskDurationInput = screen.getByLabelText(/New task duration in minutes/i);
    const addButton = screen.getByRole('button', { name: /Add Task/i });

    fireEvent.change(taskNameInput, { target: { value: 'Task to Remove' } });
    fireEvent.change(taskDurationInput, { target: { value: '45' } });
    fireEvent.click(addButton);

    expect(screen.getByText(/Task to Remove \(45 min\)/i)).toBeInTheDocument();

    const removeButton = screen.getByRole('button', { name: /Remove task/i });
    fireEvent.click(removeButton);

    expect(screen.queryByText(/Task to Remove \(45 min\)/i)).not.toBeInTheDocument();
    expect(localStorage.getItem('chronoChoreographerTasks')).not.toContain('Task to Remove');
  });

  test('allows reordering tasks up and down', () => {
    render(<App />);
    const taskNameInput = screen.getByLabelText(/New task name/i);
    const taskDurationInput = screen.getByLabelText(/New task duration in minutes/i);
    const addButton = screen.getByRole('button', { name: /Add Task/i });

    fireEvent.change(taskNameInput, { target: { value: 'First Task' } });
    fireEvent.change(taskDurationInput, { target: { value: '10' } });
    fireEvent.click(addButton);

    fireEvent.change(taskNameInput, { target: { value: 'Second Task' } });
    fireEvent.change(taskDurationInput, { target: { value: '20' } });
    fireEvent.click(addButton);

    const tasks = screen.getAllByRole('listitem');
    expect(tasks[0]).toHaveTextContent('First Task');
    expect(tasks[1]).toHaveTextContent('Second Task');

    // Move 'Second Task' up
    const moveSecondTaskUpButton = screen.getAllByRole('button', { name: /Move task up/i })[1];
    fireEvent.click(moveSecondTaskUpButton);

    const reorderedTasks = screen.getAllByRole('listitem');
    expect(reorderedTasks[0]).toHaveTextContent('Second Task');
    expect(reorderedTasks[1]).toHaveTextContent('First Task');

    // Move 'Second Task' down (back to original position)
    const moveSecondTaskDownButton = screen.getAllByRole('button', { name: /Move task down/i })[0];
    fireEvent.click(moveSecondTaskDownButton);

    const reorderedTasksAgain = screen.getAllByRole('listitem');
    expect(reorderedTasksAgain[0]).toHaveTextContent('First Task');
    expect(reorderedTasksAgain[1]).toHaveTextContent('Second Task');
  });

  test('loads tasks from local storage on startup', () => {
    localStorage.setItem('chronoChoreographerTasks', JSON.stringify([
      { id: 1, name: 'Loaded Task 1', duration: 15 },
      { id: 2, name: 'Loaded Task 2', duration: 25 }
    ]));

    render(<App />);

    expect(screen.getByText(/Loaded Task 1 \(15 min\)/i)).toBeInTheDocument();
    expect(screen.getByText(/Loaded Task 2 \(25 min\)/i)).toBeInTheDocument();
    expect(screen.getByText(/Total Choreography Time: 40 minutes/i)).toBeInTheDocument();
  });

  test('displays total choreography time', () => {
    render(<App />);
    const taskNameInput = screen.getByLabelText(/New task name/i);
    const taskDurationInput = screen.getByLabelText(/New task duration in minutes/i);
    const addButton = screen.getByRole('button', { name: /Add Task/i });

    fireEvent.change(taskNameInput, { target: { value: 'Task A' } });
    fireEvent.change(taskDurationInput, { target: { value: '10' } });
    fireEvent.click(addButton);

    fireEvent.change(taskNameInput, { target: { value: 'Task B' } });
    fireEvent.change(taskDurationInput, { target: { value: '20' } });
    fireEvent.click(addButton);

    expect(screen.getByText(/Total Choreography Time: 30 minutes/i)).toBeInTheDocument();
  });

  test('dance floor elements reflect task durations proportionally', () => {
    render(<App />);
    const taskNameInput = screen.getByLabelText(/New task name/i);
    const taskDurationInput = screen.getByLabelText(/New task duration in minutes/i);
    const addButton = screen.getByRole('button', { name: /Add Task/i });

    fireEvent.change(taskNameInput, { target: { value: 'Short Dance' } });
    fireEvent.change(taskDurationInput, { target: { value: '10' } });
    fireEvent.click(addButton);

    fireEvent.change(taskNameInput, { target: { value: 'Long Dance' } });
    fireEvent.change(taskDurationInput, { target: { value: '30' } });
    fireEvent.click(addButton);

    const shortDanceMove = screen.getByTitle(/Short Dance \(10 min\)/i);
    const longDanceMove = screen.getByTitle(/Long Dance \(30 min\)/i);

    // 10 min out of 40 total = 25%
    expect(shortDanceMove).toHaveStyle('width: 25%');
    // 30 min out of 40 total = 75%
    expect(longDanceMove).toHaveStyle('width: 75%');
  });
});
