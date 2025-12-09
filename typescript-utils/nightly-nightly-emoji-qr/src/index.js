const emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣'];
function charToEmoji(ch) {
    const code = ch.charCodeAt(0);
    return emojis[code % emojis.length];
}
function generateEmojiGrid(input) {
    const chars = input.split('');
    const size = Math.ceil(Math.sqrt(chars.length));
    const total = size * size;
    while (chars.length < total) {
        chars.push(' ');
    }
    const rows = [];
    for (let r = 0; r < size; r++) {
        let row = '';
        for (let c = 0; c < size; c++) {
            const idx = r * size + c;
            row += charToEmoji(chars[idx]);
        }
        rows.push(row);
    }
    return rows;
}
function main() {
    const args = process.argv.slice(2);
    if (args.length > 0) {
        const input = args.join(' ');
        const grid = generateEmojiGrid(input);
        console.log(grid.join('\n'));
    }
    else {
        let data = '';
        process.stdin.setEncoding('utf8');
        process.stdin.on('data', chunk => data += chunk);
        process.stdin.on('end', () => {
            const input = data.trim();
            const grid = generateEmojiGrid(input);
            console.log(grid.join('\n'));
        });
    }
}
if (require.main === module) {
    main();
}
