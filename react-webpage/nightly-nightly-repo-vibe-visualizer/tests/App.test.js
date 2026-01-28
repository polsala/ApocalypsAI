import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import App from '../src/App';
import * as VibeAnalyzer from '../src/VibeAnalyzer';

// # Mock rationale: The App component relies on `analyzeVibe` and a simulated async data fetch.
// # We mock `analyzeVibe` to control its output deterministically for testing specific scenarios.
// # The `setTimeout` in `App.js` is implicitly handled by `waitFor` in React Testing Library,
// # allowing us to test the asynchronous rendering flow without actual network requests.

describe('App', () => {
  beforeEach(() => {
    // Mock the analyzeVibe function to return a predictable result
    jest.spyOn(VibeAnalyzer, 'analyzeVibe').mockReturnValue('Optimistic');
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('renders loading state initially', () => {
    render(<App />);
    expect(screen.getByText(/Calculating the repo's vibe.../i)).toBeInTheDocument();
  });

  test('renders the VibeVisualizer with the calculated vibe after loading', async () => {
    render(<App />);

    // Wait for the simulated data fetching to complete
    await waitFor(() => {
      expect(screen.getByText(/Optimistic/i)).toBeInTheDocument();
    }, { timeout: 2000 }); // Increase timeout if 1s delay in App.js is too short for test runner

    expect(screen.getByText(/The repository is buzzing with new features and improvements!/i)).toBeInTheDocument();
    expect(screen.getByText(/Based on recent contributions \(mocked data\)./i)).toBeInTheDocument();
  });

  test('VibeAnalyzer is called with mock data', async () => {
    render(<App />);
    await waitFor(() => {
      expect(VibeAnalyzer.analyzeVibe).toHaveBeenCalledTimes(1);
      // Verify it's called with the mock data defined in App.js
      expect(VibeAnalyzer.analyzeVibe).toHaveBeenCalledWith([
        "feat: implement new user profile page",
        "fix(auth): resolve login redirect bug",
        "docs: update API documentation for v2",
        "chore: upgrade dependencies to latest versions",
        "refactor: simplify data fetching logic in components",
        "urgent: hotfix for critical security vulnerability",
        "style: consistent button styling across app",
        "add: new feature flag for experimental UI",
        "update: build process configuration",
        "tweak: animation speed on modal close"
      ]);
    }, { timeout: 2000 });
  });

  test('renders default Mysterious vibe description if VibeAnalyzer returns unexpected value', async () => {
    VibeAnalyzer.analyzeVibe.mockReturnValue('UnknownVibe'); // Mock an unexpected return
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/UnknownVibe/i)).toBeInTheDocument(); // It will still display the text
      expect(screen.getByText(/A mix of minor updates and tweaks. The path forward is unclear.../i)).toBeInTheDocument(); // But the description falls back to Mysterious
    }, { timeout: 2000 });
  });
});
