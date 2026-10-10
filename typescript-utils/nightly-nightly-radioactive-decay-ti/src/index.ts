#!/usr/bin/env node
import { argv } from 'process';

function parseArgs(args: string[]): { initial: number; halfLife: number; time: number } {
  const result: any = { initial: 1, halfLife: 1, time: 0 };
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--initial' && i + 1 < args.length) {
      result.initial = Number(args[++i]);
    } else if (arg === '--half-life' && i + 1 < args.length) {
      result.halfLife = Number(args[++i]);
    } else if (arg === '--time' && i + 1 < args.length) {
      result.time = Number(args[++i]);
    }
  }
  return result;
}

export function remainingAmount(initial: number, halfLife: number, time: number): number {
  if (halfLife <= 0) throw new Error('Half-life must be positive');
  const decayFactor = Math.pow(0.5, time / halfLife);
  return initial * decayFactor;
}

if (require.main === module) {
  const { initial, halfLife, time } = parseArgs(argv.slice(2));
  try {
    const remaining = remainingAmount(initial, halfLife, time);
    console.log(`Remaining amount: ${remaining}`);
  } catch (e: any) {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  }
}
