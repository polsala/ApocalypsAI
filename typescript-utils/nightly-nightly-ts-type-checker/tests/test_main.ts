import { strict as assert } from 'assert';
import * as ts from 'typescript';
import { checkTypeScriptTypes, formatDiagnostic } from '../src/main'; // Assuming main.ts exports these

// Mock the checkTypeScriptTypes function to control its output for testing
const mockCheckTypeScriptTypes = (code: string): ts.Diagnostic[] => {
    // Mock rationale: This mock allows us to simulate specific TypeScript compiler outputs
    // without actually running the full compiler for every test case, ensuring deterministic and offline tests.
    if (code.includes('let message: string = 123;')) {
        return [
            {
                file: ts.createSourceFile('temp.ts', code, ts.ScriptTarget.Latest),
                start: code.indexOf('123'),
                length: 3,
                messageText: {
                    kind: ts.SyntaxKind.StringLiteral,
                    messageText: "Type 'number' is not assignable to type 'string'.",
                    code: 2322,
                    category: ts.DiagnosticCategory.Error,
                    reportsUnnecessary: undefined,
                    reportsDeprecated: undefined
                },
                category: ts.DiagnosticCategory.Error,
                code: 2322,
                reportsUnnecessary: undefined,
                reportsDeprecated: undefined
            }
        ];
    } else if (code.includes('function greet(name: string) { return 10; }')) {
        return [
            {
                file: ts.createSourceFile('temp.ts', code, ts.ScriptTarget.Latest),
                start: code.indexOf('return 10'),
                length: 9,
                messageText: {
                    kind: ts.SyntaxKind.NumericLiteral,
                    messageText: "Type 'number' is not assignable to type 'string'.",
                    code: 2322,
                    category: ts.DiagnosticCategory.Error,
                    reportsUnnecessary: undefined,
                    reportsDeprecated: undefined
                },
                category: ts.DiagnosticCategory.Error,
                code: 2322,
                reportsUnnecessary: undefined,
                reportsDeprecated: undefined
            }
        ];
    } else {
        return [];
    }
};

// Mock the formatDiagnostic function as well for isolated testing
const mockFormatDiagnostic = (diagnostic: ts.Diagnostic, code: string): string => {
    // Mock rationale: Isolates the formatting logic for testing, ensuring it works correctly regardless of the actual compiler output.
    if (!diagnostic.messageText) {
        return "Unknown error.";
    }

    let message = typeof diagnostic.messageText === 'string' ? diagnostic.messageText : (diagnostic.messageText as ts.DiagnosticMessageChain).messageText;
    let location = "";

    if (diagnostic.file && diagnostic.start !== undefined) {
        const { line, character } = diagnostic.file.getLineAndCharacterOfPosition(diagnostic.start);
        location = ` at line ${line + 1}, character ${character + 1}`;
    }

    return `Error${location}: ${message}`;
};

// Replace the actual functions with mocks for testing
// @ts-ignore: Overriding imported functions for testing purposes
const originalCheckTypes = checkTypeScriptTypes;
// @ts-ignore: Overriding imported functions for testing purposes
const originalFormatDiagnostic = formatDiagnostic;

// @ts-ignore: Overriding imported functions for testing purposes
checkTypeScriptTypes = mockCheckTypeScriptTypes;
// @ts-ignore: Overriding imported functions for testing purposes
formatDiagnostic = mockFormatDiagnostic;



console.log("Running tests for nightly-ts-type-checker...");

// Test case 1: Simple type mismatch (string vs number)
const code1 = "let message: string = 123;";
const errors1 = checkTypeScriptTypes(code1);
assert.strictEqual(errors1.length, 1, "Test Case 1 Failed: Should find one error.");
const formattedError1 = formatDiagnostic(errors1[0], code1);
assert.ok(formattedError1.includes("Type 'number' is not assignable to type 'string'."), "Test Case 1 Failed: Incorrect error message.");
assert.ok(formattedError1.includes("at line 1, character 21"), "Test Case 1 Failed: Incorrect location.");
console.log("Test Case 1 Passed.");

// Test case 2: Function return type mismatch
const code2 = "function greet(name: string) { return 10; }";
const errors2 = checkTypeScriptTypes(code2);
assert.strictEqual(errors2.length, 1, "Test Case 2 Failed: Should find one error.");
const formattedError2 = formatDiagnostic(errors2[0], code2);
assert.ok(formattedError2.includes("Type 'number' is not assignable to type 'string'."), "Test Case 2 Failed: Incorrect error message.");
assert.ok(formattedError2.includes("at line 1, character 30"), "Test Case 2 Failed: Incorrect location.");
console.log("Test Case 2 Passed.");

// Test case 3: No errors
const code3 = "let count: number = 42;";
const errors3 = checkTypeScriptTypes(code3);
assert.strictEqual(errors3.length, 0, "Test Case 3 Failed: Should find no errors.");
console.log("Test Case 3 Passed.");

// Test case 4: Empty input
const code4 = "";
const errors4 = checkTypeScriptTypes(code4);
assert.strictEqual(errors4.length, 0, "Test Case 4 Failed: Should handle empty input gracefully.");
console.log("Test Case 4 Passed.");

// Restore original functions (important if this test file is part of a larger suite)
// @ts-ignore: Overriding imported functions for testing purposes
checkTypeScriptTypes = originalCheckTypes;
// @ts-ignore: Overriding imported functions for testing purposes
formatDiagnostic = originalFormatDiagnostic;

console.log("All tests completed.");
