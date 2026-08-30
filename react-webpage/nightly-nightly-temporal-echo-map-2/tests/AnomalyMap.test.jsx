import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import AnomalyMap from '../src/components/AnomalyMap';

describe('AnomalyMap', () => {
  const gridSize = 3; // Use a smaller grid for easier testing

  // Mock rationale: We are testing the rendering logic of the AnomalyMap component.
  // Using mock data ensures deterministic test results without relying on external
  // data sources or complex state management.
  const mockAnomalies = [
    { id: 'a1', x: 0, y: 0, intensity: 50, type: 'minor-echo' },
    { id: 'a2', x: 1, y: 1, intensity: 100, type: 'major-distortion' },
    { id: 'a3', x: 0, y: 0, intensity: 30, type: 'minor-echo' }, // Overlapping
    { id: 'a4', x: 2, y: 2, intensity: 10, type: 'chronal-flux' },
  ];

  it('renders the correct number of grid cells', () => {
    render(<AnomalyMap anomalies={[]} gridSize={gridSize} />);
    const cells = screen.getAllByTitle(/Cell/);
    expect(cells).toHaveLength(gridSize * gridSize); // 3x3 = 9 cells
  });

  it('applies correct background color based on anomaly intensity', () => {
    render(<AnomalyMap anomalies={mockAnomalies} gridSize={gridSize} />);

    // Cell (0,0) has two anomalies: 50 + 30 = 80 intensity
    // In AnomalyMap.jsx color calculation:
    // cappedIntensity = min(80, 255) = 80
    // red = min(255, 80 * 2) = 160
    // green = max(0, 255 - 80 * 2) = 95
    const cell00 = screen.getByTitle('Cell (0,0) - Intensity: 80.00');
    expect(cell00).toHaveStyle('background-color: rgb(160, 95, 0)');

    // Cell (1,1) has one anomaly: 100 intensity
    // cappedIntensity = min(100, 255) = 100
    // red = min(255, 100 * 2) = 200
    // green = max(0, 255 - 100 * 2) = 55
    const cell11 = screen.getByTitle('Cell (1,1) - Intensity: 100.00');
    expect(cell11).toHaveStyle('background-color: rgb(200, 55, 0)');

    // Cell (2,2) has one anomaly: 10 intensity
    // cappedIntensity = min(10, 255) = 10
    // red = min(255, 10 * 2) = 20
    // green = max(0, 255 - 10 * 2) = 235
    const cell22 = screen.getByTitle('Cell (2,2) - Intensity: 10.00');
    expect(cell22).toHaveStyle('background-color: rgb(20, 235, 0)');

    // A cell with no anomalies should have 0 intensity
    // cappedIntensity = min(0, 255) = 0
    // red = min(255, 0 * 2) = 0
    // green = max(0, 255 - 0 * 2) = 255
    const cell01 = screen.getByTitle('Cell (0,1) - Intensity: 0.00');
    expect(cell01).toHaveStyle('background-color: rgb(0, 255, 0)');
  });

  it('caps intensity at 255 for color calculation', () => {
    const highIntensityAnomalies = [
      { id: 'h1', x: 0, y: 0, intensity: 200, type: 'super-rift' },
      { id: 'h2', x: 0, y: 0, intensity: 100, type: 'super-rift' }, // Total 300
    ];
    render(<AnomalyMap anomalies={highIntensityAnomalies} gridSize={gridSize} />);
    // rawIntensity = 300
    // cappedIntensity = min(300, 255) = 255
    // red = min(255, 255 * 2) = 255
    // green = max(0, 255 - 255 * 2) = 0
    const cell00 = screen.getByTitle('Cell (0,0) - Intensity: 300.00'); // Title shows actual sum
    expect(cell00).toHaveStyle('background-color: rgb(255, 0, 0)'); // Should be pure red
  });
});
