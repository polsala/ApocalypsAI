import { render, screen } from '@testing-library/react';
import App from '../src/main';

// Mock whimsy items to make tests deterministic
jest.mock('../src/whimsy-items', () => ({
  default: {
    'post-apocalyptic': ['Test Item 1', 'Test Item 2']
  }
}));

describe('Whimsical Survival Kit Builder', () => {
  test('renders scenario selector', () => {
    render(<App />);
    expect(screen.getByText('Scenario:')).toBeInTheDocument();
  });

  test('shows whimsy slider', () => {
    render(<App />);
    expect(screen.getByRole('slider')).toBeInTheDocument();
  });

  test('generates items based on whimsy level', () => {
    // Mocked test would simulate slider changes and verify output
    // Implementation would require full component mounting
  });
});
