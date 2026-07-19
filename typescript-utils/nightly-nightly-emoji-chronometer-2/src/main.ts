import { formatTime } from "./timeFormatter";

function main() {
  const now = new Date();
  const emojiTime = formatTime(now);
  console.log(emojiTime);
}

if (require.main === module) {
  main();
}

export { main };
