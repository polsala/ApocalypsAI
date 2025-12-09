import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';
import * as WhimsyGenerator from '../src/WhimsyGenerator'; // Import the module

// Mock rationale: We need to ensure deterministic test results for the random forecast generation.
// By mocking the generateWhimsyForecast function, we can control its output and verify
// that the App component correctly displays and updates the forecast based on this controlled output.
jest.mock('../src/WhimsyGenerator', () => ({
  generateWhimsyForecast: jest.fn(),
}));

describe('App', () => {
  beforeEach(() => {
    // Reset the mock before each test
    WhimsyGenerator.generateWhimsyForecast.mockClear();
  });

  test('renders initial forecast on load', async () => {
    const mockForecast = {
      weather: 'Mock Weather',
      resources: 'Mock Resources',
      mood: 'Mock Mood',
      timestamp: '12:00:00 PM'
    };
    WhimsyGenerator.generateWhimsyForecast.mockReturnValue(mockForecast);

    render(<App />);

    expect(screen.getByText(/Nightly Wasteland Whimsy Weaver/i)).toBeInTheDocument();
    expect(screen.getByText(/Today's Whimsy Forecast/i)).toBeInTheDocument();
    expect(screen.getByText(`Weather: ${mockForecast.weather}`)).toBeInTheDocument();
    expect(screen.getByText(`Resources: ${mockForecast.resources}`)).toBeInTheDocument();
    expect(screen.getByText(`Wasteland Mood: ${mockForecast.mood}`)).toBeInTheDocument();
    expect(screen.getByText(`Last updated: ${mockForecast.timestamp}`)).toBeInTheDocument();
    expect(WhimsyGenerator.generateWhimsyForecast).toHaveBeenCalledTimes(1);
  });

  test('updates forecast when "Reroll Whimsy" button is clicked', async () => {
    const initialForecast = {
      weather: 'Initial Weather',
      resources: 'Initial Resources',
      mood: 'Initial Mood',
      timestamp: '1:00:00 PM'
    };
    const newForecast = {
      weather: 'New Weather',
      resources: 'New Resources',
      mood: 'New Mood',
      timestamp: '2:00:00 PM'
    };

    // First call returns initial, second call returns new
    WhimsyGenerator.generateWhimsyForecast
      .mockReturnValueOnce(initialForecast)
      .mockReturnValueOnce(newForecast);

    render(<App />);

    // Check initial forecast
    expect(screen.getByText(`Weather: ${initialForecast.weather}`)).toBeInTheDocument();
    expect(screen.queryByText(`Weather: ${newForecast.weather}`)).not.toBeInTheDocument();

    // Click the reroll button
    const rerollButton = screen.getByRole('button', { name: /Reroll Whimsy/i });
    fireEvent.click(rerollButton);

    // Check if forecast updated
    expect(screen.getByText(`Weather: ${newForecast.weather}`)).toBeInTheDocument();
    expect(screen.queryByText(`Weather: ${initialForecast.weather}`)).not.toBeInTheDocument();
    expect(WhimsyGenerator.generateWhimsyForecast).toHaveBeenCalledTimes(2); // Initial + Reroll
  });

  test('displays loading message initially', () => {
    // Ensure the mock doesn't return a value immediately to simulate loading
    WhimsyGenerator.generateWhimsyForecast.mockReturnValue(null); // Or a promise that resolves later

    render(<App />);
    expect(screen.getByText(/Loading Whimsy.../i)).toBeInTheDocument();
  });
});
