## Nightly TypeScript Type Guard Generator

This utility generates TypeScript type guard functions from provided interfaces. This helps ensure type safety when dealing with data that might not conform to expected structures, especially when data comes from external sources like APIs or user input.

### Usage

1.  **Install Dependencies**: 
    ```bash
    npm install -g typescript
    ```

2.  **Create an Interface File**: Create a TypeScript file (e.g., `interfaces.ts`) containing your interfaces.

    ```typescript
    // interfaces.ts
    export interface UserProfile {
      id: number;
      username: string;
      email?: string;
      isActive: boolean;
    }

    export interface Product {
      sku: string;
      name: string;
      price: number;
      inStock: boolean;
    }
    ```

3.  **Run the Generator**: Execute the `ts-type-guard-gen` command, specifying the input interface file and an optional output file.

    ```bash
    ts-type-guard-gen --input interfaces.ts --output guards.ts
    ```

    If no output file is specified, the guards will be printed to the console.

### Generated Type Guards

The generated `guards.ts` file will contain functions like:

```typescript
// guards.ts

export function isUserProfile(obj: any): obj is UserProfile {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.id === 'number' &&
    typeof obj.username === 'string' &&
    (typeof obj.email === 'undefined' || typeof obj.email === 'string') &&
    typeof obj.isActive === 'boolean'
  );
}

export function isProduct(obj: any): obj is Product {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.sku === 'string' &&
    typeof obj.name === 'string' &&
    typeof obj.price === 'number' &&
    typeof obj.inStock === 'boolean'
  );
}
```

### Development

To run the tests locally:

```bash
npm install
npm test
```
