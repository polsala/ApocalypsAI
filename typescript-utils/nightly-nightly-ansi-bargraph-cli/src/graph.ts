export interface RenderOptions {
  width?: number;
  color?: boolean;
}

/**
 * Render a simple horizontal bar chart using ANSI characters.
 * @param values array of nonânegative numbers
 * @param options optional rendering options
 * @returns string containing the chart (lines separated by 
)
 */
export function renderBarChart(values: number[], options: RenderOptions = {}): string {
  const width = options.width ?? 40;
  const useColor = options.color ?? false;
  const max = Math.max(...values, 0);
  if (max === 0) {
    return values.map(() => '').join('
');
  }
  const scale = width / max;
  const barChar = 'â';
  const reset = '[0m';
  const red = '[31m';
  const green = '[32m';
  const blue = '[34m';
  const colors = [red, green, blue];
  return values
    .map((v, i) => {
      const len = Math.round(v * scale);
      const bar = barChar.repeat(len);
      if (useColor) {
        const color = colors[i % colors.length];
        return `${color}${bar}${reset}`;
      }
      return bar;
    })
    .join('
');
}
