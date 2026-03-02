import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: Avoid actual DOM rendering of charts which require canvas
jest.mock('../src/components/AnomalyChart', () => () => <div>AnomalyChartMock</div>);
jest.mock('../src/components/SkillRadar', () => () => <div>SkillRadarMock</div>);
jest.mock('../src/components/ResourceHeatmap', () => () => <div>ResourceHeatmapMock</div>);
jest.mock('../src/components/AffirmationTicker', () => () => <div>AffirmationTickerMock</div>);

test('renders dashboard header', () => {
  render(<App />);
  expect(screen.getByText(/\.VoidWhispers Dashboard/i)).toBeInTheDocument();
});

test('renders all mocked components', () => {
  render(<App />);
  expect(screen.getByText(/AnomalyChartMock/i)).toBeInTheDocument();
  expect(screen.getByText(/SkillRadarMock/i)).toBeInTheDocument();
  expect(screen.getByText(/ResourceHeatmapMock/i)).toBeInTheDocument();
  expect(screen.getByText(/AffirmationTickerMock/i)).toBeInTheDocument();
});
