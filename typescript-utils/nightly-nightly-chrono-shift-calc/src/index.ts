import {
  add, sub, set, isWeekend, nextMonday, getDay
} from 'date-fns';
import { ChronoShift } from './types';

/**
 * Applies a series of temporal shifts to a given start date.
 *
 * @param startDate The initial date and time.
 * @param shifts An array of ChronoShift objects to apply.
 * @returns The date after all shifts have been applied.
 */
export function applyShifts(startDate: Date, shifts: ChronoShift[]): Date {
  let currentDate = new Date(startDate); // Work with a copy to avoid modifying original

  for (const shift of shifts) {
    switch (shift.type) {
      case 'add':
        currentDate = add(currentDate, { [shift.unit]: shift.value });
        break;
      case 'subtract':
        currentDate = sub(currentDate, { [shift.unit]: shift.value });
        break;
      case 'set-time':
        currentDate = set(currentDate, {
          hours: shift.hour,
          minutes: shift.minute,
          seconds: shift.second,
          milliseconds: 0, // Always reset milliseconds for consistency
        });
        break;
      case 'skip-weekends':
        if (isWeekend(currentDate)) {
          // If it's Saturday or Sunday, move to the next Monday.
          // date-fns' nextMonday correctly handles both Saturday and Sunday.
          currentDate = nextMonday(currentDate);
          // Note: nextMonday sets the time to 00:00:00 of the next Monday.
          // If preserving time is critical, a 'set-time' shift might be needed afterwards.
        }
        break;
      case 'find-next-weekday':
        const targetDay = shift.weekday; // 0 for Sunday, 1 for Monday, ..., 6 for Saturday
        const currentDayOfWeek = getDay(currentDate); // 0 for Sunday, 1 for Monday, ...

        if (currentDayOfWeek === targetDay) {
          // If the current date is already the target weekday, no shift is needed.
          // We interpret "find next" as "find the next occurrence, including today".
        } else {
          // Calculate days to add to reach the target weekday.
          // (targetDay - currentDayOfWeek + 7) % 7 ensures a positive result.
          let daysToAdd = (targetDay - currentDayOfWeek + 7) % 7;
          currentDate = add(currentDate, { days: daysToAdd });
        }
        break;
      default:
        // This case should ideally not be reached due to TypeScript's discriminated unions,
        // but it's good practice for robustness.
        console.warn(`[ChronoShift Calculator] Unknown shift type encountered: ${(shift as any).type}`);
    }
  }
  return currentDate;
}
