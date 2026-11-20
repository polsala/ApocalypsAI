import { render, screen, fireEvent } from '@testing-library/react';
import Echo from '../src/Echo';

describe('Echo', () => {
  const mockEcho = {
    id: 1,
    x: 10,
    y: 20,
    size: 30,
    harmonized: false,
    temporalSignature: 0.5
  };

  const mockOnClick = jest.fn();

  // Mock rationale: We are testing the Echo component in isolation. The onClick function is an external dependency
  // passed as a prop, so mocking it allows us to verify it's called correctly without needing the full EchoBloom context.

  test('renders an echo with correct styles', () => {
    render(<Echo echo={mockEcho} onClick={mockOnClick} />);
    const echoElement = screen.getByTitle(`Echo #${mockEcho.id}`);
    expect(echoElement).toBeInTheDocument();
    expect(echoElement).toHaveStyle(`left: ${mockEcho.x}px`);
    expect(echoElement).toHaveStyle(`top: ${mockEcho.y}px`);
    expect(echoElement).toHaveStyle(`width: ${mockEcho.size}px`);
    expect(echoElement).toHaveStyle(`height: ${mockEcho.size}px`);
    expect(echoElement).not.toHaveClass('harmonized');
  });

  test('renders a harmonized echo with correct styles', () => {
    const harmonizedEcho = { ...mockEcho, harmonized: true };
    render(<Echo echo={harmonizedEcho} onClick={mockOnClick} />);
    const echoElement = screen.getByTitle(`Harmonized Echo #${harmonizedEcho.id}`);
    expect(echoElement).toBeInTheDocument();
    expect(echoElement).toHaveClass('harmonized');
    // Check for harmonized specific styles (e.g., transform scale)
    expect(echoElement).toHaveStyle('transform: scale(1.2)');
  });

  test('calls onClick handler when clicked', () => {
    render(<Echo echo={mockEcho} onClick={mockOnClick} />);
    const echoElement = screen.getByTitle(`Echo #${mockEcho.id}`);
    fireEvent.click(echoElement);
    expect(mockOnClick).toHaveBeenCalledTimes(1);
    expect(mockOnClick).toHaveBeenCalledWith(mockEcho.id);
  });
});
