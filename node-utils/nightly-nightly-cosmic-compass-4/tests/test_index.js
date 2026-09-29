const { faker } = require('@faker-js/faker');
const cosmicCompass = require('../src/index'); // Adjust path as needed

// Mock the faker library to ensure deterministic tests
jest.mock('@faker-js/faker', () => ({
  word: {
    adjective: jest.fn(),
    noun: jest.fn()
  },
  number: {
    int: jest.fn()
  },
  helpers: {
    arrayElement: jest.fn()
  }
}));

describe('Cosmic Compass', () => {
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
  });

  describe('generateStarSystemName', () => {
    it('should generate a star system name using mocked faker', () => {
      // Mock rationale: Ensure deterministic output for name generation.
      faker.word.adjective.mockReturnValue('Radiant');
      faker.word.noun.mockReturnValue('Nebula');
      const name = cosmicCompass.generateStarSystemName(); // Assuming this function is exported or accessible
      expect(name).toBe('Radiant Nebula');
      expect(faker.word.adjective).toHaveBeenCalledTimes(1);
      expect(faker.word.noun).toHaveBeenCalledTimes(1);
    });
  });

  describe('generateCoordinates', () => {
    it('should generate coordinates using mocked faker', () => {
      // Mock rationale: Ensure deterministic output for coordinate generation.
      faker.number.int.mockReturnValueOnce(500).mockReturnValueOnce(100);
      const coordinates = cosmicCompass.generateCoordinates(); // Assuming this function is exported or accessible
      // We can't directly mock arrayElement for the fixed arrays, so we'll check the structure and a sample value.
      // For a more robust test, we'd mock the array access or the function itself.
      expect(coordinates).toHaveProperty('sector');
      expect(coordinates).toHaveProperty('quadrant');
      expect(coordinates).toHaveProperty('cluster');
      expect(coordinates).toHaveProperty('designation');
      expect(coordinates.designation).toBe('X-100'); // Based on mockReturnValueOnce(100)
    });
  });

  describe('generateDescription', () => {
    it('should generate a description using mocked faker', () => {
      // Mock rationale: Ensure deterministic output for description generation.
      const mockCoordinates = {
        sector: 'Gamma',
        quadrant: 'II',
        cluster: 'Cygnus',
        designation: 'X-7890'
      };
      faker.helpers.arrayElement.mockReturnValueOnce('uncharted asteroid fields');
      faker.helpers.arrayElement.mockReturnValueOnce('a reclusive monastic order');

      const description = cosmicCompass.generateDescription(mockCoordinates); // Assuming this function is exported or accessible
      expect(description).toBe('Located in the Gamma II, this system is known for its uncharted asteroid fields. It is rumored to be a haven for a reclusive monastic order.');
      expect(faker.helpers.arrayElement).toHaveBeenCalledTimes(2);
    });
  });

  describe('generateStarSystem', () => {
    it('should generate a complete star system object with mocked data', async () => {
      // Mock rationale: Ensure deterministic output for the main generation function.
      faker.word.adjective.mockReturnValue('Stellar');
      faker.word.noun.mockReturnValue('Expanse');
      faker.number.int.mockReturnValueOnce(200);
      faker.helpers.arrayElement.mockReturnValueOnce('a sentient gas giant');
      faker.helpers.arrayElement.mockReturnValueOnce('sentient energy beings');

      const system = await cosmicCompass.generateStarSystem();

      expect(system.name).toBe('Stellar Expanse Nebula');
      expect(system.coordinates.sector).toBeDefined(); // We don't mock specific sector/quadrant/cluster here for simplicity, but check they exist.
      expect(system.coordinates.designation).toBe('X-200');
      expect(system.description).toBe('Located in the Alpha I, this system is known for its a sentient gas giant. It is rumored to be a haven for sentient energy beings.'); // Note: Alpha I is default if not mocked, but the description logic uses the mocked phenomena/inhabitants.
    });
  });

  describe('main CLI execution', () => {
    let consoleSpy;

    beforeEach(() => {
      // Mock rationale: Capture console output to verify CLI behavior without actual printing.
      consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
      // Mock the entire generateStarSystem to control its output for CLI test
      jest.spyOn(cosmicCompass, 'generateStarSystem').mockResolvedValue({
        name: 'Mocked Star System',
        coordinates: {
          sector: 'Omega',
          quadrant: 'X',
          cluster: 'Void',
          designation: 'X-0000'
        },
        description: 'A test description.'
      });
    });

    afterEach(() => {
      consoleSpy.mockRestore();
    });

    it('should log star system details when --cli is present', async () => {
      process.argv = ['node', 'src/index.js', '--cli'];
      await cosmicCompass.main();

      expect(consoleSpy).toHaveBeenCalledWith('Star System: Mocked Star System');
      expect(consoleSpy).toHaveBeenCalledWith('Coordinates: Omega X Void X-0000');
      expect(consoleSpy).toHaveBeenCalledWith('Description: A test description.');
    });

    it('should not log details if --cli is not present', async () => {
      process.argv = ['node', 'src/index.js'];
      await cosmicCompass.main();
      expect(consoleSpy).not.toHaveBeenCalled();
    });
  });
});
