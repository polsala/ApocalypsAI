import { generateTypeGuards } from '../src/main';

// Mock interfaces for testing
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

interface Admin {
  id: number;
  role: string;
}

interface Guest {
  id: number;
  username: string;
}

describe('generateTypeGuards', () => {
  // Mock rationale: We are mocking the interfaces and the `generateTypeGuards` function's
  // internal schema inference logic because directly inspecting TypeScript types at
  // runtime is not feasible without a TS compiler API or similar tools. The tests
  // focus on verifying that the *generated* guard functions behave as expected given
  // a simulated schema inference.

  it('should generate a type guard for a single interface', () => {
    const { isUser } = generateTypeGuards<User>();

    expect(isUser({ id: 1, name: 'Alice' })).toBe(true);
    expect(isUser({ id: 2, name: 'Bob', email: 'bob@example.com' })).toBe(true);
    expect(isUser({ id: 3 })).toBe(false); // Missing name
    expect(isUser({ name: 'Charlie' })).toBe(false); // Missing id
    expect(isUser({ id: 4, name: 'David', email: 123 })).toBe(false); // Incorrect email type
    expect(isUser({})).toBe(false);
    expect(isUser(null)).toBe(false);
    expect(isUser(undefined)).toBe(false);
    expect(isUser('not an object')).toBe(false);
  });

  it('should generate type guards for multiple interfaces', () => {
    const { isUser, isProduct } = generateTypeGuards<User, Product>();

    // Test User guards
    expect(isUser({ id: 1, name: 'Alice' })).toBe(true);
    expect(isProduct({ sku: 'XYZ', price: 100, description: 'Gadget' })).toBe(true);

    // Test mixed data
    expect(isUser({ sku: 'ABC', price: 50, description: 'Widget' })).toBe(false);
    expect(isProduct({ id: 5, name: 'Eve' })).toBe(false);
  });

  it('should handle optional properties correctly', () => {
    const { isUser } = generateTypeGuards<User>();

    expect(isUser({ id: 1, name: 'Alice' })).toBe(true); // email is optional
    expect(isUser({ id: 2, name: 'Bob', email: 'bob@example.com' })).toBe(true);
  });

  it('should generate guards for up to 5 interfaces', () => {
    const { isUser, isProduct, isAdmin, isGuest } = generateTypeGuards<User, Product, Admin, Guest>();

    expect(isUser({ id: 1, name: 'Alice' })).toBe(true);
    expect(isProduct({ sku: 'XYZ', price: 100, description: 'Gadget' })).toBe(true);
    expect(isAdmin({ id: 10, role: 'superadmin' })).toBe(true);
    expect(isGuest({ id: 20, username: 'testuser' })).toBe(true);

    // Test a non-matching type
    expect(isUser({ id: 30, role: 'user' })).toBe(false);
  });

  it('should return an empty object if no valid interfaces are provided (or inferable)', () => {
    // This test case is tricky because `generateTypeGuards` expects at least one generic type.
    // If we pass something that `inferSchema` cannot handle, it should result in no guards.
    // For this mock, `inferSchema` returns {} for unknown types.
    const result = generateTypeGuards<any>(); // Using 'any' to simulate an uninferable type
    expect(result).toEqual({});
  });
});
