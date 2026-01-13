import { generateCalendar } from "./calendar";

function parseArgs(): { month: number; year: number } {
  const args = process.argv.slice(2);
  const now = new Date();
  let month = now.getMonth() + 1; // 1âbased
  let year = now.getFullYear();
  if (args.length >= 1) {
    const m = Number(args[0]);
    if (!isNaN(m) && m >= 1 && m <= 12) {
      month = m;
    }
  }
  if (args.length >= 2) {
    const y = Number(args[1]);
    if (!isNaN(y) && y >= 1) {
      year = y;
    }
  }
  return { month, year };
}

const { month, year } = parseArgs();
console.log(generateCalendar(month, year));

