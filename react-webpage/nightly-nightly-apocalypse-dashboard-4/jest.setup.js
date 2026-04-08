import '@testing-library/jest-dom';

// Mocking CSS modules for Jest
// Mock rationale: Jest doesn't understand CSS imports directly, and we don't need to test CSS itself.
// 'identity-obj-proxy' is a common solution for this.
jest.mock('identity-obj-proxy');

// Mocking SVG imports for Jest
// Mock rationale: Similar to CSS, Jest doesn't natively handle SVG imports.
// 'jest-transform-stub' is used to treat them as empty modules.
jest.mock('jest-transform-stub');

// Mocking global fetch if needed, though not strictly necessary for this app's current mock setup.
// global.fetch = jest.fn(() =>
//   Promise.resolve({
//     json: () => Promise.resolve({ /* mock response */ }),
//   })
// );
