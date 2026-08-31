#!/usr/bin/env node
"use strict";

const fs = require("fs");

function convertToKg(item) {
  if (item.unit === "kg") return item.weight;
  if (item.unit === "lb") return item.weight * 0.453592;
  throw new Error(`Unsupported unit: ${item.unit}`);
}
function convertToLb(item) {
  if (item.unit === "lb") return item.weight;
  if (item.unit === "kg") return item.weight * 2.20462;
  throw new Error(`Unsupported unit: ${item.unit}`);
}

/**
 * Compute total weight in kg and lb.
 * @param {Array<{name:string,weight:number,unit:"kg"|"lb"}>} items
 * @returns {{totalKg:number,totalLb:number}}
 */
function computeTotal(items) {
  const totalKg = items.reduce((sum, i) => sum + convertToKg(i), 0);
  const totalLb = items.reduce((sum, i) => sum + convertToLb(i), 0);
  // round to 6 decimal places for readability
  return {
    totalKg: Math.round(totalKg * 1e6) / 1e6,
    totalLb: Math.round(totalLb * 1e6) / 1e6,
  };
}

// CLI handling
if (require.main === module) {
  const inputPath = process.argv[2];
  let raw = "";
  if (inputPath) {
    raw = fs.readFileSync(inputPath, "utf8");
    try {
      const items = JSON.parse(raw);
      const result = computeTotal(items);
      console.log(JSON.stringify(result));
    } catch (e) {
      console.error("Error parsing input:", e.message);
      process.exit(1);
    }
  } else {
    // Read from stdin
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => (raw += chunk));
    process.stdin.on("end", () => {
      try {
        const items = JSON.parse(raw);
        const result = computeTotal(items);
        console.log(JSON.stringify(result));
      } catch (e) {
        console.error("Error parsing input:", e.message);
        process.exit(1);
      }
    });
    if (process.stdin.isTTY) {
      console.error("No input provided.");
      process.exit(1);
    }
  }
}

module.exports = { computeTotal };
