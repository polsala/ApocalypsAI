export function generateQuestSchedule(
  tasks: string[],
  startDate: string,
  randomFn: () => number = Math.random
): string {
  const adjectives = [
    "Mysterious",
    "Ancient",
    "Forgotten",
    "Enchanted",
    "Cursed",
    "Radiant",
    "Shadowy",
    "Glorious"
  ];
  const start = new Date(startDate);
  if (isNaN(start.getTime())) {
    throw new Error("Invalid startDate");
  }
  const lines: string[] = ["# Epic Quest Itinerary", ""];
  tasks.forEach((task, idx) => {
    const day = new Date(start);
    day.setDate(start.getDate() + idx);
    const dateStr = day.toISOString().split("T")[0];
    const adj = adjectives[Math.floor(randomFn() * adjectives.length)];
    lines.push(`## Day ${idx + 1}: ${dateStr} – ${adj} ${task}`);
    lines.push("");
  });
  return lines.join("\n");
}

// CLI handling
if (require.main === module) {
  const [, , startDate, ...tasks] = process.argv;
  if (!startDate || tasks.length === 0) {
    console.error("Usage: ts-node src/questScheduler.ts <startDate> <task1> [task2 ...]");
    process.exit(1);
  }
  try {
    const output = generateQuestSchedule(tasks, startDate);
    console.log(output);
  } catch (e) {
    console.error((e as Error).message);
    process.exit(1);
  }
}
