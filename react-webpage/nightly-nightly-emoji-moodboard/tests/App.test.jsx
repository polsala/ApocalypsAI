import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import App from "../src/App";

test("renders five emojis and refresh button works", () => {
  render(<App />);
  const emojiDiv = screen.getByTestId("emoji");
  // Ensure exactly 5 emojis are displayed (split by whitespace)
  expect(emojiDiv.textContent.trim().split(/\s+/).filter(Boolean).length).toBe(5);
  const button = screen.getByText(/refresh/i);
  const firstEmojis = emojiDiv.textContent;
  fireEvent.click(button);
  const secondEmojis = emojiDiv.textContent;
  // After refresh still 5 emojis
  expect(secondEmojis.trim().split(/\s+/).filter(Boolean).length).toBe(5);
  // The set may change; we just assert it's still 5 items
});
