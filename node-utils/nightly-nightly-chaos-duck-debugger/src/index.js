#!/usr/bin/env node

const scenarios = [
  "You're debugging a function that's supposed to reverse a string, but it's returning numbers instead.",
  "Your API call works in Postman but fails in code. The error says 'CORS'.",
  "A React component re-renders infinitely, even though you're using React.memo.",
  "You're trying to parse JSON but keep getting 'Unexpected token o in JSON at position 1'.",
  "Your CSS grid isn't aligning items, even though you've set justify-content correctly.",
  "Node.js script exits immediately without running any async code."
];

const hints = [
  "Quack! Maybe check if you're accidentally calling .length instead of .reverse()?",
  "Quack! CORS issues often stem from missing headers on the server side.",
  "Quack! Did you forget to wrap your component in React.memo's parentheses?",
  "Quack! Sounds like you're parsing something already parsed. Check for double parsing!",
  "Quack! Grid items might be overriding your justify-content. Try justify-items.",
  "Quack! Async functions need to be awaited or handled with .then()."
];

function getRandomElement(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function chaosDuckDebugger() {
  const scenario = getRandomElement(scenarios);
  const hint = getRandomElement(hints);

  console.log(`🚨 DEBUGGING CHALLENGE 🚨\n\n${scenario}\n\n🦆 Rubber Duck says: \"${hint}\"\n`);
}

chaosDuckDebugger();
