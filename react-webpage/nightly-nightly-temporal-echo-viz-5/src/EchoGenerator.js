export function generateEchoParameters(text) {
  if (!text || text.trim() === '') {
    return null;
  }

  const cleanText = text.toLowerCase().replace(/[^a-z0-9]/g, '');
  if (cleanText.length === 0) {
    return null;
  }

  let sumAscii = 0;
  let uniqueChars = new Set();

  for (let i = 0; i < cleanText.length; i++) {
    const charCode = cleanText.charCodeAt(i);
    sumAscii += charCode;
    uniqueChars.add(cleanText[i]);
  }

  const length = cleanText.length;
  const numUniqueChars = uniqueChars.size;

  // Deterministic parameter generation
  const rippleCount = (length % 7) + 3; // 3 to 9 ripples
  const baseFrequency = ((sumAscii % 100) / 100) * 0.5 + 0.5; // 0.5 to 1.0
  const colorHue = (sumAscii * length * numUniqueChars) % 360; // 0 to 359
  const distortionMagnitude = (numUniqueChars / 36) * 0.7 + 0.3; // 0.3 to 1.0 (max 36 unique chars a-z, 0-9)
  const animationSpeed = 1 + (length % 5) * 0.2; // 1.0 to 2.0

  return {
    rippleCount,
    baseFrequency,
    colorHue,
    distortionMagnitude,
    animationSpeed,
    seed: sumAscii + length + numUniqueChars // A combined seed for more complex patterns if needed
  };
}
