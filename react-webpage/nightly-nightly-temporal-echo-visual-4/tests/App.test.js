import { render, screen } from '@testing-library/react';
import App from '../src/App';

describe('App', () => {
  test('renders the main heading', () => {
    // # Mock rationale: No external dependencies, just rendering a static title.
    render(<App />);
    const headingElement = screen.getByText(/Nightly Temporal Echo Visualizer/i);
    expect(headingElement).toBeInTheDocument();
  });

  test('renders the TemporalEchoChamber component', () => {
    // # Mock rationale: Verifies that the child component is rendered.
    // We don't need to test its internal logic here, just its presence.
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter a concept/i);
    expect(inputElement).toBeInTheDocument();
    const buttonElement = screen.getByRole('button', { name: /Generate Echoes/i });
    expect(buttonElement).toBeInTheDocument();
  });
});
