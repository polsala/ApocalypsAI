import { generateEchoData } from '../src/EchoGenerator';

describe('generateEchoData', () => {
  test('should return an array of 20 echo data points', () => {
    const data = generateEchoData('Test Location', '2023-01-01T12:00');
    expect(data).toHaveLength(20);
  });

  test('should produce deterministic output for the same inputs', () => {
    const data1 = generateEchoData('Same Location', '2023-01-01T10:00');
    const data2 = generateEchoData('Same Location', '2023-01-01T10:00');
    expect(data1).toEqual(data2);
  });

  test('should produce different output for different locations', () => {
    const data1 = generateEchoData('Location A', '2023-01-01T10:00');
    const data2 = generateEchoData('Location B', '2023-01-01T10:00');
    expect(data1).not.toEqual(data2);
  });

  test('should produce different output for different times', () => {
    const data1 = generateEchoData('Test Location', '2023-01-01T10:00');
    const data2 = generateEchoData('Test Location', '2023-01-01T11:00');
    expect(data1).not.toEqual(data2);
  });

  test('each data point should have expected properties', () => {
    const data = generateEchoData('Test Location', '2023-01-01T12:00');
    data.forEach(echo => {
      expect(echo).toHaveProperty('offset');
      expect(typeof echo.offset).toBe('number');

      expect(echo).toHaveProperty('intensity');
      expect(typeof echo.intensity).toBe('number');
      expect(echo.intensity).toBeGreaterThanOrEqual(0.2); // Min intensity from generator logic
      expect(echo.intensity).toBeLessThanOrEqual(1.0); // Max intensity from generator logic

      expect(echo).toHaveProperty('distortionType');
      expect(typeof echo.distortionType).toBe('string');
      const validTypes = ['Chronal Ripple', 'Paradox Pulse', 'Void Whisper'];
      expect(validTypes).toContain(echo.distortionType);
    });
  });

  test('intensity values are correctly formatted to two decimal places', () => {
    const data = generateEchoData('Test Location', '2023-01-01T12:00');
    data.forEach(echo => {
      const decimalPlaces = (echo.intensity.toString().split('.')[1] || '').length;
      expect(decimalPlaces).toBeLessThanOrEqual(2);
    });
  });
});
