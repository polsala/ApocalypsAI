import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import App from "../src/App";

test("displays emojis for known mood", () => {
  render(<App />);
  const input = screen.getByLabelText("mood-input");
  fireEvent.change(input, { target: { value: "happy" } });
  fireEvent.click(screen.getByText("Show Emojis"));
  const output = screen.getByLabelText("emoji-output");
  expect(output.textContent).toContain("😄");
  expect(output.textContent).toContain("😊");
  expect(output.textContent).toContain("🥳");
});

test("displays fallback for unknown mood", () => {
  render(<App />);
  const input = screen.getByLabelText("mood-input");
  fireEvent.change(input, { target: { value: "unknownmood" } });
  fireEvent.click(screen.getByText("Show Emojis"));
  const output = screen.getByLabelText("emoji-output");
  expect(output.textContent).toContain("🤔");
});
