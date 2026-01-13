import React from "react";
import { render, fireEvent, screen } from "@testing-library/react";
import App from "../src/App";

test("displays weather after entering city", () => {
  render(<App />);
  const input = screen.getByTestId("city-input");
  fireEvent.change(input, { target: { value: "Atlantis" } });
  const btn = screen.getByTestId("weather-btn");
  fireEvent.click(btn);
  const output = screen.getByTestId("weather-output");
  expect(output.textContent).toMatch(/Atlantis/);
});

test("cycles memes on button click", () => {
  render(<App />);
  const img = screen.getByTestId("meme-image");
  const firstSrc = img.src;
  const btn = screen.getByTestId("meme-btn");
  fireEvent.click(btn);
  const secondSrc = img.src;
  expect(secondSrc).not.toBe(firstSrc);
});
