import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: EchoBloom contains complex animation and state logic that is better tested in its own component.
// For App.js, we only need to ensure its basic structure and text content are rendered.
jest.mock('../src/EchoBloom', () => {
  return function MockEchoBloom() {
    return <div data-testid="echo-bloom-mock"></div>;
  };
});

describe('App', () => {
  test('renders the main title and instructions', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Bloom/i)).toBeInTheDocument();
    expect(screen.getByText(/Click on the echoes to harmonize their temporal frequencies./i)).toBeInTheDocument();
  });

  test('renders the EchoBloom component', () => {
    render(<App />);
    expect(screen.getByTestId('echo-bloom-mock')).toBeInTheDocument();
  });
});
