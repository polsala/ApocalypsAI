// Mock rationale: This service simulates fetching mood data. In a real application,
// this would make an API call. For deterministic, offline tests, we mock the
// external data source by generating random numbers within a defined range.
export const getSimulatedMood = () => {
  // Simulate mood data between -100 (very low) and 100 (very high)
  // Math.random() generates a number between 0 (inclusive) and 1 (exclusive)
  // (Math.random() * 201) - 100 will give a range from -100 to 100
  return Math.floor(Math.random() * 201) - 100;
};
