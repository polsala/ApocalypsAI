# nightly-emoji-encoder

A whimsical Bash utility that converts plain text into a sequence of emojis. Each alphabetic character (a‑z) is mapped to a corresponding emoji, spaces become a pause emoji, and other characters are left unchanged. Great for adding a splash of fun to messages in chat or logs.

## Usage

```sh
./src/emoji_encoder.sh "hello world"
# Output: 🍯🍋🍋🍊🍏 🌊🍏🍎🍊🍎
```

You can also pipe text via **stdin**:

```sh
echo "survive" | ./src/emoji_encoder.sh
```

## Mapping

| Char | Emoji |
|------|-------|
| a | 🍎 |
| b | 🐝 |
| c | 🌊 |
| d | 🍩 |
| e | 🍯 |
| f | 🍟 |
| g | 🍇 |
| h | 🍯 |
| i | 🍦 |
| j | 🕹️ |
| k | 🥝 |
| l | 🍋 |
| m | 🍈 |
| n | 🍜 |
| o | 🍊 |
| p | 🍍 |
| q | ❓ |
| r | 🌈 |
| s | 🍓 |
| t | 🌴 |
| u | 🍇 |
| v | 🎻 |
| w | 🌊 |
| x | ❌ |
| y | 🍋 |
| z | 🦓 |
| (space) | 🌟 |

Characters not listed (numbers, punctuation, etc.) are emitted unchanged.

## License

MIT © ApocalypsAI
