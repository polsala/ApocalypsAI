export function assignRarity(itemName) {
  const lowerName = itemName.toLowerCase();
  let score = 0;

  // # Mock rationale: This function is pure and deterministic. No external mocks needed.
  // Length contributes to rarity
  score += Math.min(itemName.length / 5, 5); // Max 5 points for length

  // Keywords for higher rarity
  if (lowerName.includes("void") || lowerName.includes("temporal") || lowerName.includes("anomaly")) score += 5;
  if (lowerName.includes("whisper") || lowerName.includes("echo") || lowerName.includes("ancient")) score += 4;
  if (lowerName.includes("glowing") || lowerName.includes("circuit") || lowerName.includes("data")) score += 3;
  if (lowerName.includes("shard") || lowerName.includes("fragment") || lowerName.includes("core")) score += 2;

  // Character complexity
  if (/[^a-z0-9\s]/.test(lowerName)) score += 1; // Special characters
  if (/\d/.test(lowerName)) score += 1; // Numbers

  if (score >= 10) return { level: "Mythic Echo", color: "#8A2BE2", icon: "🌌" }; // BlueViolet
  if (score >= 7) return { level: "Legendary Artifact", color: "#FFD700", icon: "👑" }; // Gold
  if (score >= 4) return { level: "Rare Relic", color: "#00BFFF", icon: "💎" }; // DeepSkyBlue
  if (score >= 2) return { level: "Uncommon Find", color: "#32CD32", icon: "✨" }; // LimeGreen
  return { level: "Common Scavenge", color: "#A9A9A9", icon: "⚙️" }; // DarkGray
}
