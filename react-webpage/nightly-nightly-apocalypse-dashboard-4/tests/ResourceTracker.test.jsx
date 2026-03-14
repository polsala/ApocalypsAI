import React from 'react';
import { render, screen } from '@testing-library/react';
import ResourceTracker from '../src/components/ResourceTracker';

describe('ResourceTracker Component', () => {
  const mockResources = {
    cannedGoods: 750,
    cleanWater: 300,
    fuel: 150,
  };

  test('renders resource names and values', () => {
    render(<ResourceTracker resources={mockResources} />);
    expect(screen.getByText(/Canned Goods/i)).toBeInTheDocument();
    expect(screen.getByText(/750 units/i)).toBeInTheDocument();
    expect(screen.getByText(/Clean Water/i)).toBeInTheDocument();
    expect(screen.getByText(/300 units/i)).toBeInTheDocument();
    expect(screen.getByText(/Fuel/i)).toBeInTheDocument();
    expect(screen.getByText(/150 units/i)).toBeInTheDocument();
  });

  test('renders progress bars with correct widths', () => {
    render(<ResourceTracker resources={mockResources} />);
    const cannedGoodsBar = screen.getByText(/Canned Goods/i).closest('div').querySelector('.bg-yellow-500');
    expect(cannedGoodsBar).toHaveStyle('width: 75%'); // 750/1000 * 100

    const cleanWaterBar = screen.getByText(/Clean Water/i).closest('div').querySelector('.bg-blue-500');
    expect(cleanWaterBar).toHaveStyle('width: 60%'); // 300/500 * 100

    const fuelBar = screen.getByText(/Fuel/i).closest('div').querySelector('.bg-red-500');
    expect(fuelBar).toHaveStyle('width: 75%'); // 150/200 * 100
  });

  test('handles resources exceeding max values gracefully', () => {
    const excessiveResources = {
      cannedGoods: 1200,
      cleanWater: 600,
      fuel: 250,
    };
    render(<ResourceTracker resources={excessiveResources} />);

    const cannedGoodsBar = screen.getByText(/Canned Goods/i).closest('div').querySelector('.bg-yellow-500');
    expect(cannedGoodsBar).toHaveStyle('width: 100%'); // Capped at 100%

    const cleanWaterBar = screen.getByText(/Clean Water/i).closest('div').querySelector('.bg-blue-500');
    expect(cleanWaterBar).toHaveStyle('width: 100%'); // Capped at 100%

    const fuelBar = screen.getByText(/Fuel/i).closest('div').querySelector('.bg-red-500');
    expect(fuelBar).toHaveStyle('width: 100%'); // Capped at 100%
  });

  test('renders with zero resources', () => {
    const zeroResources = {
      cannedGoods: 0,
      cleanWater: 0,
      fuel: 0,
    };
    render(<ResourceTracker resources={zeroResources} />);

    const cannedGoodsBar = screen.getByText(/Canned Goods/i).closest('div').querySelector('.bg-yellow-500');
    expect(cannedGoodsBar).toHaveStyle('width: 0%');

    const cleanWaterBar = screen.getByText(/Clean Water/i).closest('div').querySelector('.bg-blue-500');
    expect(cleanWaterBar).toHaveStyle('width: 0%');

    const fuelBar = screen.getByText(/Fuel/i).closest('div').querySelector('.bg-red-500');
    expect(fuelBar).toHaveStyle('width: 0%');
  });
});
