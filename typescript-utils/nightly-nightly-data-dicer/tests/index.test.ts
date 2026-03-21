import { DataDicer, DataItem } from '../src/index';

describe('DataDicer', () => {
  const sampleData: DataItem[] = [
    { id: 1, name: 'Alice', age: 30, city: 'New York', active: true },
    { id: 2, name: 'Bob', age: 24, city: 'London', active: false },
    { id: 3, name: 'Charlie', age: 35, city: 'New York', active: true },
    { id: 4, name: 'David', age: 28, city: 'Paris', active: false },
    { id: 5, name: 'Eve', age: 30, city: 'London', active: true },
  ];

  it('should initialize with data', () => {
    const dicer = new DataDicer(sampleData);
    expect(dicer.execute()).toEqual(sampleData);
  });

  it('should filter data correctly based on a predicate', () => {
    const dicer = new DataDicer(sampleData);
    const result = dicer.filter(item => item.age > 25).execute();
    expect(result).toEqual([
      { id: 1, name: 'Alice', age: 30, city: 'New York', active: true },
      { id: 3, name: 'Charlie', age: 35, city: 'New York', active: true },
      { id: 4, name: 'David', age: 28, city: 'Paris', active: false },
      { id: 5, name: 'Eve', age: 30, city: 'London', active: true },
    ]);
  });

  it('should sample data deterministically with a seed', () => {
    // # Mock rationale: Math.random is non-deterministic. The DataDicer class's `sample` method
    // uses an internal seeded pseudo-random number generator (PRNG) when a seed is provided.
    // This ensures that tests involving random sampling are deterministic and reproducible
    // without needing to mock the global Math.random, making the tests self-contained and reliable.
    const dicer1 = new DataDicer(sampleData);
    const result1 = dicer1.sample(2, 123).execute();

    const dicer2 = new DataDicer(sampleData);
    const result2 = dicer2.sample(2, 123).execute();

    expect(result1.length).toBe(2);
    expect(result1).toEqual(result2); // Should be the same due to seed
    expect(result1).not.toEqual(sampleData); // Should be a subset
  });

  it('should pick specified keys from items', () => {
    const dicer = new DataDicer(sampleData);
    const result = dicer.pick(['name', 'city']).execute();
    expect(result).toEqual([
      { name: 'Alice', city: 'New York' },
      { name: 'Bob', city: 'London' },
      { name: 'Charlie', city: 'New York' },
      { name: 'David', city: 'Paris' },
      { name: 'Eve', city: 'London' },
    ]);
  });

  it('should omit specified keys from items', () => {
    const dicer = new DataDicer(sampleData);
    const result = dicer.omit(['id', 'active']).execute();
    expect(result).toEqual([
      { name: 'Alice', age: 30, city: 'New York' },
      { name: 'Bob', age: 24, city: 'London' },
      { name: 'Charlie', age: 35, city: 'New York' },
      { name: 'David', age: 28, city: 'Paris' },
      { name: 'Eve', age: 30, city: 'London' },
    ]);
  });

  it('should sort data by a key in ascending order', () => {
    const dicer = new DataDicer(sampleData);
    const result = dicer.sort('age').execute();
    expect(result.map(item => item.age)).toEqual([24, 28, 30, 30, 35]);
    expect(result[0].name).toBe('Bob'); // Verify specific item order
  });

  it('should sort data by a key in descending order', () => {
    const dicer = new DataDicer(sampleData);
    const result = dicer.sort('age', false).execute();
    expect(result.map(item => item.age)).toEqual([35, 30, 30, 28, 24]);
    expect(result[0].name).toBe('Charlie'); // Verify specific item order
  });

  it('should handle chained operations correctly', () => {
    const dicer = new DataDicer(sampleData);
    const result = dicer
      .filter(item => item.city === 'New York')
      .sort('name', false) // Sort by name descending
      .pick(['name', 'age'])
      .execute();
    expect(result).toEqual([
      { name: 'Charlie', age: 35 },
      { name: 'Alice', age: 30 },
    ]);
  });

  it('should handle empty initial data gracefully', () => {
    const dicer = new DataDicer([]);
    expect(dicer.filter(() => true).sample(1).pick(['id']).execute()).toEqual([]);
  });

  it('should handle sampling more items than available by returning all items', () => {
    const smallData = sampleData.slice(0, 2); // Only 2 items
    const dicer = new DataDicer(smallData);
    const result = dicer.sample(5).execute(); // Try to sample 5
    expect(result.length).toBe(2);
    expect(result).toEqual(expect.arrayContaining(smallData));
  });

  it('should handle picking non-existent keys gracefully', () => {
    const dicer = new DataDicer(sampleData);
    const result = dicer.pick(['name', 'nonExistentKey'] as (keyof DataItem)[]).execute();
    expect(result).toEqual([
      { name: 'Alice' },
      { name: 'Bob' },
      { name: 'Charlie' },
      { name: 'David' },
      { name: 'Eve' }
    ]);
  });

  it('should handle omitting non-existent keys gracefully', () => {
    const dicer = new DataDicer(sampleData);
    const result = dicer.omit(['id', 'anotherNonExistentKey'] as (keyof DataItem)[]).execute();
    expect(result).toEqual([
      { name: 'Alice', age: 30, city: 'New York', active: true },
      { name: 'Bob', age: 24, city: 'London', active: false },
      { name: 'Charlie', age: 35, city: 'New York', active: true },
      { name: 'David', age: 28, city: 'Paris', active: false },
      { name: 'Eve', age: 30, city: 'London', active: true }
    ]);
  });
});
