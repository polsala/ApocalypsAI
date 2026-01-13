import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import App from "../src/App.jsx";

test("renders initial forecast", () => {
  render(<App />);
  const conditionRegex = /(Acid rain|Radiation fog|Solar flare|Dust storm|Glowing aurora)/;
  const conditionElement = screen.getByText(conditionRegex);
  expect(conditionElement).toBeInTheDocument();
});

test("refresh button exists and can be clicked", () => {
  render(<App />);
  const button = screen.getByText("Refresh");
  expect(button).toBeInTheDocument();
  // Mock rationale: The forecast may randomly stay the same after a click; we only verify the button works without error.
  fireEvent.click(button);
  expect(button).toBeInTheDocument();
});

