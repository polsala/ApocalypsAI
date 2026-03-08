/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  collectCoverageFrom: [
    "src/**/*.ts",
    "!src/index.ts" // CLI entry point doesn't need unit test coverage
  ]
};
