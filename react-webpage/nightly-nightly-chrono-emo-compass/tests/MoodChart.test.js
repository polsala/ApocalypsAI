import { render, screen } from '@testing-library/react';
import MoodChart from '../src/components/MoodChart';
import mockMoodData from '../src/data/mockMoodData'; // # Mock rationale: Directly importing mock data ensures deterministic tests without network calls.

describe('MoodChart Component', () => {
  test('renders the chart title', () => {
    render(<MoodChart data={mockMoodData} />);
    expect(screen.getByText(/Temporal Emotional Flux/i)).toBeInTheDocument();
  });

  test('renders the correct number of mood events', () => {
    render(<MoodChart data={mockMoodData} />);
    const moodEvents = screen.getAllByTitle(/Time: .*Mood: .*Event: .*/);
    expect(moodEvents).toHaveLength(mockMoodData.length);
  });

  test('each mood event displays its score', () => {
    render(<MoodChart data={mockMoodData} />);
    mockMoodData.forEach(event => {
      expect(screen.getByText(event.mood_score.toString())).toBeInTheDocument();
    });
  });

  test('mood events have correct background colors based on score', () => {
    render(<MoodChart data={mockMoodData} />);

    // Helper to get computed style (simplified for direct style check)
    const getComputedBgColor = (score) => {
      if (score >= 5) return 'rgb(76, 175, 80)'; // --color-very-positive
      if (score >= 1) return 'rgb(139, 195, 74)'; // --color-positive
      if (score === 0) return 'rgb(255, 235, 59)'; // --color-neutral
      if (score >= -4) return 'rgb(255, 152, 0)'; // --color-negative
      return 'rgb(244, 67, 54)'; // --color-very-negative
    };

    mockMoodData.forEach(event => {
      const eventElement = screen.getByTitle(new RegExp(`Mood: ${event.mood_score}`));
      // Note: getComputedStyle returns RGB values, so we compare against those.
      // This test is a bit brittle to exact CSS changes, but verifies the logic.
      expect(eventElement).toHaveStyle(`background-color: ${getComputedBgColor(event.mood_score)}`);
    });
  });

  test('renders the mood legend', () => {
    render(<MoodChart data={mockMoodData} />);
    expect(screen.getByText(/Very Positive/i)).toBeInTheDocument();
    expect(screen.getByText(/Positive/i)).toBeInTheDocument();
    expect(screen.getByText(/Neutral/i)).toBeInTheDocument();
    expect(screen.getByText(/Negative/i)).toBeInTheDocument();
    expect(screen.getByText(/Very Negative/i)).toBeInTheDocument();
  });
});
