import * as ts from 'typescript';
import * as fs from 'fs';
import * as path from 'path';

interface InterfaceInfo {
  name: string;
  properties: ts.PropertySignature[];
}

function parseInterfaces(filePath: string): InterfaceInfo[] {
  const program = ts.createProgram([filePath], {});
  const sourceFile = program.getSourceFile(filePath);
  if (!sourceFile) {
    throw new Error(`Could not find source file: ${filePath}`);
  }

  const interfaces: InterfaceInfo[] = [];

  function visit(node: ts.Node) {
    if (ts.isInterfaceDeclaration(node)) {
      interfaces.push({
        name: node.name.text,
        properties: node.members.filter(ts.isPropertySignature) as ts.PropertySignature[],
      });
    }
    ts.forEachChild(node, visit);
  }

  ts.forEachChild(sourceFile, visit);
  return interfaces;
}

function generateTypeGuard(interfaceInfo: InterfaceInfo): string {
  const { name, properties } = interfaceInfo;

  const propertyChecks = properties.map(prop => {
    const propName = prop.name.getText();
    const type = prop.type;
    let typeCheck: string;

    if (!type) {
      // Handle cases where type is not explicitly defined (e.g., any)
      typeCheck = `typeof obj.${propName} !== 'undefined'`;
    } else if (ts.isKeywordTypeNode(type) && type.kind === ts.SyntaxKind.StringKeyword) {
      typeCheck = `typeof obj.${propName} === 'string'`;
    } else if (ts.isKeywordTypeNode(type) && type.kind === ts.SyntaxKind.NumberKeyword) {
      typeCheck = `typeof obj.${propName} === 'number'`;
    } else if (ts.isKeywordTypeNode(type) && type.kind === ts.SyntaxKind.BooleanKeyword) {
      typeCheck = `typeof obj.${propName} === 'boolean'`;
    } else if (ts.isUnionTypeNode(type)) {
      // Handle union types, e.g., string | undefined
      const types = type.types.map(t => {
        if (ts.isKeywordTypeNode(t) && t.kind === ts.SyntaxKind.UndefinedKeyword) {
          return `typeof obj.${propName} === 'undefined'`;
        } else if (ts.isKeywordTypeTypeNode(t) && t.kind === ts.SyntaxKind.StringKeyword) {
          return `typeof obj.${propName} === 'string'`;
        } else if (ts.isKeywordTypeTypeNode(t) && t.kind === ts.SyntaxKind.NumberKeyword) {
          return `typeof obj.${propName} === 'number'`;
        } else if (ts.isKeywordTypeTypeNode(t) && t.kind === ts.SyntaxKind.BooleanKeyword) {
          return `typeof obj.${propName} === 'boolean'`;
        }
        return 'true'; // Fallback for complex types
      });
      typeCheck = types.join(' || ');
    } else {
      // Fallback for other types (e.g., custom interfaces, arrays, objects)
      // This is a simplification; more complex type checking would be needed for full coverage.
      typeCheck = `typeof obj.${propName} !== 'undefined'`;
    }

    // Check if the property is optional
    const isOptional = prop.questionToken !== undefined;
    if (isOptional) {
      return `(${typeCheck} || typeof obj.${propName} === 'undefined')`;
    } else {
      return `(${typeCheck})`;
    }
  });

  const guardBody = [
    `typeof obj === 'object' &&`, 
    `obj !== null &&`, 
    ...propertyChecks.map(check => `  ${check} &&`)
  ].join('\n');

  // Remove the last '&&' and trailing newline
  const cleanedGuardBody = guardBody.replace(/&&\n$/g, '').replace(/\n  \(true\) &&/g, '').replace(/\n  typeof obj\..* === 'undefined' &&/g, '');

  return `
export function is${name}(obj: any): obj is ${name} {
  return (
${cleanedGuardBody}
  );
}
`;
}

function main() {
  const args = process.argv.slice(2);
  let inputFilePath: string | undefined;
  let outputFilePath: string | undefined;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--input' && i + 1 < args.length) {
      inputFilePath = args[i + 1];
    } else if (args[i] === '--output' && i + 1 < args.length) {
      outputFilePath = args[i + 1];
    }
  }

  if (!inputFilePath) {
    console.error('Error: --input file path is required.');
    process.exit(1);
  }

  const absoluteInputPath = path.resolve(inputFilePath);

  try {
    const interfaces = parseInterfaces(absoluteInputPath);
    let generatedCode = '';
    for (const iface of interfaces) {
      generatedCode += generateTypeGuard(iface);
    }

    if (outputFilePath) {
      const absoluteOutputPath = path.resolve(outputFilePath);
      fs.writeFileSync(absoluteOutputPath, generatedCode);
      console.log(`Type guards generated successfully and saved to ${absoluteOutputPath}`);
    } else {
      console.log(generatedCode);
    }
  } catch (error: any) {
    console.error(`Error generating type guards: ${error.message}`);
    process.exit(1);
  }
}

main();
