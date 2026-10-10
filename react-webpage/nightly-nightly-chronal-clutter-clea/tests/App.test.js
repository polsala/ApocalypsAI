import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import mockClutter from '../src/mockClutter'; // Mock rationale: Using mock data for deterministic tests.

// Mock rationale: Mocking react-scripts' CSS import behavior
// to prevent errors during Jest tests.
jest.mock('../src/index.css', () => ({}));

describe('App Component', () => {
  test('renders the main heading', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Chronal Clutter Cleaner/i)).toBeInTheDocument();
  });

  test('renders all clutter items by default', () => {
    render(<App />);
    // Check if all mock items are rendered
    mockClutter.forEach(item => {
      expect(screen.getByText(item.name)).toBeInTheDocument();
    });
    expect(screen.getAllByText(/Temporal Weight:/).length).toBe(mockClutter.length);
  });

  test('filters clutter items by type', () => {
    render(<App />);
    const filterSelect = screen.getByLabelText(/Filter by Type:/i);

    fireEvent.change(filterSelect, { target: { value: 'Branch' } });

    // Expect only 'Branch' items to be visible
    const branchItems = mockClutter.filter(item => item.type === 'Branch');
    branchItems.forEach(item => {
      expect(screen.getByText(item.name)).toBeInTheDocument();
    });

    const nonBranchItems = mockClutter.filter(item => item.type !== 'Branch');
    nonBranchItems.forEach(item => {
      expect(screen.queryByText(item.name)).not.toBeInTheDocument();
    });
  });

  test('sorts clutter items by temporal weight (oldest first)', () => {
    render(<App />);
    const sortSelect = screen.getByLabelText(/Sort by:/i);

    fireEvent.change(sortSelect, { target: { value: 'temporalWeightDesc' } });

    const items = screen.getAllByText(/Temporal Weight:/i).map(el => el.parentElement.querySelector('div:first-child').textContent);
    const expectedOrder = mockClutter
      .sort((a, b) => b.temporalWeight - a.temporalWeight)
      .map(item => item.name);

    // Check if the displayed order matches the expected sorted order
    expect(items).toEqual(expectedOrder);
  });

  test('sorts clutter items by name (A-Z)', () => {
    render(<App />);
    const sortSelect = screen.getByLabelText(/Sort by:/i);

    fireEvent.change(sortSelect, { target: { value: 'nameAsc' } });

    const items = screen.getAllByText(/Temporal Weight:/i).map(el => el.parentElement.querySelector('div:first-child').textContent);
    const expectedOrder = mockClutter
      .sort((a, b) => a.name.localeCompare(b.name))
      .map(item => item.name);

    expect(items).toEqual(expectedOrder);
  });

  test('displays "No clutter found" message when no items match filter', () => {
    render(<App />);
    const filterSelect = screen.getByLabelText(/Filter by Type:/i);

    fireEvent.change(filterSelect, { target: { value: 'NonExistentType' } }); // Filter by a type that doesn't exist

    expect(screen.getByText(/No chronal clutter found matching your criteria./i)).toBeInTheDocument();
  });
});
