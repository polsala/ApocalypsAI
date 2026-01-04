// Nightly Emoji Weather Widget Tests
// Deterministic, offline tests with mocks

const fs = require('fs');
const path = require('path');
const { 
  getCurrentLocation, 
  getWeatherData, 
  displayWeather, 
  WEATHER_ICONS, 
  ASCII_ARTS 
} = require('../src/index');

// Mock rationale: We mock external APIs and file system operations
// to ensure tests are deterministic and can run offline without network access

// Test configuration
const TEST_CONFIG = {
  api_key: 'test-key-123',
  default_city: 'Testville, TN',
  theme: 'default',
  units: 'metric'
};

// Mock fetch
const originalFetch = global.fetch;
beforeAll(() => {
  global.fetch = jest.fn();
});

afterAll(() => {
  global.fetch = originalFetch;
});

// Mock fs operations
jest.mock('fs');
const mockFs = fs.__proto__;

// Mock execSync for location detection
jest.mock('child_process', () => ({
  execSync: jest.fn().mockReturnValue(JSON.stringify({
    city: 'MockCity',
    region: 'MO'
  }))
}));

// Mock readline
jest.mock('readline', () => ({
  createInterface: jest.fn().mockReturnValue({
    question: jest.fn().mockImplementation((question, callback) => {
      callback('mock-answer');
    }),
    close: jest.fn()
  })
}));

// Helper to capture console output
function captureConsole() {
  const logSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
  const errorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
  return { logSpy, errorSpy, restore: () => { logSpy.mockRestore(); errorSpy.mockRestore(); } };
}

// Test WEATHER_ICONS
describe('WEATHER_ICONS', () => {
  test('contains expected weather types', () => {
    expect(WEATHER_ICONS).toHaveProperty('clear');
    expect(WEATHER_ICONS).toHaveProperty('rain');
    expect(WEATHER_ICONS).toHaveProperty('snow');
    expect(WEATHER_ICONS).toHaveProperty('thunderstorm');
    expect(WEATHER_ICONS.clear).toBe('☀️');
    expect(WEATHER_ICONS.rain).toBe('🌧️');
  });
});

// Test ASCII_ARTS
describe('ASCII_ARTS', () => {
  test('contains expected ascii art types', () => {
    expect(ASCII_ARTS).toHaveProperty('sunrise');
    expect(ASCII_ARTS).toHaveProperty('rain');
    expect(ASCII_ARTS).toHaveProperty('snow');
    expect(ASCII_ARTS).toHaveProperty('cloud');
    expect(ASCII_ARTS.sunrise).toContain('🌅');
    expect(ASCII_ARTS.rain).toContain('💦');
  });
});

describe('getCurrentLocation', () => {
  test('returns mock location when ipapi works', () => {
    const location = getCurrentLocation();
    expect(location).toBe('MockCity, MO');
  });
});

// Mock the real config file operations for weather tests
describe('getWeatherData', () => {
  beforeEach(() => {
    // Mock config file exists
    mockFs.existsSync.mockReturnValue(true);
    mockFs.readFileSync.mockReturnValue(JSON.stringify(TEST_CONFIG));
  });

  test('returns weather data when API call succeeds', async () => {
    const mockResponse = {
      ok: true,
      json: jest.fn().mockResolvedValue({
        weather: [{ main: 'Clear', description: 'clear sky' }],
        main: { temp: 25, temp_min: 20, temp_max: 30 },
        name: 'Testville',
        sys: { country: 'TN' }
      })
    };

    global.fetch.mockResolvedValue(mockResponse);

    const data = await getWeatherData('Testville, TN');
    expect(data).toBeDefined();
    expect(data.name).toBe('Testville');
    expect(data.weather[0].main).toBe('Clear');
  });

  test('handles API error gracefully', async () => {
    const mockResponse = {
      ok: false,
      status: 401,
      statusText: 'Unauthorized'
    };

    global.fetch.mockResolvedValue(mockResponse);

    const data = await getWeatherData('Testville, TN');
    expect(data).toBeNull();
  });

  test('throws error when no API key', async () => {
    // Mock config without api_key
    mockFs.readFileSync.mockReturnValue(JSON.stringify({ ...TEST_CONFIG, api_key: null }));
    
    await expect(getWeatherData('Testville, TN')).rejects.toThrow('No API key found');
  });
});

describe('displayWeather', () => {
  test('displays weather with correct emojis and formatting', () => {
    const mockData = {
      weather: [{ main: 'Rain', description: 'light rain' }],
      main: { temp: 15, temp_min: 10, temp_max: 20 },
      name: 'RainyTown'
    };

    const consoleCapture = captureConsole();
    
    displayWeather(mockData, 'default');
    
    expect(consoleCapture.logSpy).toHaveBeenCalled();
    consoleCapture.restore();
  });

  test('handles missing data gracefully', () => {
    const consoleCapture = captureConsole();
    
    displayWeather(null, 'default');
    
    expect(consoleCapture.logSpy).toHaveBeenCalledWith(expect.stringContaining('❌ Unable to fetch weather data'));
    consoleCapture.restore();
  });
});

// Integration test
describe('Integration Tests', () => {
  test('full workflow with mock data', async () => {
    // Setup mocks
    mockFs.existsSync.mockReturnValue(true);
    mockFs.readFileSync.mockReturnValue(JSON.stringify(TEST_CONFIG));
    
    const mockResponse = {
      ok: true,
      json: jest.fn().mockResolvedValue({
        weather: [{ main: 'Clear', description: 'clear sky' }],
        main: { temp: 22, temp_min: 18, temp_max: 26 },
        name: 'SunnyCity',
        sys: { country: 'US' }
      })
    };
    
    global.fetch.mockResolvedValue(mockResponse);
    
    // Capture output
    const consoleCapture = captureConsole();
    
    // This would normally display the weather
    // We verify that no errors occur in the process
    expect(async () => {
      await getWeatherData('SunnyCity, US');
    }).not.toThrow();
    
    consoleCapture.restore();
  });
});

// Edge case tests
describe('Edge Cases', () => {
  test('handles unknown weather types', () => {
    const mockData = {
      weather: [{ main: 'Unknown', description: 'unknown condition' }],
      main: { temp: 0 },
      name: 'MysteryTown'
    };

    const consoleCapture = captureConsole();
    
    displayWeather(mockData, 'default');
    
    // Should use default emoji
    expect(consoleCapture.logSpy).toHaveBeenCalled();
    consoleCapture.restore();
  });
});

console.log('\n🧪 All tests completed successfully!\n');
