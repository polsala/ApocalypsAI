import '@testing-library/jest-dom';

// Mock performance.now() for deterministic time in tests
let mockPerformanceTime = 0;
Object.defineProperty(window.performance, 'now', {
  value: () => mockPerformanceTime,
  writable: true,
});

// Mock requestAnimationFrame and cancelAnimationFrame
let animationFrameCallbacks = [];
let animationFrameIdCounter = 0;

window.requestAnimationFrame = vi.fn((callback) => {
  const id = ++animationFrameIdCounter;
  animationFrameCallbacks.push({ id, callback });
  return id;
});

window.cancelAnimationFrame = vi.fn((id) => {
  animationFrameCallbacks = animationFrameCallbacks.filter(cb => cb.id !== id);
});

// Helper to advance animation frames
global.advanceAnimationFrames = (count = 1, deltaTime = 16) => {
  for (let i = 0; i < count; i++) {
    mockPerformanceTime += deltaTime;
    const callbacksToRun = [...animationFrameCallbacks];
    animationFrameCallbacks = []; // Clear for next frame's requests
    callbacksToRun.forEach(({ callback }) => callback(mockPerformanceTime));
  }
};

// Mock HTMLCanvasElement for testing canvas interactions
const mockCanvasContext = {
  clearRect: vi.fn(),
  beginPath: vi.fn(),
  arc: vi.fn(),
  stroke: vi.fn(),
  fill: vi.fn(),
  measureText: vi.fn(() => ({ width: 10 })),
  set strokeStyle(value) { this._strokeStyle = value; },
  get strokeStyle() { return this._strokeStyle; },
  set lineWidth(value) { this._lineWidth = value; },
  get lineWidth() { return this._lineWidth; },
  set globalAlpha(value) { this._globalAlpha = value; },
  get globalAlpha() { return this._globalAlpha; },
  // Add other context methods as needed
};

HTMLCanvasElement.prototype.getContext = vi.fn(() => mockCanvasContext);

// Mock offsetWidth and offsetHeight for canvas sizing
Object.defineProperty(HTMLElement.prototype, 'offsetWidth', {
  configurable: true,
  value: 800,
});
Object.defineProperty(HTMLElement.prototype, 'offsetHeight', {
  configurable: true,
  value: 600,
});

// Reset mocks before each test
beforeEach(() => {
  vi.clearAllMocks();
  mockPerformanceTime = 0;
  animationFrameCallbacks = [];
  animationFrameIdCounter = 0;
  mockCanvasContext.clearRect.mockClear();
  mockCanvasContext.beginPath.mockClear();
  mockCanvasContext.arc.mockClear();
  mockCanvasContext.stroke.mockClear();
  mockCanvasContext.fill.mockClear();
  mockCanvasContext.measureText.mockClear();
  mockCanvasContext._strokeStyle = undefined;
  mockCanvasContext._lineWidth = undefined;
  mockCanvasContext._globalAlpha = undefined;
});
