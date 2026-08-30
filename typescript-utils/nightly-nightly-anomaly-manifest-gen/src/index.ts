import { AnomalyInput, AnomalyManifestEntry, AnomalyCategory, AnomalySeverity } from './types';

/**
 * Classifies an anomaly's category and severity based on keywords in its description.
 * @param description The raw description of the anomaly.
 * @returns An object containing the classified category and severity.
 */
export function classifyAnomaly(description: string): { category: AnomalyCategory; severity: AnomalySeverity } {
  const lowerDesc = description.toLowerCase();
  let category: AnomalyCategory = "Unknown";
  let severity: AnomalySeverity = "Unknown";

  // --- Category classification ---
  if (lowerDesc.includes("time") || lowerDesc.includes("temporal") || lowerDesc.includes("loop") || lowerDesc.includes("echo") || lowerDesc.includes("chronal")) {
    category = "Temporal Distortion";
  } else if (lowerDesc.includes("reality") || lowerDesc.includes("glitch") || lowerDesc.includes("flicker") || lowerDesc.includes("impossible") || lowerDesc.includes("paradox")) {
    category = "Reality Glitch";
  } else if (lowerDesc.includes("space") || lowerDesc.includes("spatial") || lowerDesc.includes("teleport") || lowerDesc.includes("displace") || lowerDesc.includes("rift")) {
    category = "Spatial Displacement";
  } else if (lowerDesc.includes("energy") || lowerDesc.includes("power") || lowerDesc.includes("surge") || lowerDesc.includes("radiation") || lowerDesc.includes("flux")) {
    category = "Energy Fluctuation";
  } else if (lowerDesc.includes("creature") || lowerDesc.includes("mutation") || lowerDesc.includes("flora") || lowerDesc.includes("fauna") || lowerDesc.includes("organic")) {
    category = "Biological Mutation";
  }

  // --- Severity classification ---
  if (lowerDesc.includes("critical") || lowerDesc.includes("catastrophic") || lowerDesc.includes("imminent") || lowerDesc.includes("apocalyptic")) {
    severity = "Critical";
  } else if (lowerDesc.includes("severe") || lowerDesc.includes("dangerous") || lowerDesc.includes("major") || lowerDesc.includes("hazardous")) {
    severity = "Severe";
  } else if (lowerDesc.includes("moderate") || lowerDesc.includes("noticeable") || lowerDesc.includes("disruptive") || lowerDesc.includes("significant")) {
    severity = "Moderate";
  } else if (lowerDesc.includes("minor") || lowerDesc.includes("slight") || lowerDesc.includes("subtle") || lowerDesc.includes("insignificant")) {
    severity = "Minor";
  }

  return { category, severity };
}

/**
 * Generates a simple, non-cryptographic unique ID.
 * This avoids external dependencies like 'uuid'.
 * @returns A unique string ID.
 */
function generateSimpleId(): string {
  return Date.now().toString(36) + Math.random().toString(36).substring(2, 7);
}

/**
 * Takes an array of raw anomaly inputs and generates a structured, classified manifest.
 * @param inputs An array of AnomalyInput objects.
 * @returns An array of AnomalyManifestEntry objects.
 */
export function generateAnomalyManifest(inputs: AnomalyInput[]): AnomalyManifestEntry[] {
  return inputs.map(input => {
    const { category, severity } = classifyAnomaly(input.description);
    return {
      id: generateSimpleId(),
      timestamp: new Date().toISOString(),
      description: input.description,
      location: input.location,
      observedBy: input.observedBy,
      category,
      severity,
      notes: `Auto-classified based on keywords: ${category}, ${severity}. Review manually if needed.`
    };
  });
}

/**
 * Main function for the CLI entry point.
 * Reads JSON input from stdin, processes it, and writes JSON output to stdout.
 */
async function main() {
  try {
    const inputBuffer = await new Promise<string>((resolve, reject) => {
      let data = '';
      process.stdin.on('data', chunk => data += chunk);
      process.stdin.on('end', () => resolve(data));
      process.stdin.on('error', err => reject(err));
    });

    const rawInputs: AnomalyInput[] = JSON.parse(inputBuffer);
    const manifest = generateAnomalyManifest(rawInputs);
    console.log(JSON.stringify(manifest, null, 2));
  } catch (error: any) {
    console.error(`Error: Failed to process input. Ensure it's valid JSON array of anomaly objects. Details: ${error.message}`);
    process.exit(1);
  }
}

// Only run main if the script is executed directly
if (require.main === module) {
  main();
}
