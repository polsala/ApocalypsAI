import React, { useState } from "react";
import { songs, quotes } from "./data";

function getRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

export default function RadioPlayer() {
  const [playing, setPlaying] = useState(false);
  const [song, setSong] = useState("");
  const [quote, setQuote] = useState("");

  const toggle = () => {
    if (!playing) {
      setSong(getRandom(songs));
      setQuote(getRandom(quotes));
    }
    setPlaying(!playing);
  };

  return React.createElement(
    "div",
    null,
    React.createElement(
      "button",
      { onClick: toggle },
      playing ? "Stop" : "Play"
    ),
    playing &&
      React.createElement(
        "div",
        { style: { marginTop: "1rem" } },
        React.createElement(
          "p",
          null,
          React.createElement("strong", null, "Now Playing: "),
          song
        ),
        React.createElement(
          "p",
          null,
          React.createElement("em", null, quote)
        )
      )
  );
}
