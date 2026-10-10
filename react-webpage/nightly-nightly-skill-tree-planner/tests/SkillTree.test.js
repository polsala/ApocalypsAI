import { render, screen, fireEvent } from '@testing-library/react';
import SkillTree from '../src/SkillTree';

// Mock rationale: We use a small, controlled set of skill data for deterministic tests.
// This avoids reliance on external data sources and ensures test consistency.
const mockSkillsData = [
  { id: 'skillA', name: 'Skill A', description: 'Desc A', prerequisites: [], tier: 1, branch: 'Branch1' },
  { id: 'skillB', name: 'Skill B', description: 'Desc B', prerequisites: ['skillA'], tier: 2, branch: 'Branch1' },
  { id: 'skillC', name: 'Skill C', description: 'Desc C', prerequisites: [], tier: 1, branch: 'Branch2' }
];

// Mock the skillsData import
jest.mock('../src/data/skills', () => mockSkillsData);

describe('SkillTree Component', () => {
  beforeEach(() => {
    // Clear any previous learned skills state if component re-renders
    // This is implicitly handled by `render` creating a fresh component instance
  });

  test('renders skill tree title and instruction', () => {
    render(<SkillTree />);
    expect(screen.getByText(/Survival Skill Tree/i)).toBeInTheDocument();
    expect(screen.getByText(/Click on available skills to learn them./i)).toBeInTheDocument();
  });

  test('renders all initial skills', () => {
    render(<SkillTree />);
    expect(screen.getByText('Skill A')).toBeInTheDocument();
    expect(screen.getByText('Skill B')).toBeInTheDocument();
    expect(screen.getByText('Skill C')).toBeInTheDocument();
  });

  test('initially, only skills with no prerequisites are available', () => {
    render(<SkillTree />);
    const skillANode = screen.getByTestId('skill-node-skillA');
    const skillBNode = screen.getByTestId('skill-node-skillB');
    const skillCNode = screen.getByTestId('skill-node-skillC');

    expect(skillANode).toHaveClass('available');
    expect(skillBNode).not.toHaveClass('available'); // Has prereq 'skillA'
    expect(skillCNode).toHaveClass('available');
  });

  test('learning a skill marks it as learned and makes dependent skills available', () => {
    render(<SkillTree />);
    const skillANode = screen.getByTestId('skill-node-skillA');
    const skillBNode = screen.getByTestId('skill-node-skillB');

    // Learn Skill A
    fireEvent.click(skillANode);
    expect(skillANode).toHaveClass('learned');
    expect(skillANode).not.toHaveClass('available'); // Learned skills are not "available" to learn again

    // Skill B should now be available
    expect(skillBNode).toHaveClass('available');
  });

  test('cannot learn a skill if prerequisites are not met', () => {
    render(<SkillTree />);
    const skillBNode = screen.getByTestId('skill-node-skillB');

    // Try to learn Skill B directly (prereq Skill A not learned)
    fireEvent.click(skillBNode);
    expect(skillBNode).not.toHaveClass('learned');
    expect(skillBNode).not.toHaveClass('available'); // Still not available
  });

  test('clicking a learned skill does not change its state', () => {
    render(<SkillTree />);
    const skillANode = screen.getByTestId('skill-node-skillA');

    fireEvent.click(skillANode); // Learn
    expect(skillANode).toHaveClass('learned');

    fireEvent.click(skillANode); // Click again
    expect(skillANode).toHaveClass('learned'); // Should remain learned
  });

  test('skills are grouped by branch and tier', () => {
    render(<SkillTree />);
    expect(screen.getByText('Branch1')).toBeInTheDocument();
    expect(screen.getByText('Branch2')).toBeInTheDocument();
    expect(screen.getAllByText('Tier 1').length).toBeGreaterThanOrEqual(1); // Appears multiple times
    expect(screen.getByText('Tier 2')).toBeInTheDocument();
  });
});
