import React from "react";
import Countdown from "./Countdown";

function App() {
  // Example target: Jan 1 2099 UTC
  const targetDate = new Date("2099-01-01T00:00:00Z").getTime();
  return (
    <div style={{ textAlign: "center", marginTop: "2rem" }}>
      <Countdown target={targetDate} />
    </div>
  );
}

export default App;

