import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../src/App';
import * as api from '../src/api';

describe('App', () => {
  // Mock rationale: We mock the `fetchCelestialData` API call to control the data
  // returned to the App component. This allows us to test the App's rendering and
  // state management independently of the actual data calculation logic, ensuring
  // tests are fast, deterministic, and offline.

  const mockCelestialData = {
    positions: [
      { name: 'Solara', angle: 10, color: '#FFD700' },
      { name: 'Lunaris', angle: 180, color: '#C0C0C0' }
    ],
    influences: ['Mock Conjunction: Test influence.']
  };

  beforeEach(() => {
    jest.spyOn(api, 'fetchCelestialData').mockResolvedValue(mockCelestialData);
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('renders the main title and loads data', async () => {
    render(<App />);

    expect(screen.getByText(/Nightly Celestial Alignment Tracker/i)).toBeInTheDocument();
    expect(screen.getByText(/Loading cosmic energies.../i)).toBeInTheDocument();

    await waitFor(() => {
      expect(api.fetchCelestialData).toHaveBeenCalledTimes(1);
      expect(screen.queryByText(/Loading cosmic energies.../i)).not.toBeInTheDocument();
      expect(screen.getByText('S')).toBeInTheDocument(); // Solara initial
      expect(screen.getByText('L')).toBeInTheDocument(); // Lunaris initial
      expect(screen.getByText(/Mock Conjunction/i)).toBeInTheDocument();
    });
  });

  test('changes celestial data when date is changed', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('S')).toBeInTheDocument();
    });

    const datePicker = screen.getByLabelText(/Select Date:/i);
    userEvent.clear(datePicker);
    userEvent.type(datePicker, '2023-05-20');
    userEvent.tab(); // Blur the input to trigger change

    const newMockCelestialData = {
      positions: [
        { name: 'Terra Nova', angle: 50, color: '#00FF7F' }
      ],
      influences: ['New Alignment: Different cosmic vibes.']
    };
    api.fetchCelestialData.mockResolvedValueOnce(newMockCelestialData);

    await waitFor(() => {
      expect(api.fetchCelestialData).toHaveBeenCalledTimes(2); // Initial load + date change
      expect(screen.queryByText('S')).not.toBeInTheDocument(); // Old body gone
      expect(screen.getByText('T')).toBeInTheDocument(); // New body present
      expect(screen.getByText(/New Alignment/i)).toBeInTheDocument();
    });
  });

  test('displays loading messages while fetching data', async () => {
    // Make the mock return a pending promise to simulate loading state
    api.fetchCelestialData.mockReturnValueOnce(new Promise(() => {}));

    render(<App />);

    expect(screen.getByText(/Loading cosmic energies.../i)).toBeInTheDocument();
    expect(screen.getByText(/Calculating influences.../i)).toBeInTheDocument();

    // Restore mock and resolve it to allow cleanup
    api.fetchCelestialData.mockRestore();
    jest.spyOn(api, 'fetchCelestialData').mockResolvedValue(mockCelestialData);
  });
});
