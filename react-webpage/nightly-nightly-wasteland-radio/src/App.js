import React from "react";
import RadioPlayer from "./RadioPlayer";

export default function App() {
  return React.createElement(
    "div",
    { style: { fontFamily: "sans-serif", padding: "2rem" } },
    React.createElement("h1", null, "🛠️ Wasteland Radio"),
    React.createElement(RadioPlayer, null)
  );
}
