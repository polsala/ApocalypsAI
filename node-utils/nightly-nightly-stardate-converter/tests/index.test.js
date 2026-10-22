const { calculateStardate, DEFAULT_EPOCH_DATE, MS_PER_DAY, DEFAULT_BASE_STARDATE } = require('../src/index');

function runTest(name, testFunction) {
  try {
    testFunction();
    console.log(`\u2713 ${name}`); // Checkmark symbol
  } catch (error) {
    console.error(`\u2718 ${name}`); // X mark symbol
    console.error(`  ${error.message}`);
    process.exit(1);
  }
}

runTest('should calculate Stardate for the epoch date correctly', () => {
  // Mock rationale: We are testing the core calculation logic, which relies on standard JavaScript Date objects.
  // The Date object's behavior for fixed input strings and UTC interpretation is deterministic and does not involve external I/O or randomness.
  const epochDateString = '2000-01-01';
  const expectedStardate = DEFAULT_BASE_STARDATE.toFixed(2);
  const result = calculateStardate(epochDateString, DEFAULT_EPOCH_DATE, DEFAULT_BASE_STARDATE);
  if (result !== expectedStardate) {
    throw new Error(`Expected ${expectedStardate}, but got ${result}`);
  }
});

runTest('should calculate Stardate for one day after epoch correctly', () => {
  // Mock rationale: See above.
  const dateString = '2000-01-02';
  const expectedStardate = (DEFAULT_BASE_STARDATE + 1).toFixed(2);
  const result = calculateStardate(dateString, DEFAULT_EPOCH_DATE, DEFAULT_BASE_STARDATE);
  if (result !== expectedStardate) {
    throw new Error(`Expected ${expectedStardate}, but got ${result}`);
  }
});

runTest('should calculate Stardate for one day before epoch correctly', () => {
  // Mock rationale: See above.
  const dateString = '1999-12-31';
  const expectedStardate = (DEFAULT_BASE_STARDATE - 1).toFixed(2);
  const result = calculateStardate(dateString, DEFAULT_EPOCH_DATE, DEFAULT_BASE_STARDATE);
  if (result !== expectedStardate) {
    throw new Error(`Expected ${expectedStardate}, but got ${result}`);
  }
});

runTest('should handle leap year correctly (2000 is a leap year)', () => {
  // Mock rationale: See above. The Date object correctly handles leap years in its calculations.
  const dateString = '2001-01-01'; // 366 days after 2000-01-01 (due to Feb 29, 2000)
  const expectedStardate = (DEFAULT_BASE_STARDATE + 366).toFixed(2);
  const result = calculateStardate(dateString, DEFAULT_EPOCH_DATE, DEFAULT_BASE_STARDATE);
  if (result !== expectedStardate) {
    throw new Error(`Expected ${expectedStardate}, but got ${result}`);
  }
});

runTest('should handle different valid date formats', () => {
  // Mock rationale: See above. The Date object's parsing of various valid date strings is deterministic.
  const dateString = 'July 21, 2024';
  // Calculate expected stardate for '2024-07-21T00:00:00Z' relative to epoch
  const expectedDays = (new Date('2024-07-21T00:00:00Z').getTime() - DEFAULT_EPOCH_DATE.getTime()) / MS_PER_DAY;
  const expectedStardate = (DEFAULT_BASE_STARDATE + expectedDays).toFixed(2);
  const result = calculateStardate(dateString, DEFAULT_EPOCH_DATE, DEFAULT_BASE_STARDATE);
  if (result !== expectedStardate) {
    throw new Error(`Expected ${expectedStardate}, but got ${result}`);
  }
});

runTest('should throw error for invalid date string', () => {
  // Mock rationale: See above. Error handling for invalid Date object construction is deterministic.
  const invalidDateString = 'not-a-date';
  let errorThrown = false;
  try {
    calculateStardate(invalidDateString, DEFAULT_EPOCH_DATE, DEFAULT_BASE_STARDATE);
  } catch (error) {
    errorThrown = true;
    if (!error.message.includes('Invalid date format')) {
      throw new Error(`Expected "Invalid date format" error, but got: ${error.message}`);
    }
  }
  if (!errorThrown) {
    throw new Error('Expected an error to be thrown for invalid date string, but none was.');
  }
});

runTest('should use custom epoch and base stardate correctly', () => {
  // Mock rationale: See above. Custom parameters are passed directly to the calculation function, ensuring deterministic behavior.
  const customEpoch = new Date('2010-01-01T00:00:00Z');
  const customBase = 50000.0;
  const dateString = '2010-01-02'; // One day after custom epoch
  const expectedStardate = (customBase + 1).toFixed(2);
  const result = calculateStardate(dateString, customEpoch, customBase);
  if (result !== expectedStardate) {
    throw new Error(`Expected ${expectedStardate}, but got ${result}`);
  }
});

console.log('\nAll tests passed!');
