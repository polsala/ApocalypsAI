import '@testing-library/jest-dom';
import React from "react";
import { render, fireEvent, screen } from "@testing-library/react";
import App from "../src/App";

test('renders title and play button', () => {
  render(React.createElement(App));
  expect(screen.getByText('🛠️ Wasteland Radio')).toBeInTheDocument();
  expect(screen.getByText('Play')).toBeInTheDocument();
});

test('shows song and quote after playing', () => {
  render(React.createElement(App));
  const button = screen.getByText('Play');
  fireEvent.click(button);
  expect(screen.getByText('Stop')).toBeInTheDocument();
  expect(screen.getByText(/Now Playing:/)).toBeInTheDocument();
  // Quote is rendered inside an <em> element; verify its presence
  const quoteEl = screen.getByText((content, element) => element.tagName.toLowerCase() === 'em');
  expect(quoteEl).toBeInTheDocument();
});
