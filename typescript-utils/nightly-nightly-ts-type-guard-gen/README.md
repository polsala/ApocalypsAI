## Nightly TypeScript Type Guard Generator

This utility generates TypeScript type guard functions from provided interfaces. Type guards are essential for narrowing down types in TypeScript, especially when dealing with data from external sources (like API responses or user input) where the exact type might not be guaranteed.

### Why Use This?

- **Type Safety**: Ensures that you're working with the correct data types, preventing runtime errors.
- **Readability**: Generates clear and concise type guard functions.
- **Developer Productivity**: Automates the tedious process of writing repetitive type guard code.

### Usage

1.  **Define your TypeScript interfaces**: Create your data structures using TypeScript interfaces.

    ```typescript
    interface User {
      id: number;
      name: string;
      email?: string;
    }

    interface Product {
      sku: string;
      price: number;
      description: string;
    }
    ```

2.  **Run the generator**: Use the generated `generateTypeGuards` function, passing your interfaces as arguments.

    ```typescript
    import { generateTypeGuards } from './src/main';

    // Define your interfaces here or import them
    interface User {
      id: number;
      name: string;
      email?: string;
    }

    interface Product {
      sku: string;
      price: number;
      description: string;
    }

    // Generate type guards
    const { isUser, isProduct } = generateTypeGuards<User, Product>();

    // Example usage
    function processData(data: any) {
      if (isUser(data)) {
        console.log(`Processing user: ${data.name}`);
      } else if (isProduct(data)) {
        console.log(`Processing product: ${data.sku}`);
      } else {
        console.log('Unknown data type');
      }
    }

    processData({ id: 1, name: 'Alice' });
    processData({ sku: 'XYZ123', price: 99.99, description: 'A cool gadget' });
    processData({ invalid: true });
    ```

### How it Works

The `generateTypeGuards` function uses a factory pattern. It takes generic types representing your interfaces and dynamically creates functions that check for the presence and type of properties defined in those interfaces. It handles optional properties gracefully.

### Installation

This is a standalone utility. You can copy the `src/main.ts` file into your project or install it as a dependency if it were published.

### Testing

Unit tests are included to verify the functionality of the generated type guards. Run `npm install` and then `npm test` to execute them.
