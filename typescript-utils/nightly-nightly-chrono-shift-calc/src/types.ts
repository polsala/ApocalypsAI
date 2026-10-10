export type TimeUnit = 'years' | 'months' | 'weeks' | 'days' | 'hours' | 'minutes' | 'seconds';

export type AddSubtractShift = {
  type: 'add' | 'subtract';
  unit: TimeUnit;
  value: number;
};

export type SetTimeShift = {
  type: 'set-time';
  hour: number; // 0-23
  minute: number; // 0-59
  second: number; // 0-59
};

export type SkipWeekendsShift = {
  type: 'skip-weekends';
};

export type FindNextWeekdayShift = {
  type: 'find-next-weekday';
  weekday: 0 | 1 | 2 | 3 | 4 | 5 | 6; // 0 for Sunday, 6 for Saturday
};

export type ChronoShift = AddSubtractShift | SetTimeShift | SkipWeekendsShift | FindNextWeekdayShift;
