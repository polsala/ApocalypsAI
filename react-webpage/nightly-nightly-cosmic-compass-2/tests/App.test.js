import { render, screen } from '@testing-library/react';
import App from '../src/App';

describe('App Component', () => {
  test('renders Nightly Cosmic Compass title', () => {
    render(<App />);
    const titleElement = screen.getByText(/Nightly Cosmic Compass/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders the CosmicCompass component', () => {
    render(<App />);
    // Check for an element that is unique to CosmicCompass, e.g., its button
    const scanButton = screen.getByRole('button', { name: /Scan for Cosmic Alignment/i });
    expect(scanButton).toBeInTheDocument();
  });
});
