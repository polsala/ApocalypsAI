export const fortunes = [
  "You will find a hidden talent.",
  "A surprise encounter will bring joy.",
  "Your hard work will pay off soon.",
  "A new opportunity is on the horizon.",
  "Trust your instincts in the coming days."
];

export function getFortune(): string {
  const idx = Math.floor(Math.random() * fortunes.length);
  return fortunes[idx];
}

export function printFortune(): void {
  const fortune = getFortune();
  console.log("┌───────────────────────────────┐");
  console.log(`│ ${fortune.padEnd(27)} │`);
  console.log("└───────────────────────────────┘");
  console.log("   \\   ^__^");
  console.log("    \\  (oo)\\_______");
  console.log("       (__)\\       )\/\\");
  console.log("           ||----w |");
  console.log("           ||     ||");
}

if (require.main === module) {
  printFortune();
}
