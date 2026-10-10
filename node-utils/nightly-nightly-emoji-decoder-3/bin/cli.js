#!/usr/bin/env node
const { decodeEmojis } = require("../src/decoder");
const fs = require("fs");

function getInput(callback) {
  const arg = process.argv[2];
  if (arg) {
    callback(arg);
  } else {
    // read from stdin
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", chunk => (data += chunk));
    process.stdin.on("end", () => callback(data.trim()));
  }
}

getInput(input => {
  const result = decodeEmojis(input);
  console.log(result);
});
