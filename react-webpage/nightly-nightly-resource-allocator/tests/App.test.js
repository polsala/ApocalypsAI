import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: React Testing Library is designed to test components as users would interact with them.
// We simulate user input and clicks, and assert on the rendered output. No external API calls or complex
// side effects are involved, so direct interaction simulation is sufficient and deterministic.

describe('App Component', () => {
  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Resource Allocator/i)).toBeInTheDocument();
  });

  test('initial state inputs are rendered correctly', () => {
    render(<App />);
    expect(screen.getByLabelText(/Food Rations:/i)).toHaveValue(100);
    expect(screen.getByLabelText(/Water Units:/i)).toHaveValue(150);
    expect(screen.getByLabelText(/Medical Kits:/i)).toHaveValue(20);
    expect(screen.getByLabelText(/Number of Survivors:/i)).toHaveValue(10);
  });

  test('updates input values on change', () => {
    render(<App />);
    const foodInput = screen.getByLabelText(/Food Rations:/i);
    fireEvent.change(foodInput, { target: { value: '200' } });
    expect(foodInput).toHaveValue(200);
  });

  test('calculates allocation and displays results for sufficient resources (High Morale)', () => {
    render(<App />);

    // Set inputs to ensure high morale
    fireEvent.change(screen.getByLabelText(/Food Rations:/i), { target: { value: '200' } }); // Needs 20
    fireEvent.change(screen.getByLabelText(/Water Units:/i), { target: { value: '300' } }); // Needs 30
    fireEvent.change(screen.getByLabelText(/Medical Kits:/i), { target: { value: '10' } }); // Needs 5
    fireEvent.change(screen.getByLabelText(/Number of Survivors:/i), { target: { value: '10' } });

    fireEvent.click(screen.getByText(/Calculate Allocation/i));

    expect(screen.getByText(/Allocation Report/i)).toBeInTheDocument();
    expect(screen.getByText(/Food: 20 \/ 20 rations allocated/i)).toBeInTheDocument();
    expect(screen.getByText(/Water: 30 \/ 30 units allocated/i)).toBeInTheDocument();
    expect(screen.getByText(/Medical Kits: 5 \/ 5 kits allocated/i)).toBeInTheDocument();
    expect(screen.getByText(/Community Morale: 😊 High/i)).toBeInTheDocument();
    expect(screen.getByText(/Next Scavenging Success Chance: High \(80% chance of finding something useful!\)/i)).toBeInTheDocument();
  });

  test('calculates allocation and displays results for some unmet needs (Medium Morale)', () => {
    render(<App />);

    // Set inputs to ensure medium morale (e.g., low food)
    fireEvent.change(screen.getByLabelText(/Food Rations:/i), { target: { value: '10' } }); // Needs 20
    fireEvent.change(screen.getByLabelText(/Water Units:/i), { target: { value: '300' } }); // Needs 30
    fireEvent.change(screen.getByLabelText(/Medical Kits:/i), { target: { value: '10' } }); // Needs 5
    fireEvent.change(screen.getByLabelText(/Number of Survivors:/i), { target: { value: '10' } });

    fireEvent.click(screen.getByText(/Calculate Allocation/i));

    expect(screen.getByText(/Allocation Report/i)).toBeInTheDocument();
    expect(screen.getByText(/Food: 10 \/ 20 rations allocated/i)).toBeInTheDocument();
    expect(screen.getByText(/Water: 30 \/ 30 units allocated/i)).toBeInTheDocument();
    expect(screen.getByText(/Medical Kits: 5 \/ 5 kits allocated/i)).toBeInTheDocument();
    expect(screen.getByText(/Community Morale: 😐 Medium/i)).toBeInTheDocument();
    expect(screen.getByText(/Next Scavenging Success Chance: Moderate \(50% chance, but beware of raiders!\)/i)).toBeInTheDocument();
  });

  test('calculates allocation and displays results for significant unmet needs (Low Morale)', () => {
    render(<App />);

    // Set inputs to ensure low morale (e.g., low food and water)
    fireEvent.change(screen.getByLabelText(/Food Rations:/i), { target: { value: '5' } }); // Needs 20
    fireEvent.change(screen.getByLabelText(/Water Units:/i), { target: { value: '10' } }); // Needs 30
    fireEvent.change(screen.getByLabelText(/Medical Kits:/i), { target: { value: '10' } }); // Needs 5
    fireEvent.change(screen.getByLabelText(/Number of Survivors:/i), { target: { value: '10' } });

    fireEvent.click(screen.getByText(/Calculate Allocation/i));

    expect(screen.getByText(/Allocation Report/i)).toBeInTheDocument();
    expect(screen.getByText(/Food: 5 \/ 20 rations allocated/i)).toBeInTheDocument();
    expect(screen.getByText(/Water: 10 \/ 30 units allocated/i)).toBeInTheDocument();
    expect(screen.getByText(/Medical Kits: 5 \/ 5 kits allocated/i)).toBeInTheDocument();
    expect(screen.getByText(/Community Morale: 😟 Low/i)).toBeInTheDocument();
    expect(screen.getByText(/Next Scavenging Success Chance: Low \(20% chance, better stay put or risk it all!\)/i)).toBeInTheDocument();
  });

  test('displays error message if survivors is 0', () => {
    render(<App />);
    fireEvent.change(screen.getByLabelText(/Number of Survivors:/i), { target: { value: '0' } });
    fireEvent.click(screen.getByText(/Calculate Allocation/i));
    expect(screen.getByText(/Number of survivors must be greater than 0./i)).toBeInTheDocument();
  });
});
