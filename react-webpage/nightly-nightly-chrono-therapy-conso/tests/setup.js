// # Mock rationale: localStorage is a browser API and needs to be mocked for deterministic, offline testing in a Node.js environment (Vitest).
// This ensures tests don't interfere with actual browser storage and run consistently.
import '@testing-library/jest-dom/vitest'; // Import for extended matchers

const localStorageMock = (function() {
  let store = {};
  return {
    getItem(key) {
      return store[key] || null;
    },
    setItem(key, value) {
      store[key] = value.toString();
    },
    clear() {
      store = {};
    },
    removeItem(key) {
      delete store[key];
    }
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock
});
