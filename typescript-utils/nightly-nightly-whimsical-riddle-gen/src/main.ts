#!/usr/bin/env node
import { generateRiddle } from './riddle';

const showAnswer = process.argv.includes('--answer') || process.argv.includes('-a');
const riddle = generateRiddle();
console.log(riddle.question);
if (showAnswer) {
  console.log('\nAnswer: ' + riddle.answer);
}
