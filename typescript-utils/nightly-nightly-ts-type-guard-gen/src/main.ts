import ts from 'typescript';
import fs from 'fs';
import path from 'path';
import { program } from 'commander';

interface InterfaceInfo {
  name: string;
  properties: { name: string; type: string }[];
}

function extractInterfaces(filePath: string): InterfaceInfo[] {
  const program = ts.createProgram([filePath], { allowJs: true });
  const checker = program.getTypeChecker();
  const sourceFile = program.getSourceFile(filePath);

  if (!sourceFile) {
    throw new Error(`Could not find source file: ${filePath}`);
  }

  const interfaces: InterfaceInfo[] = [];

  ts.forEachChild(sourceFile, (node) => {
    if (ts.isInterfaceDeclaration(node) && node.name) {
      const interfaceName = node.name.text;
      const properties: { name: string; type: string }[] = [];

      ts.forEachChild(node, (member) => {
        if (ts.isPropertySignature(member) && member.name && member.type) {
          const propertyName = member.name.getText(sourceFile);
          const propertyType = checker.typeToString(checker.getTypeAtLocation(member.type));
          properties.push({ name: propertyName, type: propertyType });
        }
      });
      interfaces.push({ name: interfaceName, properties });
    }
  });

  return interfaces;
}

function generateTypeGuard(interfaceInfo: InterfaceInfo): string {
  const { name, properties } = interfaceInfo;
  const guardName = `is${name}`;

  const checks: string[] = [];
  checks.push(`typeof obj === 'object' && obj !== null`);

  properties.forEach(prop => {
    const typeCheck = getPrimitiveTypeCheck(prop.type);
    if (typeCheck) {
      checks.push(`'${prop.name}' in obj && ${typeCheck}`);
    } else if (prop.type.includes('|')) { // Handle union types
      const unionTypes = prop.type.split('|').map(t => t.trim());
      const unionChecks = unionTypes.map(unionType => {
        const primitiveCheck = getPrimitiveTypeCheck(unionType);
        if (primitiveCheck) {
          return `typeof obj.${prop.name} === '${unionType}'`;
        } else if (unionType === 'any') {
          return `obj.${prop.name} !== undefined`;
        } else if (unionType.endsWith('[]')) { // Array check
            const elementType = unionType.slice(0, -2);
            const elementCheck = getPrimitiveTypeCheck(elementType);
            if (elementCheck) {
                return `Array.isArray(obj.${prop.name}) && obj.${prop.name}.every((item: any) => ${elementCheck})`;
            } else {
                // Fallback for complex array elements, could be recursive or require more sophisticated parsing
                return `Array.isArray(obj.${prop.name})`;
            }
        } else {
          // For complex types (e.g., other interfaces), we'd need recursive calls or a more robust type system integration.
          // For now, we'll assume a basic check or skip.
          return `typeof obj.${prop.name} === 'object'`; // Basic object check as a fallback
        }
      });
      checks.push(`'${prop.name}' in obj && (${unionChecks.join(' || ')})`);
    } else if (prop.type.endsWith('[]')) { // Array check
        const elementType = prop.type.slice(0, -2);
        const elementCheck = getPrimitiveTypeCheck(elementType);
        if (elementCheck) {
            checks.push(`'${prop.name}' in obj && Array.isArray(obj.${prop.name}) && obj.${prop.name}.every((item: any) => ${elementCheck})`);
        } else {
            // Fallback for complex array elements
            checks.push(`'${prop.name}' in obj && Array.isArray(obj.${prop.name})`);
        }
    } else {
      // For complex types (e.g., other interfaces), we'd need recursive calls or a more robust type system integration.
      // For now, we'll assume a basic check or skip.
      checks.push(`'${prop.name}' in obj && typeof obj.${prop.name} === 'object'`); // Basic object check as a fallback
    }
  });

  return `export function ${guardName}(obj: any): obj is ${name} {
  return (
    ${checks.join(' &&
    ')}
  );
}
`;
}

function getPrimitiveTypeCheck(type: string): string | null {
  switch (type) {
    case 'string':
      return "typeof obj.${prop.name} === 'string'" ;
    case 'number':
      return "typeof obj.${prop.name} === 'number'" ;
    case 'boolean':
      return "typeof obj.${prop.name} === 'boolean'" ;
    case 'any':
      return "obj.${prop.name} !== undefined" ;
    case 'null':
      return "obj.${prop.name} === null" ;
    case 'undefined':
      return "obj.${prop.name} === undefined" ;
    default:
      return null;
  }
}

function main() {
  program
    .option('-i, --input <file>', 'Input TypeScript file path')
    .option('-o, --output <file>', 'Output TypeScript file path')
    .parse(process.argv);

  const options = program.opts();

  if (!options.input || !options.output) {
    console.error('Error: --input and --output are required.');
    program.help();
    process.exit(1);
  }

  const inputFilePath = path.resolve(options.input);
  const outputFilePath = path.resolve(options.output);

  try {
    const interfaces = extractInterfaces(inputFilePath);
    let outputContent = "// Generated by ApocalypsAI Nightly TypeScript Type Guard Generator\n\n";

    // Include original interfaces in the output for completeness
    const originalCode = fs.readFileSync(inputFilePath, 'utf-8');
    outputContent += originalCode;
    outputContent += "\n";

    interfaces.forEach(iface => {
      outputContent += generateTypeGuard(iface);
      outputContent += "\n";
    });

    fs.writeFileSync(outputFilePath, outputContent);
    console.log(`Successfully generated type guards to ${outputFilePath}`);
  } catch (error: any) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

main();
