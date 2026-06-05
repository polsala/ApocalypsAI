import { loadAnomalies, saveAnomalies } from '../src/data/localStorageService';

// Mock rationale: localStorage is a browser-specific API and not available in a Node.js test environment.
// Mocking it allows for deterministic, offline testing of the utility functions without a real browser.
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: jest.fn((key) => store[key] || null),
    setItem: jest.fn((key, value) => {
      store[key] = value.toString();
    }),
    clear: jest.fn(() => {
      store = {};
    }),
    removeItem: jest.fn((key) => {
      delete store[key];
    }),
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('localStorageService', () => {
  beforeEach(() => {
    localStorageMock.clear();
    localStorageMock.getItem.mockClear();
    localStorageMock.setItem.mockClear();
  });

  it('should load empty array if no anomalies are in local storage', () => {
    expect(loadAnomalies()).toEqual([]);
    expect(localStorageMock.getItem).toHaveBeenCalledWith('temporalAnomalies');
  });

  it('should load existing anomalies from local storage', () => {
    const mockAnomalies = [{ id: 1, description: 'test' }];
    localStorageMock.setItem('temporalAnomalies', JSON.stringify(mockAnomalies));
    expect(loadAnomalies()).toEqual(mockAnomalies);
    expect(localStorageMock.getItem).toHaveBeenCalledWith('temporalAnomalies');
  });

  it('should save anomalies to local storage', () => {
    const mockAnomalies = [{ id: 2, description: 'another test' }];
    saveAnomalies(mockAnomalies);
    expect(localStorageMock.setItem).toHaveBeenCalledWith('temporalAnomalies', JSON.stringify(mockAnomalies));
  });

  it('should handle errors when loading anomalies', () => {
    localStorageMock.getItem.mockImplementationOnce(() => {
      throw new Error('Parsing error');
    });
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {}); // Mock rationale: Suppress console error for expected error handling test.
    expect(loadAnomalies()).toEqual([]);
    expect(consoleErrorSpy).toHaveBeenCalled();
    consoleErrorSpy.mockRestore();
  });

  it('should handle errors when saving anomalies', () => {
    localStorageMock.setItem.mockImplementationOnce(() => {
      throw new Error('Storage error');
    });
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {}); // Mock rationale: Suppress console error for expected error handling test.
    saveAnomalies([{ id: 3, description: 'error test' }]);
    expect(consoleErrorSpy).toHaveBeenCalled();
    consoleErrorSpy.mockRestore();
  });
});
