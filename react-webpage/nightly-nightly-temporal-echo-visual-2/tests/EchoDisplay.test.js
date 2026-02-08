import { render, screen } from '@testing-library/react';
import EchoDisplay from '../src/EchoDisplay';

// Mock rationale: EchoDisplay is a presentational component. We test that it renders
// the provided text and applies the given inline styles correctly. No external dependencies.

describe('EchoDisplay', () => {
  test('renders text correctly', () => {
    const testText = 'Temporal Ripple';
    render(<EchoDisplay text={testText} style={{}} delay={0} />);
    expect(screen.getByText(testText)).toBeInTheDocument();
  });

  test('applies inline styles correctly', () => {
    const testText = 'Fading Echo';
    const testStyle = { opacity: 0.5, color: 'red', transform: 'translateX(10px)' };
    render(<EchoDisplay text={testText} style={testStyle} delay={0} />);
    const element = screen.getByText(testText);
    expect(element).toHaveStyle('opacity: 0.5');
    expect(element).toHaveStyle('color: red');
    expect(element).toHaveStyle('transform: translateX(10px)');
  });

  test('applies animation delay correctly', () => {
    const testText = 'Delayed Echo';
    const testDelay = 0.5;
    render(<EchoDisplay text={testText} style={{}} delay={testDelay} />);
    const element = screen.getByText(testText);
    expect(element).toHaveStyle(`animation-delay: ${testDelay}s`);
  });

  test('renders empty string without error', () => {
    render(<EchoDisplay text="" style={{}} delay={0} />);
    expect(screen.getByText('')).toBeInTheDocument();
  });
});
