import { render, screen } from '@testing-library/react';
import WorkflowNode from '../src/WorkflowNode';

describe('WorkflowNode', () => {
  // # Mock rationale: Provides predefined workflow objects to test how the component
  // renders different statuses and moods in isolation, without relying on dynamic data.
  const mockWorkflowSuccess = {
    id: 'wf-1',
    name: 'Generator Openrouter',
    status: 'success',
    lastRun: '1/1/2024, 12:00:00 PM',
    mood: { emoji: '✨', description: 'Joyful' }
  };

  const mockWorkflowFailure = {
    id: 'wf-2',
    name: 'Nightly Self Heal',
    status: 'failure',
    lastRun: '1/1/2024, 1:00:00 PM',
    mood: { emoji: '🔥', description: 'Fiery' }
  };

  const mockWorkflowRunning = {
    id: 'wf-3',
    name: 'PR Auto Review',
    status: 'running',
    lastRun: '1/1/2024, 2:00:00 PM',
    mood: { emoji: '⚡', description: 'Energetic' }
  };

  test('renders workflow name and last run time', () => {
    render(<WorkflowNode workflow={mockWorkflowSuccess} />);
    expect(screen.getByText('Generator Openrouter')).toBeInTheDocument();
    expect(screen.getByText('Last Run: 1/1/2024, 12:00:00 PM')).toBeInTheDocument();
  });

  test('renders success status correctly', () => {
    render(<WorkflowNode workflow={mockWorkflowSuccess} />);
    const statusElement = screen.getByText('Status: Success');
    expect(statusElement).toBeInTheDocument();
    expect(statusElement).toHaveClass('status-success');
  });

  test('renders failure status correctly', () => {
    render(<WorkflowNode workflow={mockWorkflowFailure} />);
    const statusElement = screen.getByText('Status: Failure');
    expect(statusElement).toBeInTheDocument();
    expect(statusElement).toHaveClass('status-failure');
  });

  test('renders running status correctly', () => {
    render(<WorkflowNode workflow={mockWorkflowRunning} />);
    const statusElement = screen.getByText('Status: Running');
    expect(statusElement).toBeInTheDocument();
    expect(statusElement).toHaveClass('status-running');
  });

  test('renders mood emoji with correct aria-label', () => {
    render(<WorkflowNode workflow={mockWorkflowSuccess} />);
    const emojiElement = screen.getByRole('img', { name: 'Joyful' });
    expect(emojiElement).toBeInTheDocument();
    expect(emojiElement).toHaveTextContent('✨');
  });
});
