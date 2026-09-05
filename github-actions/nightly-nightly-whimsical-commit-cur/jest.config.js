module.exports = {
  clearMocks: true,
  moduleFileExtensions: ['js', 'json', 'node'],
  runner: 'jest-circus',
  testEnvironment: 'node',
  testMatch: ['**/tests/**/*.test.js'],
  testPathIgnorePatterns: ['/node_modules/', '/dist/'],
  verbose: true
};
