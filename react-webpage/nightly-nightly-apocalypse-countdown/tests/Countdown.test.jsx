import React from "react";
import { render, screen } from "@testing-library/react";
import Countdown from "../src/Countdown";

test("displays correct countdown for mocked time", () => {
  // Mock Date.now to a fixed point
  // Mock rationale: deterministic test without real time passing
  const MOCK_NOW = new Date("2098-12-31T23:59:50Z").getTime();
  const TARGET = new Date("2099-01-01T00:00:00Z").getTime();

  jest.spyOn(Date, "now").mockImplementation(() => MOCK_NOW);

  render(<Countdown target={TARGET} />);

  // Expect 0d 0h 0m 10s remaining
  const timeElement = screen.getByText(/0d 0h 0m 10s/);
  expect(timeElement).toBeInTheDocument();

  // Clean up mock
  Date.now.mockRestore();
});

