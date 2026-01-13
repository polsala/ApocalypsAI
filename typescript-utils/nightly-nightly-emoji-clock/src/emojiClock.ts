export function timeToClockEmoji(time: string): string {
  const match = /^(\\d{1,2}):(\\d{2})$/.exec(time.trim());
  if (!match) {
    throw new Error(`Invalid time format: ${time}`);
  }
  let hour = parseInt(match[1], 10);
  const minute = parseInt(match[2], 10);
  hour = hour % 12;
  let emojiHour = hour;
  let isHalf = false;
  if (minute >= 45) {
    emojiHour = (hour + 1) % 12;
  } else if (minute >= 15) {
    isHalf = true;
  }
  const base = [
    "🕛","🕐","🕑","🕒","🕓","🕔","🕕","🕖","🕗","🕘","🕙","🕚"
  ];
  const half = [
    "🕧","🕜","🕝","🕞","🕟","🕠","🕡","🕢","🕣","🕤","🕥","🕦"
  ];
  return isHalf ? half[emojiHour] : base[emojiHour];
}
