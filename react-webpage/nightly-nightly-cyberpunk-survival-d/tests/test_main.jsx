import { render, screen, fireEvent } from '@testing-library/react';
import SurvivalDashboard from '../src/main';

// Mock rationale: Deterministic state tests without external dependencies
describe('Survival Dashboard Tests', () => {
  test('Initial state shows correct threat level', () => {
    render(<SurvivalDashboard />);
    expect(screen.getByText('30% 威胁等级')).toBeInTheDocument();
  });

  test('Scavenging increases resources and threat', () => {
    render(<SurvivalDashboard />);
    fireEvent.click(screen.getByText('出发搜寻物资'));
    expect(screen.getByText('水: 110')).toBeInTheDocument();
    expect(screen.getByText('食物: 55')).toBeInTheDocument();
    expect(screen.getByText('威胁等级')).toHaveTextContent('45%');
  });

  test('AI companion reacts to actions', () => {
    render(<SurvivalDashboard />);
    fireEvent.click(screen.getByText('出发搜寻物资'));
    expect(screen.getByText('🎉 发现新资源!')).toBeInTheDocument();
  });
});
