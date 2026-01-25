import * as fs from 'fs';
import * as path from 'path';

export enum CosmicElement {
    Stardust = "Stardust (New Beginnings)",
    Nebula = "Nebula (Emerging Ideas)",
    Quasar = "Quasar (Focused Power)",
    Void = "Void (To Be Resolved)",
    CometDust = "Comet Dust (Archival Trails)",
    Singularity = "Singularity (Urgent Focus)",
    Unknown = "Unknown (Uncharted Territory)",
}

interface KeywordMapping {
    keywords: string[];
    element: CosmicElement;
}

const cosmicKeywordMap: KeywordMapping[] = [
    { keywords: ["plan", "organize", "list", "schedule", "start", "new"], element: CosmicElement.Stardust },
    { keywords: ["idea", "brainstorm", "concept", "future", "explore", "draft"], element: CosmicElement.Nebula },
    { keywords: ["report", "data", "analysis", "summary", "insight", "conclusion"], element: CosmicElement.Quasar },
    { keywords: ["bug", "error", "fix", "issue", "problem", "debug", "resolve"], element: CosmicElement.Void },
    { keywords: ["archive", "old", "legacy", "history", "past", "reference"], element: CosmicElement.CometDust },
    { keywords: ["urgent", "critical", "deadline", "immediate", "priority", "blocker"], element: CosmicElement.Singularity },
];

export function classifyContent(content: string): CosmicElement {
    const lowerContent = content.toLowerCase();
    for (const mapping of cosmicKeywordMap) {
        for (const keyword of mapping.keywords) {
            if (lowerContent.includes(keyword)) {
                return mapping.element;
            }
        }
    }
    return CosmicElement.Unknown;
}

export async function processInput(input: string): Promise<{ type: 'file' | 'text', content: string, element: CosmicElement }> {
    let content: string;
    let inputType: 'file' | 'text';

    // Check if the input string corresponds to an existing file
    if (fs.existsSync(input) && fs.lstatSync(input).isFile()) {
        content = await fs.promises.readFile(input, 'utf8');
        inputType = 'file';
    } else {
        // Otherwise, treat the input string directly as content
        content = input;
        inputType = 'text';
    }

    const element = classifyContent(content);
    return { type: inputType, content, element };
}

// CLI entry point
export async function runCli(args: string[]): Promise<void> {
    const input = args[2]; // node index.js <input>

    if (!input) {
        console.log("Usage: npx ts-node src/index.ts <file_path_or_text>");
        console.log("       or npm start <file_path_or_text>");
        return;
    }

    try {
        const result = await processInput(input);
        console.log(`\n--- Cosmic Hoard Analysis ---`);
        console.log(`Input Type: ${result.type === 'file' ? 'File' : 'Text Snippet'}`);
        console.log(`Assigned Cosmic Element: ${result.element}`);
        console.log(`\nSuggestion: Consider tagging this with "${result.element.split(' ')[0].toLowerCase()}" or moving to a "${result.element.split(' ')[0].toLowerCase()}-vault".`);
        console.log(`-----------------------------\n`);
    } catch (error: any) {
        console.error(`Error: ${error.message}`);
        process.exit(1);
    }
}

// This block ensures `runCli` is called only when the script is executed directly
if (require.main === module) {
    runCli(process.argv);
}
