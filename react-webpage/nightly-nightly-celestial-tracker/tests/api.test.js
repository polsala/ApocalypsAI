import { fetchCelestialData } from '../src/api';
import * as utils from '../src/utils';

describe('api', () => {
  // Mock rationale: We mock the underlying utility functions to ensure the API layer
  // correctly calls them and formats the output, without re-testing the utility logic itself.
  // This keeps the API tests focused on the API's responsibility.

  const mockPositions = [
    { name: 'MockSolara', angle: 10, color: 'red' },
    { name: 'MockLunaris', angle: 180, color: 'blue' }
  ];
  const mockInfluences = ['Mock Conjunction: Test influence.'];

  beforeEach(() => {
    jest.spyOn(utils, 'calculateCelestialPositions').mockReturnValue(mockPositions);
    jest.spyOn(utils, 'determineAlignmentInfluence').mockReturnValue(mockInfluences);
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('fetchCelestialData should return positions and influences', async () => {
    const testDate = new Date('2023-04-01T00:00:00Z');
    const data = await fetchCelestialData(testDate);

    expect(utils.calculateCelestialPositions).toHaveBeenCalledWith(testDate);
    expect(utils.determineAlignmentInfluence).toHaveBeenCalledWith(mockPositions);

    expect(data).toEqual({
      positions: mockPositions,
      influences: mockInfluences
    });
  });

  test('fetchCelestialData should return a promise', () => {
    const testDate = new Date();
    const result = fetchCelestialData(testDate);
    expect(result).toBeInstanceOf(Promise);
  });
});
