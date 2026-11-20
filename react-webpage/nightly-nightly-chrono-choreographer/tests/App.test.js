import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../src/App';

// # Mock rationale: localStorage is a browser-specific API and needs to be mocked
// for deterministic, offline testing in a Node.js environment (Jest).
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: (key) => store[key] || null,
    setItem: (key, value) => { store[key] = value.toString(); },
    clear: () => { store = {}; },
    removeItem: (key) => { delete store[key]; }
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('App Component', () => {
  beforeEach(() => {
    localStorage.clear(); // Clear local storage before each test
    jest.spyOn(localStorage, 'setItem');
    jest.spyOn(localStorage, 'getItem');
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Chrono-Choreographer/i)).toBeInTheDocument();
  });

  test('adds a new task', async () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/Enter a new task/i);
    const addButton = screen.getByRole('button', { name: /Add Task/i });

    await userEvent.type(input, 'Scavenge for temporal dust');
    fireEvent.click(addButton);

    expect(screen.getByText('Scavenge for temporal dust')).toBeInTheDocument();
    expect(screen.getByText('No unassigned tasks. Time to get busy!')).not.toBeInTheDocument();
    expect(localStorage.setItem).toHaveBeenCalledWith(
      'chronoTasks',
      expect.stringContaining('Scavenge for temporal dust')
    );
  });

  test('assigns an unassigned task to a day', async () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/Enter a new task/i);
    const addButton = screen.getByRole('button', { name: /Add Task/i });

    await userEvent.type(input, 'Recalibrate temporal flux capacitor');
    fireEvent.click(addButton);

    const taskItem = screen.getByText('Recalibrate temporal flux capacitor');
    const select = taskItem.nextSibling; // The select element is next to the task span

    expect(select).toBeInTheDocument();
    await userEvent.selectOptions(select, 'Tuesday');

    expect(screen.queryByText('Recalibrate temporal flux capacitor', { selector: '.unassigned-tasks-list .task-item span' })).not.toBeInTheDocument();
    expect(screen.getByText('Recalibrate temporal flux capacitor', { selector: '.calendar-day .task-item span' })).toBeInTheDocument();
    expect(screen.getByText('Tuesday').closest('.calendar-day')).toContainElement(taskItem);
    expect(localStorage.setItem).toHaveBeenCalledWith(
      'chronoTasks',
      expect.stringContaining('"day":"Tuesday"')
    );
  });

  test('toggles task completion status', async () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/Enter a new task/i);
    const addButton = screen.getByRole('button', { name: /Add Task/i });

    await userEvent.type(input, 'Fortify bunker entrance');
    fireEvent.click(addButton);

    const taskItem = screen.getByText('Fortify bunker entrance');
    const select = taskItem.nextSibling;
    await userEvent.selectOptions(select, 'Monday');

    const assignedTask = screen.getByText('Fortify bunker entrance', { selector: '.calendar-day .task-item span' });
    const parentTaskDiv = assignedTask.closest('.task-item');

    expect(parentTaskDiv).not.toHaveClass('completed');
    fireEvent.click(parentTaskDiv);
    expect(parentTaskDiv).toHaveClass('completed');

    fireEvent.click(parentTaskDiv);
    expect(parentTaskDiv).not.toHaveClass('completed');

    expect(localStorage.setItem).toHaveBeenCalledWith(
      'chronoTasks',
      expect.stringContaining('"completed":true')
    );
  });

  test('clears completed tasks', async () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/Enter a new task/i);
    const addButton = screen.getByRole('button', { name: /Add Task/i });

    await userEvent.type(input, 'Gather mutated berries');
    fireEvent.click(addButton);
    const taskItem1 = screen.getByText('Gather mutated berries');
    await userEvent.selectOptions(taskItem1.nextSibling, 'Wednesday');
    fireEvent.click(screen.getByText('Gather mutated berries', { selector: '.calendar-day .task-item span' }).closest('.task-item')); // Mark complete

    await userEvent.type(input, 'Repair time-displacement unit');
    fireEvent.click(addButton);
    const taskItem2 = screen.getByText('Repair time-displacement unit');
    await userEvent.selectOptions(taskItem2.nextSibling, 'Wednesday');

    const clearButton = screen.getByRole('button', { name: /Clear Completed/i });
    fireEvent.click(clearButton);

    expect(screen.queryByText('Gather mutated berries')).not.toBeInTheDocument();
    expect(screen.getByText('Repair time-displacement unit')).toBeInTheDocument();
    expect(localStorage.setItem).toHaveBeenCalled();
  });

  test('loads tasks from local storage on initial render', () => {
    // # Mock rationale: Pre-populating localStorage to test loading behavior.
    localStorage.setItem('chronoTasks', JSON.stringify([
      { id: 1, name: 'Pre-existing task', day: 'Thursday', completed: false }
    ]));

    render(<App />);

    expect(localStorage.getItem).toHaveBeenCalledWith('chronoTasks');
    expect(screen.getByText('Pre-existing task')).toBeInTheDocument();
    expect(screen.getByText('Thursday').closest('.calendar-day')).toContainElement(screen.getByText('Pre-existing task').closest('.task-item'));
  });

  test('does not add empty task', async () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/Enter a new task/i);
    const addButton = screen.getByRole('button', { name: /Add Task/i });

    await userEvent.type(input, '   '); // Only whitespace
    fireEvent.click(addButton);

    expect(screen.queryByText('   ')).not.toBeInTheDocument();
    expect(localStorage.setItem).not.toHaveBeenCalledWith('chronoTasks', '[]'); // Should not save an empty task list if nothing was added
  });
});
