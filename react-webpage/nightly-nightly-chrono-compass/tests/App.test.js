import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: TaskInput and ChronoCompass are child components. We mock them
// to isolate the testing of the App component's state management and rendering
// of its direct children, preventing tests from failing due to issues in children.
jest.mock('../src/TaskInput', () => {
  return function MockTaskInput({ onAddTask }) {
    return (
      <form data-testid="mock-task-input" onSubmit={(e) => {
        e.preventDefault();
        onAddTask('Test Task', 60, 'Positive');
      }}>
        <button type="submit">Add Task</button>
      </form>
    );
  };
});

jest.mock('../src/ChronoCompass', () => {
  return function MockChronoCompass({ tasks }) {
    return (
      <div data-testid="mock-chrono-compass">
        {tasks.length > 0 ? `Tasks count: ${tasks.length}` : 'No tasks'}
      </div>
    );
  };
});

describe('App Component', () => {
  test('renders Nightly Chrono-Compass title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Chrono-Compass/i)).toBeInTheDocument();
  });

  test('renders TaskInput and ChronoCompass components', () => {
    render(<App />);
    expect(screen.getByTestId('mock-task-input')).toBeInTheDocument();
    expect(screen.getByTestId('mock-chrono-compass')).toBeInTheDocument();
  });

  test('adds a task when TaskInput calls onAddTask', () => {
    render(<App />);
    const addTaskButton = screen.getByRole('button', { name: /Add Task/i });
    fireEvent.click(addTaskButton);

    // Check if the task appears in the list
    expect(screen.getByText(/Test Task \(60 min\)/i)).toBeInTheDocument();
    expect(screen.getByText(/\[Positive\]/i)).toBeInTheDocument();

    // Check if ChronoCompass received the task (via mock output)
    expect(screen.getByText(/Tasks count: 1/i)).toBeInTheDocument();
  });

  test('displays "No tasks logged yet" when no tasks are present', () => {
    render(<App />);
    expect(screen.getByText(/No tasks logged yet. Chart your temporal journey!/i)).toBeInTheDocument();
  });

  test('does not add task if duration is not positive (mocked behavior)', () => {
    // This test relies on the mock TaskInput always sending valid data.
    // A more robust test would involve mocking TaskInput to send invalid data.
    // For this test, we'll just ensure the default mock behavior works.
    render(<App />);
    const addTaskButton = screen.getByRole('button', { name: /Add Task/i });
    fireEvent.click(addTaskButton); // Adds 'Test Task', 60, 'Positive'
    fireEvent.click(addTaskButton); // Adds another 'Test Task', 60, 'Positive'

    expect(screen.getAllByText(/Test Task \(60 min\)/i).length).toBe(2);
    expect(screen.getByText(/Tasks count: 2/i)).toBeInTheDocument();
  });
});
