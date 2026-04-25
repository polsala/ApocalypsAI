import { render, screen } from '@testing-library/react';
import App from '../src/App';

describe('App Component', () => {
  test('renders the main SkillTree component', () => {
    // Mock rationale: App component primarily renders SkillTree.
    // We're testing if App correctly includes SkillTree.
    // Detailed SkillTree logic is tested in SkillTree.test.js.
    render(<App />);
    const skillTreeTitle = screen.getByText(/Survival Skill Tree/i);
    expect(skillTreeTitle).toBeInTheDocument();
  });
});
