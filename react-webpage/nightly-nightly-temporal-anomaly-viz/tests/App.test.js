import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: AnomalyDashboard uses mock data internally, so App.js doesn't need further mocking for its children.
// We just need to ensure the main title is rendered.

test('renders Temporal Anomaly Visualizer title', () => {
  render(<App />);
  const linkElement = screen.getByText(/Temporal Anomaly Visualizer/i);
  expect(linkElement).toBeInTheDocument();
});
