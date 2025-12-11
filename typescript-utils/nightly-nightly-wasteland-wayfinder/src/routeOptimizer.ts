export function optimizeRoute(start: string, targets: string[], avoid: string[] = []): string {
  // Mock implementation with type-safe logic
  const sortedTargets = targets.sort((a, b) => b.length - a.length);
  const avoidanceWarning = avoid.length 
    ? `\n⚠️  Avoiding: ${avoid.join(', ')}` 
    : '';

  return `
1. Depart from ${start}
2. Head to nearest ${sortedTargets[0]} cache
3. Scavange ${sortedTargets.join(' & ')}
${avoidanceWarning}`;
}
