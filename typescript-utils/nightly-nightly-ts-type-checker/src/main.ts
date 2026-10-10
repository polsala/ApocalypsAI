import * as ts from 'typescript';

/**
 * Analyzes a TypeScript code snippet for type errors.
 * @param code The TypeScript code to analyze.
 * @returns An array of diagnostic messages representing type errors.
 */
function checkTypeScriptTypes(code: string): ts.Diagnostic[] {
    // Create a virtual file system host
    const host: ts.CompilerHost = {
        getSourceFile: (fileName, languageVersion) => {
            if (fileName === 'temp.ts') {
                return ts.createSourceFile(fileName, code, languageVersion);
            }
            return undefined;
        },
        getDefaultLibFileName: (options) => ts.getDefaultLibFileName(options),
        writeFile: (fileName, data, writeByteOrderMark, onError) => { /* no-op */ },
        getCurrentDirectory: () => "/",
        getDirectories: (path: string) => [],
        fileExists: (fileName) => fileName === 'temp.ts',
        readFile: (fileName) => fileName === 'temp.ts' ? code : undefined,
        getCanonicalFileName: (fileName) => fileName,
        useCaseSensitiveFileNames: () => true,
        getNewLine: () => '\n',
        // Add a default implementation for getEnvironmentVariable if needed
        getEnvironmentVariable: (key) => process.env[key] || ''
    };

    // Create a program with the virtual file
    const program = ts.createProgram(['temp.ts'], { noEmitOnError: true, noLib: true }, host);

    // Get all diagnostics for the program
    const diagnostics = ts.getPreEmitDiagnostics(program);

    return diagnostics;
}

/**
 * Formats a TypeScript diagnostic message for human readability.
 * @param diagnostic The diagnostic message to format.
 * @param code The original source code.
 * @returns A formatted string representing the diagnostic.
 */
function formatDiagnostic(diagnostic: ts.Diagnostic, code: string): string {
    if (!diagnostic.messageText) {
        return "Unknown error.";
    }

    let message = typeof diagnostic.messageText === 'string' ? diagnostic.messageText : diagnostic.messageText.messageText;
    let location = "";

    if (diagnostic.file && diagnostic.start !== undefined) {
        const { line, character } = diagnostic.file.getLineAndCharacterOfPosition(diagnostic.start);
        location = ` at line ${line + 1}, character ${character + 1}`;
    }

    return `Error${location}: ${message}`;
}

// --- Main execution --- 

async function main() {
    let inputCode = "";
    process.stdin.on('data', (chunk) => {
        inputCode += chunk.toString();
    });

    process.stdin.on('end', () => {
        if (!inputCode.trim()) {
            console.error("No TypeScript code provided via stdin.");
            process.exit(1);
        }

        const errors = checkTypeScriptTypes(inputCode);

        if (errors.length === 0) {
            console.log("No type errors found. Your code is as pristine as a freshly wiped slate!");
        } else {
            console.log("Found the following type anomalies:");
            errors.forEach(error => {
                console.error(formatDiagnostic(error, inputCode));
            });
            process.exitCode = 1; // Indicate failure
        }
    });
}

main();
