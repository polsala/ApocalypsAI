import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import App from "../src/App";

// Mock localStorage to keep tests deterministic
beforeEach(() => {
  const store = {};
  const localStorageMock = {
    getItem: key => (key in store ? store[key] : null),
    setItem: (key, value) => { store[key] = value.toString(); },
    clear: () => { Object.keys(store).forEach(key => delete store[key]); },
    removeItem: key => { delete store[key]; }
  };
  Object.defineProperty(window, "localStorage", { value: localStorageMock });
});

test("renders initial items and toggles completion", () => {
  render(<App />);
  const waterItem = screen.getByText(/Water filter/i);
  expect(waterItem).toBeInTheDocument();

  const checkboxes = screen.getAllByRole("checkbox");
  expect(checkboxes[0]).not.toBeChecked();
  fireEvent.click(checkboxes[0]);
  expect(checkboxes[0]).toBeChecked();
});

test("adds a new checklist item", () => {
  render(<App />);
  const input = screen.getByPlaceholderText(/New item/i);
  fireEvent.change(input, { target: { value: "Radiation suit" } });
  fireEvent.click(screen.getByText(/Add/i));
  expect(screen.getByText(/Radiation suit/i)).toBeInTheDocument();
});
