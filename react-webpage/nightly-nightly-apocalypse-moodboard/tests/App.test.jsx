import { render, screen } from "@testing-library/react";
import App from "../src/App";

// Mock Date to a fixed day
const RealDate = Date;

function mockDate(isoDate) {
  global.Date = class extends RealDate {
    constructor(...args) {
      if (args.length) {
        return new RealDate(...args);
      }
      return new RealDate(isoDate);
    }
    static now() {
      return new RealDate(isoDate).getTime();
    }
    static parse(str) {
      return RealDate.parse(str);
    }
    static UTC(...args) {
      return RealDate.UTC(...args);
    }
  };
}

afterAll(() => {
  global.Date = RealDate;
});

test("renders deterministic mood for mocked date", () => {
  mockDate("2023-01-01T00:00:00Z");
  render(<App />);
  const dateStr = "2023-01-01";
  const moods = [
    { phrase: "Radiant Ruins", color: "#ff7f7f" },
    { phrase: "Dusty Dawn", color: "#ffd27f" },
    { phrase: "Gleeful Grit", color: "#7fff7f" },
    { phrase: "Mellow Mutant", color: "#7fd2ff" },
    { phrase: "Serene Fallout", color: "#d27fff" },
    { phrase: "Optimistic Oblivion", color: "#ff7fd2" }
  ];
  let hash = 0;
  for (let i = 0; i < dateStr.length; i++) {
    hash = (hash + dateStr.charCodeAt(i)) % moods.length;
  }
  const expectedPhrase = moods[hash].phrase;
  expect(screen.getByText(expectedPhrase)).toBeInTheDocument();
});
