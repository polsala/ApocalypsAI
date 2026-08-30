#!/usr/bin/env ts-node

/**
 * Nightly Wasteland Color Namer
 * Converts a hex color into a whimsical apocalypse‑themed name.
 */

export function nameColor(hex: string): string {
  // Remove leading #
  const clean = hex.replace(/^#/, '').trim().toLowerCase()
  if (!/^[0-9a-f]{6}$/.test(clean)) {
    throw new Error('Invalid hex color. Expected format #RRGGBB')
  }
  const r = parseInt(clean.slice(0, 2), 16)
  const g = parseInt(clean.slice(2, 4), 16)
  const b = parseInt(clean.slice(4, 6), 16)

  // Determine adjective based on max component value
  const maxVal = Math.max(r, g, b)
  let adjective: string
  if (maxVal > 200) {
    if (maxVal === r) adjective = 'Scorching'
    else if (maxVal === g) adjective = 'Toxic'
    else adjective = 'Frozen'
  } else {
    adjective = 'Dusty'
  }

  // Determine noun based on dominant channel
  if (r >= g && r >= b) {
    return `${adjective} Ember`
  } else if (g >= r && g >= b) {
    return `${adjective} Mire`
  } else {
    return `${adjective} Glacier`
  }
}

// CLI entry point
if (require.main === module) {
  const arg = process.argv[2]
  if (!arg) {
    console.error('Usage: ts-node src/index.ts <hex-color>')
    process.exit(1)
  }
  try {
    console.log(nameColor(arg))
  } catch (e) {
    console.error((e as Error).message)
    process.exit(1)
  }
}
