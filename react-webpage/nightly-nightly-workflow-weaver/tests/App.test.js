import { render, screen, waitFor } from '@testing-library/react';
import App from '../src/App';
import { fetchWorkflows } from '../src/api';

// # Mock rationale: Mocks the `fetchWorkflows` function to control the data returned,
// allowing testing of loading states, error states, and rendering of components
// with specific workflow data without actual network calls.
jest.mock('../src/api', () => ({
  fetchWorkflows: jest.fn()
}));

describe('App', () => {
  const mockWorkflows = [
    {
      id: 'wf-1',
      name: 'Generator Openrouter',
      status: 'success',
      lastRun: '1/1/2024, 12:00:00 PM',
      mood: { emoji: '✨', description: 'Joyful' }
    },
    {
      id: 'wf-2',
      name: 'Nightly Self Heal',
      status: 'failure',
      lastRun: '1/1/2024, 1:00:00 PM',
      mood: { emoji: '🔥', description: 'Fiery' }
    }
  ];

  beforeEach(() => {
    fetchWorkflows.mockClear();
  });

  test('renders loading message initially', () => {
    fetchWorkflows.mockReturnValueOnce(new Promise(() => {})); // Never resolve to keep it loading
    render(<App />);
    expect(screen.getByText(/Weaving the cosmic threads.../i)).toBeInTheDocument();
  });

  test('renders workflows after successful fetch', async () => {
    fetchWorkflows.mockResolvedValueOnce({ success: true, data: mockWorkflows });
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Nightly Workflow Weaver')).toBeInTheDocument();
      expect(screen.getByText('Generator Openrouter')).toBeInTheDocument();
      expect(screen.getByText('Nightly Self Heal')).toBeInTheDocument();
      expect(screen.queryByText(/Weaving the cosmic threads.../i)).not.toBeInTheDocument();
    });
  });

  test('renders error message on API failure', async () => {
    fetchWorkflows.mockResolvedValueOnce({ success: false, error: 'Failed to fetch cosmic threads.' });
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/Error: Failed to fetch cosmic threads./i)).toBeInTheDocument();
      expect(screen.queryByText(/Weaving the cosmic threads.../i)).not.toBeInTheDocument();
    });
  });

  test('renders generic error message on unexpected error', async () => {
    fetchWorkflows.mockRejectedValueOnce(new Error('Network error'));
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/An unexpected cosmic disturbance occurred./i)).toBeInTheDocument();
      expect(screen.queryByText(/Weaving the cosmic threads.../i)).not.toBeInTheDocument();
    });
  });
});
