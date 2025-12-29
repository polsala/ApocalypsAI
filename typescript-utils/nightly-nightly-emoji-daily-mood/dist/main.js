"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getMood = void 0;
const moods = [
    { emoji: '😀', phrase: 'You are awesome! Keep going!' },
    { emoji: '😢', phrase: 'It’s okay to feel down. Tomorrow is a new day.' },
    { emoji: '😎', phrase: 'Stay cool and keep coding!' },
    { emoji: '😴', phrase: 'Take a break, recharge, and return refreshed.' },
    { emoji: '🤔', phrase: 'Think big, dream bigger, and act boldly.' }
];
function getMood() {
    const idx = Math.floor(Math.random() * moods.length);
    return moods[idx];
}
exports.getMood = getMood;
if (require.main === module) {
    const mood = getMood();
    console.log(`${mood.emoji} ${mood.phrase}`);
}
