import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';
import { mockDailyDust } from '../src/data/mockData'; // Import mock data

// Mock rationale: The mockDailyDust is imported directly, ensuring tests are deterministic and offline.
// No actual network requests are made, and the data is consistent across test runs.

describe('App Component', () => {
  test('renders the main dashboard title', () => {
    render(<App />);
    expect(screen.getByText(/ApocalypsAI Cosmic Dust Collector Dashboard/i)).toBeInTheDocument();
  });

  test('renders metric cards with initial data (last 7 days)', () => {
    render(<App />);
    expect(screen.getByText(/Total Stars Collected/i)).toBeInTheDocument();
    expect(screen.getByText(/Total Commits Pushed/i)).toBeInTheDocument();
    expect(screen.getByText(/Total Issues Resolved/i)).toBeInTheDocument();

    const today = new Date();
    const cutoffDate = new Date();
    cutoffDate.setDate(today.getDate() - 7);

    const sevenDayData = mockDailyDust.filter(item => {
      const itemDate = new Date(item.date);
      return itemDate >= cutoffDate;
    });

    const expectedStars = sevenDayData.reduce((sum, item) => sum + item.stars, 0);
    const expectedCommits = sevenDayData.reduce((sum, item) => sum + item.commits, 0);
    const expectedIssues = sevenDayData.reduce((sum, item) => sum + item.issues, 0);

    expect(screen.getByText(expectedStars.toString())).toBeInTheDocument();
    expect(screen.getByText(expectedCommits.toString())).toBeInTheDocument();
    expect(screen.getByText(expectedIssues.toString())).toBeInTheDocument();
  });

  test('switches to 30-day view when "Last 30 Days" button is clicked', () => {
    render(<App />);
    
    const thirtyDaysButton = screen.getByRole('button', { name: /Last 30 Days/i });
    fireEvent.click(thirtyDaysButton);

    expect(thirtyDaysButton).toHaveClass('active');
    expect(screen.getByRole('button', { name: /Last 7 Days/i })).not.toHaveClass('active');

    const today = new Date();
    const cutoffDate = new Date();
    cutoffDate.setDate(today.getDate() - 30);

    const thirtyDayData = mockDailyDust.filter(item => {
      const itemDate = new Date(item.date);
      return itemDate >= cutoffDate;
    });

    const expectedStars = thirtyDayData.reduce((sum, item) => sum + item.stars, 0);
    const expectedCommits = thirtyDayData.reduce((sum, item) => sum + item.commits, 0);
    const expectedIssues = thirtyDayData.reduce((sum, item) => sum + item.issues, 0);

    expect(screen.getByText(expectedStars.toString())).toBeInTheDocument();
    expect(screen.getByText(expectedCommits.toString())).toBeInTheDocument();
    expect(screen.getByText(expectedIssues.toString())).toBeInTheDocument();
  });

  test('displays daily dust collection chart bars for 7 days by default', () => {
    render(<App />);
    const chartBars = screen.getAllByTitle(/Total Dust:/i);
    expect(chartBars.length).toBe(7); // Default is 7 days
  });

  test('displays daily dust collection chart bars for 30 days when selected', () => {
    render(<App />);
    const thirtyDaysButton = screen.getByRole('button', { name: /Last 30 Days/i });
    fireEvent.click(thirtyDaysButton);

    const chartBars = screen.getAllByTitle(/Total Dust:/i);
    expect(chartBars.length).toBe(30); // Should be 30 days after clicking the button
  });

  test('displays top dust collectors (agents)', () => {
    render(<App />);
    expect(screen.getByText(/Top Dust Collectors \(Agents\)/i)).toBeInTheDocument();
    expect(screen.getByText(/Agent Integrator/i)).toBeInTheDocument();
    expect(screen.getByText(/Agent Builder/i)).toBeInTheDocument();
  });
});
