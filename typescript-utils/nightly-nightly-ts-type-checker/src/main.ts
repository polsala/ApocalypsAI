import * as ts from 'typescript';
import * as fs from 'fs';
import * as path from 'path';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

function validateJsonAgainstSchema(jsonData: any, schemaInterfaceName: string, program: ts.Program): ValidationResult {
  const checker = program.getTypeChecker();
  const sourceFile = program.getSourceFile(program.getRootFileNames()[0]); // Assuming schema file is the root

  if (!sourceFile) {
    return { isValid: false, errors: ['Could not load schema source file.'] };
  }

  let schemaType: ts.Type | undefined;

  function visit(node: ts.Node) {
    if (ts.isInterfaceDeclaration(node) && node.name.text === schemaInterfaceName) {
      schemaType = checker.getTypeAtLocation(node);
    }
    ts.forEachChild(node, visit);
  }

  ts.forEachChild(sourceFile, visit);

  if (!schemaType) {
    return { isValid: false, errors: [`Interface '${schemaInterfaceName}' not found in schema file.`] };
  }

  const errors: string[] = [];

  function checkType(data: any, type: ts.Type, path: string = ''): void {
    if (type.flags & ts.TypeFlags.String) {
      if (typeof data !== 'string') {
        errors.push(`At path '${path}': Expected string, got ${typeof data}.`);
      }
    } else if (type.flags & ts.TypeFlags.Number) {
      if (typeof data !== 'number') {
        errors.push(`At path '${path}': Expected number, got ${typeof data}.`);
      }
    } else if (type.flags & ts.TypeFlags.Boolean) {
      if (typeof data !== 'boolean') {
        errors.push(`At path '${path}': Expected boolean, got ${typeof data}.`);
      }
    } else if (type.flags & ts.TypeFlags.Object) {
      if (typeof data !== 'object' || data === null || Array.isArray(data)) {
        errors.push(`At path '${path}': Expected object, got ${typeof data}.`);
        return;
      }
      const properties = checker.getPropertiesOfType(type);
      const dataKeys = Object.keys(data);

      // Check for missing required properties
      for (const prop of properties) {
        const propName = prop.name;
        const propType = checker.getTypeOfSymbolAtLocation(prop, prop.valueDeclaration! as ts.Declaration);
        const isOptional = (prop.flags & ts.SymbolFlags.Optional) !== 0;
        const fullPath = path ? `${path}.${propName}` : propName;

        if (!isOptional && !dataKeys.includes(propName)) {
          errors.push(`Property '${fullPath}' is missing.`);
        }
      }

      // Check existing properties against schema
      for (const key in data) {
        const propSymbol = checker.getSymbolAtLocation(ts.factory.createIdentifier(key));
        if (propSymbol) {
          const propType = checker.getTypeOfSymbolAtLocation(propSymbol, propSymbol.valueDeclaration! as ts.Declaration);
          const fullPath = path ? `${path}.${key}` : key;
          checkType(data[key], propType, fullPath);
        } else {
          // Property exists in data but not in schema (can be ignored or flagged depending on strictness)
          // For now, we'll ignore unknown properties to be more lenient.
        }
      }
    } else if (type.flags & ts.TypeFlags.StringLiteral) {
      const literalValue = (type as ts.StringLiteralType).value;
      if (data !== literalValue) {
        errors.push(`At path '${path}': Expected literal string "${literalValue}", got "${data}".`);
      }
    } else if (type.flags & ts.TypeFlags.BooleanLiteral) {
      const literalValue = (type as ts.BooleanLiteralType).intrinsicName === 'true';
      if (data !== literalValue) {
        errors.push(`At path '${path}': Expected boolean literal ${literalValue}, got ${data}.`);
      }
    } else if (type.isUnion()) {
      let matched = false;
      for (const unionType of type.types) {
        const tempErrors = [...errors]; // Capture errors for this branch
        checkType(data, unionType, path);
        if (errors.length === tempErrors.length) { // If no new errors were added, this branch is valid
          matched = true;
          break;
        }
        errors.splice(tempErrors.length); // Backtrack errors if this branch failed
      }
      if (!matched) {
        errors.push(`At path '${path}': Data does not match any union types.`);
      }
    } else if (type.isIntersection()) {
      for (const intersectionType of type.types) {
        checkType(data, intersectionType, path);
      }
    } else if (type.isArray()) {
      if (!Array.isArray(data)) {
        errors.push(`At path '${path}': Expected array, got ${typeof data}.`);
        return;
      }
      const elementType = checker.getElementTypeOfArrayType(type as ts.TypeReference);
      for (let i = 0; i < data.length; i++) {
        checkType(data[i], elementType, `${path}[${i}]`);
      }
    } else {
      // Fallback for other types like 'any', 'unknown', etc.
      // For simplicity, we'll assume they are valid if they exist.
    }
  }

  checkType(jsonData, schemaType);

  return {
    isValid: errors.length === 0,
    errors: errors,
  };
}

async function main() {
  const argv = await yargs(hideBin(process.argv))
    .option('schema', {
      alias: 's',
      type: 'string',
      description: 'Path to the TypeScript schema file',
      demandOption: true,
    })
    .option('data', {
      alias: 'd',
      type: 'string',
      description: 'Path to the JSON data file',
      demandOption: true,
    })
    .help()
    .argv;

  const schemaPath = path.resolve(argv.schema);
  const dataPath = path.resolve(argv.data);

  if (!fs.existsSync(schemaPath)) {
    console.error(`Error: Schema file not found at ${schemaPath}`);
    process.exit(1);
  }
  if (!fs.existsSync(dataPath)) {
    console.error(`Error: Data file not found at ${dataPath}`);
    process.exit(1);
  }

  try {
    const jsonData = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));

    // Compile the schema file to get a TypeScript Program
    const program = ts.createProgram([schemaPath], {
      target: ts.ScriptTarget.ESNext,
      module: ts.ModuleKind.CommonJS,
      strict: true,
      noEmit: true,
    });

    // Extract the interface name from the schema file path (e.g., 'schema.ts' -> 'Schema')
    const schemaFileName = path.basename(schemaPath, '.ts');
    const schemaInterfaceName = schemaFileName.charAt(0).toUpperCase() + schemaFileName.slice(1);

    const result = validateJsonAgainstSchema(jsonData, schemaInterfaceName, program);

    if (result.isValid) {
      console.log('Data is valid according to the schema.');
    } else {
      console.error('Validation failed:');
      result.errors.forEach(err => console.error(`- ${err}`));
      process.exit(1);
    }

  } catch (error: any) {
    console.error(`An error occurred: ${error.message}`);
    process.exit(1);
  }
}

main();
