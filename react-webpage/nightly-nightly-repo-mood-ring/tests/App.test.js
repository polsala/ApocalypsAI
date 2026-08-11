import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../src/App';
import { setMockActivityData } from '../src/api';

// Mock rationale: To ensure deterministic and offline testing, the actual API call
// is replaced with a controlled mock. This allows tests to define specific scenarios
// without relying on external network requests or real GitHub data.

describe('App', () => {
  beforeEach(() => {
    // Reset mock data before each test to ensure isolation
    setMockActivityData([
      { id: '1', title: 'Fix: Critical bug in temporal anomaly detector', type: 'issue' },
      { id: '2', title: 'Feature: Add new whimsical emoji clock', type: 'pr' },
      { id: '3', title: 'Docs: Update README for new utility', type: 'pr' },
      { id: '4', title: 'Chore: Refactor agent_builder for clarity', type: 'pr' },
      { id: '5', title: 'Discussion: Brainstorming next-gen survival tools', type: 'discussion' },
      { id: '6', title: 'Enhancement: Improve performance of wasteland tracker', type: 'issue' },
      { id: '7', title: 'Bug: Minor UI glitch in time-ago-cli', type: 'issue' },
      { id: '8', title: 'Resolved: All known issues addressed', type: 'pr' },
      { id: '9', title: 'Urgent: Database connection failed', type: 'issue' }
    ]);
  });

  test('renders the main title', async () => {
    render(<App />);
    expect(screen.getByText(/ApocalypsAI Repo Mood Ring/i)).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.getByText(/Current Repo Mood/i)).toBeInTheDocument();
    });
  });

  test('displays "Fiery Red" mood for high negative activity', async () => {
    setMockActivityData([
      { id: '1', title: 'Urgent: Critical system failure', type: 'issue' },
      { id: '2', title: 'Bug: Major security vulnerability', type: 'issue' },
      { id: '3', title: 'Error: Deployment failed', type: 'issue' },
      { id: '4', title: 'Feature: Small UI tweak', type: 'pr' }
    ]);
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText('Fiery Red')).toBeInTheDocument();
      expect(screen.getByText(/Warning! Critical issues detected. The void is agitated!/i)).toBeInTheDocument();
    });
  });

  test('displays "Serene Green" mood for high positive activity', async () => {
    setMockActivityData([
      { id: '1', title: 'Feature: New awesome integration', type: 'pr' },
      { id: '2', title: 'Enhancement: Performance boost', type: 'pr' },
      { id: '3', title: 'Fix: All bugs resolved', type: 'issue' },
      { id: '4', title: 'Bug: Minor typo', type: 'issue' }
    ]);
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText('Serene Green')).toBeInTheDocument();
      expect(screen.getByText(/All systems go! The void hums with positive energy./i)).toBeInTheDocument();
    });
  });

  test('displays "Calm Blue" mood for high neutral activity', async () => {
    setMockActivityData([
      { id: '1', title: 'Chore: Update dependencies', type: 'pr' },
      { id: '2', title: 'Docs: Add new section', type: 'pr' },
      { id: '3', title: 'Refactor: Clean up old code', type: 'pr' },
      { id: '4', title: 'Test: Add more unit tests', type: 'pr' }
    ]);
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText('Calm Blue')).toBeInTheDocument();
      expect(screen.getByText(/Steady progress. The void is in a state of focused maintenance./i)).toBeInTheDocument();
    });
  });

  test('displays "Energetic Yellow" mood for mixed high activity', async () => {
    setMockActivityData([
      { id: '1', title: 'Feature: New UI component', type: 'pr' },
      { id: '2', title: 'Bug: Login issue', type: 'issue' },
      { id: '3', title: 'Enhancement: Improve search', type: 'pr' },
      { id: '4', title: 'Error: API timeout', type: 'issue' },
      { id: '5', title: 'Discussion: Future plans', type: 'discussion' }
    ]);
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText('Energetic Yellow')).toBeInTheDocument();
      expect(screen.getByText(/A flurry of activity! The void is buzzing with mixed signals./i)).toBeInTheDocument();
    });
  });

  test('displays "Mysterious Purple" mood for low or balanced activity', async () => {
    setMockActivityData([
      { id: '1', title: 'Small update', type: 'pr' },
      { id: '2', title: 'Minor issue', type: 'issue' }
    ]);
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText('Mysterious Purple')).toBeInTheDocument();
      expect(screen.getByText(/The void is quiet, contemplating its next move./i)).toBeInTheDocument();
    });
  });

  test('allows user to add a vibe check', async () => {
    const user = userEvent.setup();
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText(/Current Repo Mood/i)).toBeInTheDocument();
    });

    const input = screen.getByLabelText(/Add your own Vibe Check:/i);
    await user.type(input, 'Feeling productive today!');
    expect(screen.getByDisplayValue('Feeling productive today!')).toBeInTheDocument();
    expect(screen.getByText(/Your Vibe: "Feeling productive today!"/i)).toBeInTheDocument();
  });
});
