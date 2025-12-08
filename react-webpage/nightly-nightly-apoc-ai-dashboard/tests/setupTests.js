// Jest setup file for ApocalypsAI Dashboard tests

// Mock CSS imports
jest.mock('../src/App.css', () => ({}));
jest.mock('../src/index.css', () => ({}));

// Mock environment variables
process.env.REACT_APP_GITHUB_TOKEN = 'mock-token';
process.env.REACT_APP_REPO_OWNER = 'polsala';
process.env.REACT_APP_REPO_NAME = 'ApocalypsAI';

// Mock console methods to reduce noise
const originalError = console.error;
const originalWarn = console.warn;

beforeAll(() => {
  console.error = jest.fn();
  console.warn = jest.fn();
});

afterAll(() => {
  console.error = originalError;
  console.warn = originalWarn;
});

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock ResizeObserver
global.ResizeObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));
