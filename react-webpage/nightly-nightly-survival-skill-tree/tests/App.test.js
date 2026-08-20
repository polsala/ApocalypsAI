import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// # Mock rationale: localStorage is a browser API and needs to be mocked for Node.js test environment.
// We mock it to ensure tests are deterministic and don't rely on actual browser storage.
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('App Component', () => {
  beforeEach(() => {
    localStorageMock.getItem.mockReturnValue(null); // Reset localStorage for each test
    localStorageMock.setItem.mockClear();
  });

  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/ApocalypsAI Survival Skill Tree/i)).toBeInTheDocument();
  });

  test('displays initial skills', () => {
    render(<App />);
    expect(screen.getByText('Scavenging Basics')).toBeInTheDocument();
    expect(screen.getByText('Wilderness Survival')).toBeInTheDocument();
    expect(screen.getByText('Basic First Aid')).toBeInTheDocument();
  });

  test('unlocks a skill without prerequisites when clicked', () => {
    render(<App />);
    const scavengingButton = screen.getByRole('button', { name: 'Unlock' }); // Finds the first 'Unlock' button
    fireEvent.click(scavengingButton);
    expect(screen.getByRole('button', { name: 'Mastered!' })).toBeInTheDocument();
    expect(localStorageMock.setItem).toHaveBeenCalledTimes(1);
    expect(JSON.parse(localStorageMock.setItem.mock.calls[0][1])[0].unlocked).toBe(true);
  });

  test('prevents unlocking a skill with unmet prerequisites', () => {
    render(<App />);
    // Urban Foraging requires Scavenging Basics
    const urbanForagingButton = screen.getByRole('button', { name: 'Locked' }); 
    expect(urbanForagingButton).toBeDisabled();
    fireEvent.click(urbanForagingButton); // Click disabled button
    expect(urbanForagingButton).toBeDisabled(); // Should remain disabled
    expect(localStorageMock.setItem).not.toHaveBeenCalled(); // No state change
  });

  test('unlocks a skill after its prerequisites are met', () => {
    render(<App />);

    // Unlock Scavenging Basics (prerequisite for Urban Foraging)
    const scavengingButton = screen.getByRole('button', { name: 'Unlock' });
    fireEvent.click(scavengingButton);
    expect(screen.getByRole('button', { name: 'Mastered!' })).toBeInTheDocument();

    // Now Urban Foraging should be unlockable
    const urbanForagingButton = screen.getByRole('button', { name: 'Unlock' }); // Should now be 'Unlock'
    expect(urbanForagingButton).toBeEnabled();
    fireEvent.click(urbanForagingButton);
    expect(screen.getByRole('button', { name: 'Mastered!' })).toBeInTheDocument();
    expect(localStorageMock.setItem).toHaveBeenCalledTimes(2); // Two state updates
  });

  test('allows locking an already mastered skill', () => {
    render(<App />);

    // Unlock Scavenging Basics
    const scavengingButton = screen.getByRole('button', { name: 'Unlock' });
    fireEvent.click(scavengingButton);
    expect(screen.getByRole('button', { name: 'Mastered!' })).toBeInTheDocument();

    // Lock Scavenging Basics again
    const masteredScavengingButton = screen.getByRole('button', { name: 'Mastered!' });
    fireEvent.click(masteredScavengingButton);
    expect(screen.getByRole('button', { name: 'Unlock' })).toBeInTheDocument(); // Should revert to 'Unlock'
    expect(localStorageMock.setItem).toHaveBeenCalledTimes(2);
  });

  test('loading skills from localStorage', () => {
    // # Mock rationale: Simulating a previous session where 'Scavenging Basics' was unlocked.
    localStorageMock.getItem.mockReturnValue(JSON.stringify([
      { id: 'scavenging', name: 'Scavenging Basics', description: 'Learn to find useful items in abandoned places.', prerequisites: [], unlocked: true, level: 0 },
      { id: 'urban-foraging', name: 'Urban Foraging', description: 'Identify edible plants and discarded food in city ruins.', prerequisites: ['scavenging'], unlocked: false, level: 1 },
      { id: 'wilderness-survival', name: 'Wilderness Survival', description: 'Basic outdoor survival skills: shelter, fire, water.', prerequisites: [], unlocked: false, level: 0 },
      { id: 'basic-first-aid', name: 'Basic First Aid', description: 'Treat minor injuries and stabilize wounds.', prerequisites: [], unlocked: false, level: 0 },
      { id: 'advanced-first-aid', name: 'Advanced First Aid', description: 'Handle severe trauma and medical emergencies.', prerequisites: ['basic-first-aid'], unlocked: false, level: 1 },
      { id: 'makeshift-crafting', name: 'Makeshift Crafting', description: 'Turn junk into useful tools and repairs.', prerequisites: ['scavenging'], unlocked: false, level: 1 },
      { id: 'radio-repair', name: 'Radio Repair', description: 'Fix broken radios to communicate across the wasteland.', prerequisites: ['makeshift-crafting'], unlocked: false, level: 2 },
      { id: 'wasteland-diplomacy', name: 'Wasteland Diplomacy', description: 'Negotiate with other survivors and factions.', prerequisites: [], unlocked: false, level: 0 },
      { id: 'bartering-basics', name: 'Bartering Basics', description: 'Master the art of trade in a resource-scarce world.', prerequisites: ['wasteland-diplomacy'], unlocked: false, level: 1 }
    ]));

    render(<App />);
    expect(screen.getByRole('button', { name: 'Mastered!' })).toBeInTheDocument(); // Scavenging should be mastered
    expect(screen.getByRole('button', { name: 'Unlock' })).toBeInTheDocument(); // Urban Foraging should be unlockable
  });
});
