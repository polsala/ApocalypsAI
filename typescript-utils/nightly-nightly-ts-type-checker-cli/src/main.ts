import { program } from 'commander';
import * as ts from 'typescript';
import * as fs from 'fs';
import * as path from 'path';

interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

function validateJsonAgainstInterface(jsonData: any, interfacePath: string): ValidationResult {
  const errors: string[] = [];
  let isValid = true;

  try {
    const program = ts.createProgram([interfacePath], { allowJs: true });
    const checker = program.getTypeChecker();
    const sourceFile = program.getSourceFile(path.resolve(interfacePath));

    if (!sourceFile) {
      return { isValid: false, errors: [`Could not find source file: ${interfacePath}`] };
    }

    let interfaceType: ts.Type | undefined;

    ts.forEachChild(sourceFile, (node) => {
      if (ts.isInterfaceDeclaration(node) && node.name.text === path.basename(interfacePath).replace('.ts', '')) {
        const symbol = checker.getSymbolAtLocation(node.name);
        if (symbol) {
          interfaceType = checker.getTypeOfSymbolAtLocation(symbol, node.name);
        }
      }
    });

    if (!interfaceType) {
      return { isValid: false, errors: [`Interface not found in ${interfacePath}. Ensure the interface name matches the filename (e.g., UserInterface for UserInterface.ts).`] };
    }

    // Basic validation: check if all required properties exist and have compatible types
    // This is a simplified check. A full type checker would be much more complex.
    // For this utility, we'll focus on property existence and basic type compatibility.

    const interfaceProperties = checker.getPropertiesOfType(interfaceType);

    for (const prop of interfaceProperties) {
      const propName = prop.name;
      const propType = checker.getTypeOfSymbol(prop);
      const isOptional = prop.flags & ts.SymbolFlags.Optional;

      if (!jsonData.hasOwnProperty(propName)) {
        if (!isOptional) {
          errors.push(`Missing required property: '${propName}'`);
          isValid = false;
        }
      } else {
        // Basic type checking (e.g., number, string, boolean)
        const jsonValue = jsonData[propName];
        const jsonValueType = typeof jsonValue;

        if (propType.flags & ts.TypeFlags.Number && jsonValueType !== 'number') {
          errors.push(`Property '${propName}' expected type 'number', but got '${jsonValueType}'`);
          isValid = false;
        } else if (propType.flags & ts.TypeFlags.String && jsonValueType !== 'string') {
          errors.push(`Property '${propName}' expected type 'string', but got '${jsonValueType}'`);
          isValid = false;
        } else if (propType.flags & ts.TypeFlags.Boolean && jsonValueType !== 'boolean') {
          errors.push(`Property '${propName}' expected type 'boolean', but got '${jsonValueType}'`);
          isValid = false;
        } else if (propType.flags & ts.TypeFlags.Object && jsonValueType !== 'object') {
          // This is a very basic check for objects, doesn't handle nested types well.
          // For more complex scenarios, a dedicated JSON schema validator or more advanced TS reflection would be needed.
          errors.push(`Property '${propName}' expected type 'object', but got '${jsonValueType}'`);
          isValid = false;
        }
      }
    }

    // Check for extra properties in JSON that are not in the interface
    for (const key in jsonData) {
      if (jsonData.hasOwnProperty(key)) {
        const jsonPropSymbol = checker.getSymbolAtLocation(ts.createIdentifier(key));
        if (!jsonPropSymbol || !interfaceProperties.some(p => p.name === key)) {
          errors.push(`Unexpected property found: '${key}'`);
          isValid = false;
        }
      }
    }

  } catch (e: any) {
    errors.push(`Error during validation: ${e.message}`);
    isValid = false;
  }

  return { isValid, errors };
}

program
  .version('1.0.0')
  .description('Validate JSON data against a TypeScript interface.')
  .requiredOption('-i, --interface-file <file>', 'Path to the TypeScript interface file (e.g., UserInterface.ts)')
  .requiredOption('-d, --data-file <file>', 'Path to the JSON data file')
  .parse(process.argv);

const options = program.opts();

const interfaceFilePath = path.resolve(options.interfaceFile);
const dataFilePath = path.resolve(options.dataFile);

if (!fs.existsSync(interfaceFilePath)) {
  console.error(`Error: Interface file not found at ${interfaceFilePath}`);
  process.exit(1);
}

if (!fs.existsSync(dataFilePath)) {
  console.error(`Error: Data file not found at ${dataFilePath}`);
  process.exit(1);
}

try {
  const interfaceContent = fs.readFileSync(interfaceFilePath, 'utf-8');
  const dataContent = fs.readFileSync(dataFilePath, 'utf-8');
  const jsonData = JSON.parse(dataContent);

  // Dynamically create a temporary TS file to allow ts.createProgram to resolve imports if needed
  // and to ensure the interface name is correctly inferred from the filename.
  const tempInterfaceFileName = `TempInterface_${Date.now()}.ts`;
  const tempInterfacePath = path.join(process.cwd(), tempInterfaceFileName);
  fs.writeFileSync(tempInterfacePath, interfaceContent);

  const validationResult = validateJsonAgainstInterface(jsonData, tempInterfacePath);

  if (!validationResult.isValid) {
    console.error('JSON validation failed:');
    validationResult.errors.forEach(err => console.error(`- ${err}`));
    process.exit(1);
  } else {
    console.log('JSON data is valid according to the TypeScript interface.');
    process.exit(0);
  }

} catch (error: any) {
  console.error(`An unexpected error occurred: ${error.message}`);
  process.exit(1);
} finally {
  // Clean up the temporary file
  if (fs.existsSync(path.join(process.cwd(), `TempInterface_${Date.now()}.ts`))) {
    fs.unlinkSync(path.join(process.cwd(), `TempInterface_${Date.now()}.ts`));
  }
}
