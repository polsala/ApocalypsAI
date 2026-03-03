import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import App from "../src/App";

test("initial total weight is 0", () => {
  render(<App />);
  expect(screen.getByText(/Total Weight:/i)).toHaveTextContent("0.00");
});

test("selecting items updates total weight", () => {
  render(<App />);
  const waterCheckbox = screen.getByLabelText(/Water Bottle/i);
  fireEvent.click(waterCheckbox);
  expect(screen.getByText(/Total Weight:/i)).toHaveTextContent("2.00");

  const foodCheckbox = screen.getByLabelText(/Canned Food/i);
  fireEvent.click(foodCheckbox);
  // total should be 2 + 3 = 5
  expect(screen.getByText(/Total Weight:/i)).toHaveTextContent("5.00");
});
