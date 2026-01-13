import React from 'react';
import { renderToString } from 'react-dom/server';
import App from '../src/main.jsx';

// Mock rationale: data is static, so rendering is deterministic

test('renders heatmap title', () => {
  const html = renderToString(<App />);
  expect(html).toContain('Issue Triage Heatmap');
});

test('renders data rows', () => {
  const html = renderToString(<App />);
  expect(html).toContain('2023-10-01');
  expect(html).toContain('5');
});
