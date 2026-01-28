"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.romanToInt = exports.intToRoman = void 0;
function intToRoman(num) {
    if (num <= 0 || num >= 4000)
        throw new Error('Number out of range (1-3999)');
    const map = [
        [1000, 'M'],
        [900, 'CM'],
        [500, 'D'],
        [400, 'CD'],
        [100, 'C'],
        [90, 'XC'],
        [50, 'L'],
        [40, 'XL'],
        [10, 'X'],
        [9, 'IX'],
        [5, 'V'],
        [4, 'IV'],
        [1, 'I'],
    ];
    let result = '';
    for (const _a of map) {
        const [value, numeral] = _a;
        while (num >= value) {
            result += numeral;
            num -= value;
        }
    }
    return result;
}
exports.intToRoman = intToRoman;
function romanToInt(s) {
    const map = {
        I: 1,
        V: 5,
        X: 10,
        L: 50,
        C: 100,
        D: 500,
        M: 1000,
    };
    let total = 0;
    let prev = 0;
    for (let i = s.length - 1; i >= 0; i--) {
        const curr = map[s[i].toUpperCase()];
        if (!curr)
            throw new Error(`Invalid Roman numeral character: ${s[i]}`);
        if (curr < prev) {
            total -= curr;
        }
        else {
            total += curr;
            prev = curr;
        }
    }
    return total;
}
exports.romanToInt = romanToInt;
