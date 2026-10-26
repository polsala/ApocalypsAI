import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import App from "../src/App";

test("renders resource names after mock fetch", async () => {
  render(<App />);
  // Wait for mock data to load (setTimeout 100ms in component)
  await waitFor(() => {
    expect(screen.getByText(/Food:/i)).toBeInTheDocument();
    expect(screen.getByText(/Water:/i)).toBeInTheDocument();
    expect(screen.getByText(/Medicine:/i)).toBeInTheDocument();
    expect(screen.getByText(/Fuel:/i)).toBeInTheDocument();
  });
});
