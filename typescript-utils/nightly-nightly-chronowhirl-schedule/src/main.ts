import { parseArgs } from 'util';
import { format, addHours, isWithinInterval } from 'date-fns';

enum TimeSlotEmoji {
  SUNRISE = '🌅',
  SUNSET = '🌇',
  CYBER = '💻',
  ZOOM = '🤝',
  LUNCH = '🍱',
  NIGHT = '🌃'
}

interface ScheduleEntry {
  slot: string;
  emoji: string;
  task: string;
}

function getOptimalSlots(tasks: string[], timezone: string): ScheduleEntry[] {
  const now = new Date();
  const baseTime = format(now, 'HH:mm');
  const slots = [];

  const timeBlocks = [
    { start: 6, end: 9, emoji: TimeSlotEmoji.SUNRISE },
    { start: 10, end: 12, emoji: TimeSlotEmoji.CYBER },
    { start: 13, end: 14, emoji: TimeSlotEmoji.LUNCH },
    { start: 15, end: 17, emoji: TimeSlotEmoji.ZOOM },
    { start: 18, end: 20, emoji: TimeSlotEmoji.SUNSET },
    { start: 21, end: 23, emoji: TimeSlotEmoji.NIGHT }
  ];

  const shuffled = [...tasks].sort(() => Math.random() - 0.5);

  return shuffled.map((task, i) => {
    const block = timeBlocks[i % timeBlocks.length];
    const timeStr = format(addHours(now, i), `h:mmaaa '(${block.emoji})'`);
    return {
      slot: `${block.emoji} ${timeStr} Slot`,
      emoji: block.emoji,
      task
    };
  });
}

const { timezone, tasks } = parseArgs({
  options: {
    tz: { type: 'string', short: 't' },
    tasks: { type: 'string' }
  }
});

if (!timezone || !tasks) {
  console.error('Usage: chronowhirl --tz=TIMEZONE --tasks="TASK1,TASK2"');
  process.exit(1);
}

const schedule = getOptimalSlots(tasks.split(','), timezone);

schedule.forEach(entry => {
  console.log(`${entry.slot}: ${entry.task}`);
});
