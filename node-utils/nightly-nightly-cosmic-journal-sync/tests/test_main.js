const fs = require('fs');
const path = require('path');
const { readObservations, syncObservations } = require('../src/main');

// Mock the fetch module to control API responses
jest.mock('node-fetch', () => {
  // Mock the default export of node-fetch
  return jest.fn();
});

// Mock the actual API call within syncObservations
// We'll directly mock the internal mockApiPost function for simplicity in this test
jest.mock('../src/main', () => {
  const originalModule = jest.requireActual('../src/main');
  return {
    ...originalModule,
    // Override the mockApiPost to return controlled responses
    syncObservations: jest.fn(async (observations) => {
      const mockResponseSuccess = { ok: true, status: 200, json: async () => ({ message: 'Mocked success', id: 'mock-id-123' }) };
      const mockResponseFailure = { ok: false, status: 500, json: async () => ({ message: 'Mocked failure' }) };

      const results = [];
      for (const obs of observations) {
        // Simulate success for all observations in this test
        results.push(mockResponseSuccess);
      }
      return results;
    })
  };
});

// Mock console.log and console.error to capture output
let mockConsoleLog;
let mockConsoleError;

beforeEach(() => {
  mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
  mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});
  // Ensure the data directory and file exist before each test
  const dataDir = path.join(__dirname, '../data');
  const observationsFile = path.join(dataDir, 'observations.json');
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }
  fs.writeFileSync(observationsFile, '[]', 'utf8');
});

afterEach(() => {
  mockConsoleLog.mockRestore();
  mockConsoleError.mockRestore();
});

describe('Cosmic Journal Synchronizer', () => {
  describe('readObservations', () => {
    it('should return an empty array if the observations file is empty', () => {
      const observations = readObservations();
      expect(observations).toEqual([]);
    });

    it('should return observations from the JSON file', () => {
      const testObservations = [
        { timestamp: '2023-10-27T10:00:00Z', phenomenon: 'Comet Tail', description: 'A faint streak' },
        { timestamp: '2023-10-27T11:00:00Z', phenomenon: 'Distant Galaxy', description: 'Spiral arms visible' }
      ];
      const observationsFile = path.join(__dirname, '../data/observations.json');
      fs.writeFileSync(observationsFile, JSON.stringify(testObservations), 'utf8');

      const observations = readObservations();
      expect(observations).toEqual(testObservations);
    });

    it('should return an empty array if the observations file is invalid JSON', () => {
      const observationsFile = path.join(__dirname, '../data/observations.json');
      fs.writeFileSync(observationsFile, '{invalid json}', 'utf8');

      const observations = readObservations();
      expect(observations).toEqual([]);
      expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Error reading observations'), expect.any(Error));
    });
  });

  describe('syncObservations', () => {
    it('should do nothing if there are no observations', async () => {
      await syncObservations([]);
      expect(mockConsoleLog).toHaveBeenCalledWith('\n✨ No new observations to sync. The cosmos is quiet tonight!');
    });

    it('should successfully sync multiple observations', async () => {
      const testObservations = [
        { timestamp: '2023-10-27T10:00:00Z', phenomenon: 'Supernova Remnant', description: 'A faint cloud' },
        { timestamp: '2023-10-27T11:00:00Z', phenomenon: 'Asteroid Belt', description: 'Dense region of rocks' }
      ];
      
      // Mock the syncObservations function to return specific mock responses
      // This is a bit of a workaround to test the internal logic of syncObservations
      // without relying on the actual fetch or the internal mockApiPost.
      // In a more complex setup, we'd mock node-fetch directly.
      const mockSync = jest.requireActual('../src/main').syncObservations;
      const mockApiPost = jest.fn(async (url, data) => {
        if (data.phenomenon === 'Supernova Remnant') {
          return { ok: true, status: 200, json: async () => ({ message: 'Logged SN', id: 'sn-123' }) };
        } else {
          return { ok: true, status: 200, json: async () => ({ message: 'Logged Asteroid', id: 'ast-456' }) };
        }
      });
      
      // Temporarily replace the internal mockApiPost for this test
      const originalMockApiPost = require('../src/main').mockApiPost;
      require('../src/main').mockApiPost = mockApiPost;

      await mockSync(testObservations);

      // Restore the original mockApiPost
      require('../src/main').mockApiPost = originalMockApiPost;

      expect(mockConsoleLog).toHaveBeenCalledWith('\n🌌 Syncing 2 cosmic observation(s) to the Starlight Logbook...');
      expect(mockConsoleLog).toHaveBeenCalledWith('  ✅ Successfully logged: Supernova Remnant (ID: sn-123)');
      expect(mockConsoleLog).toHaveBeenCalledWith('  ✅ Successfully logged: Asteroid Belt (ID: ast-456)');
      expect(mockConsoleLog).toHaveBeenCalledWith('\n🌟 Sync complete! 2 out of 2 observations were logged.');
    });

    it('should handle API failures gracefully', async () => {
      const testObservations = [
        { timestamp: '2023-10-27T10:00:00Z', phenomenon: 'Black Hole Event', description: 'Gravitational anomaly' }
      ];

      // Mock the syncObservations function to simulate an API failure
      const mockSync = jest.requireActual('../src/main').syncObservations;
      const mockApiPost = jest.fn(async (url, data) => {
        return { ok: false, status: 500, json: async () => ({ message: 'Internal server error' }) };
      });
      
      const originalMockApiPost = require('../src/main').mockApiPost;
      require('../src/main').mockApiPost = mockApiPost;

      await mockSync(testObservations);

      require('../src/main').mockApiPost = originalMockApiPost;

      expect(mockConsoleLog).toHaveBeenCalledWith('\n🌌 Syncing 1 cosmic observation(s) to the Starlight Logbook...');
      expect(mockConsoleError).toHaveBeenCalledWith('  ❌ Failed to log Black Hole Event. Status: 500');
      expect(mockConsoleLog).toHaveBeenCalledWith('\n🌟 Sync complete! 0 out of 1 observations were logged.');
    });

    it('should handle network errors during sync', async () => {
      const testObservations = [
        { timestamp: '2023-10-27T10:00:00Z', phenomenon: 'Nebula Bloom', description: 'Vibrant gas clouds' }
      ];

      // Mock node-fetch to throw an error
      const fetchMock = require('node-fetch');
      fetchMock.mockImplementation(() => {
        throw new Error('Network connection refused');
      });

      // Temporarily replace the internal mockApiPost to simulate the fetch call
      const originalMockApiPost = require('../src/main').mockApiPost;
      require('../src/main').mockApiPost = jest.fn(async (url, data) => {
        // This mockApiPost will be called, but it will internally call the mocked fetch
        // which will throw an error.
        return await fetch(url, { method: 'POST', body: JSON.stringify(data) });
      });

      await syncObservations(testObservations);

      // Restore mocks
      fetchMock.mockClear();
      require('../src/main').mockApiPost = originalMockApiPost;

      expect(mockConsoleLog).toHaveBeenCalledWith('\n🌌 Syncing 1 cosmic observation(s) to the Starlight Logbook...');
      expect(mockConsoleError).toHaveBeenCalledWith('  ❌ Network error while syncing Nebula Bloom:', 'Network connection refused');
      expect(mockConsoleLog).toHaveBeenCalledWith('\n🌟 Sync complete! 0 out of 1 observations were logged.');
    });
  });
});
