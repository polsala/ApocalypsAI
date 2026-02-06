import { validateAndMendManifest, defaultManifestSchema } from '../src/mender';
import { Manifest } from '../src/manifestTypes';

describe('validateAndMendManifest', () => {
  // Mock rationale: All tests operate on in-memory JavaScript objects for manifests and schemas.
  // No file system access or external network calls are made, ensuring determinism and offline execution.

  // --- Schema Validation Tests ---

  test('should return isValid true for a valid manifest', () => {
    const manifest: Manifest = {
      items: [
        { name: 'Water Filter', quantity: 1, category: 'Hydration' },
        { name: 'Canned Beans', quantity: 10, category: 'Food' }
      ],
      location: 'Safehouse Alpha',
      lastUpdated: '2024-07-20T12:00:00Z'
    };
    const result = validateAndMendManifest(manifest);
    expect(result.isValid).toBe(true);
    expect(result.errors).toBeNull();
  });

  test('should return isValid false for a manifest with missing required fields', () => {
    const manifest: Manifest = { items: [] }; // Missing 'name' and 'quantity' in items
    const result = validateAndMendManifest(manifest);
    expect(result.isValid).toBe(true); // Empty array is valid for 'items' itself

    const invalidManifest: any = { location: 'nowhere' }; // Missing 'items' array
    const invalidResult = validateAndMendManifest(invalidManifest);
    expect(invalidResult.isValid).toBe(false);
    expect(invalidResult.errors).not.toBeNull();
    expect(invalidResult.errors?.[0].message).toContain("must have required property 'items'");
  });

  test('should return isValid false for a manifest with incorrect data types', () => {
    const manifest: any = {
      items: [
        { name: 'Bandages', quantity: 'five', category: 'Medical' } // quantity should be number
      ]
    };
    const result = validateAndMendManifest(manifest);
    expect(result.isValid).toBe(false);
    expect(result.errors).not.toBeNull();
    expect(result.errors?.[0].message).toContain('must be number');
  });

  test('should return isValid false for a manifest with additional properties not allowed by default schema', () => {
    const manifest: any = {
      items: [
        { name: 'Water', quantity: 5 }
      ],
      secretStash: 'hidden'
    };
    const result = validateAndMendManifest(manifest);
    expect(result.isValid).toBe(false);
    expect(result.errors).not.toBeNull();
    expect(result.errors?.[0].message).toContain('must not have additional properties');
  });

  // --- Mending Suggestions Tests ---

  test('should suggest adding water if no water source is found (Critical)', () => {
    const manifest: Manifest = {
      items: [
        { name: 'Canned Food', quantity: 5 },
        { name: 'Matches', quantity: 1 }
      ]
    };
    const result = validateAndMendManifest(manifest);
    expect(result.suggestions).toContainEqual(expect.objectContaining({
      severity: 'critical',
      suggestion: expect.stringContaining('Add a reliable water source')
    }));
  });

  test('should not suggest adding water if water source is found', () => {
    const manifest: Manifest = {
      items: [
        { name: 'Bottled Water', quantity: 10 },
        { name: 'Water Purification Tablets', quantity: 20 }
      ]
    };
    const result = validateAndMendManifest(manifest);
    expect(result.suggestions).not.toContainEqual(expect.objectContaining({
      severity: 'critical',
      suggestion: expect.stringContaining('Add a reliable water source')
    }));
  });

  test('should suggest adding first aid if none is found (Warning)', () => {
    const manifest: Manifest = {
      items: [
        { name: 'Water', quantity: 5 }
      ]
    };
    const result = validateAndMendManifest(manifest);
    expect(result.suggestions).toContainEqual(expect.objectContaining({
      severity: 'warning',
      suggestion: expect.stringContaining('Ensure a comprehensive first aid kit')
    }));
  });

  test('should not suggest adding first aid if present', () => {
    const manifest: Manifest = {
      items: [
        { name: 'Basic First Aid Kit', quantity: 1, category: 'Medical' }
      ]
    };
    const result = validateAndMendManifest(manifest);
    expect(result.suggestions).not.toContainEqual(expect.objectContaining({
      severity: 'warning',
      suggestion: expect.stringContaining('Ensure a comprehensive first aid kit')
    }));
  });

  test('should suggest consolidating sharp tools if too many (Info)', () => {
    const manifest: Manifest = {
      items: [
        { name: 'Survival Knife', quantity: 1 },
        { name: 'Machete', quantity: 1 },
        { name: 'Utility Blade', quantity: 1 },
        { name: 'Water', quantity: 5 }
      ]
    };
    const result = validateAndMendManifest(manifest);
    expect(result.suggestions).toContainEqual(expect.objectContaining({
      severity: 'info',
      suggestion: expect.stringContaining('You have 3 sharp tools. Consider consolidating')
    }));
  });

  test('should not suggest consolidating sharp tools if few', () => {
    const manifest: Manifest = {
      items: [
        { name: 'Survival Knife', quantity: 1 },
        { name: 'Water', quantity: 5 }
      ]
    };
    const result = validateAndMendManifest(manifest);
    expect(result.suggestions).not.toContainEqual(expect.objectContaining({
      severity: 'info',
      suggestion: expect.stringContaining('Consolidate or diversifying your toolkit')
    }));
  });

  test('should suggest balancing luxury items if too many (Warning)', () => {
    const manifest: Manifest = {
      items: [
        { name: 'Chocolate Bar', quantity: 10 },
        { name: 'Gourmet Coffee', quantity: 5 },
        { name: 'Water', quantity: 2 }
      ]
    };
    const result = validateAndMendManifest(manifest);
    expect(result.suggestions).toContainEqual(expect.objectContaining({
      severity: 'warning',
      suggestion: expect.stringContaining('high proportion of luxury items')
    }));
  });

  test('should not suggest balancing luxury items if few', () => {
    const manifest: Manifest = {
      items: [
        { name: 'Canned Food', quantity: 20 },
        { name: 'Water', quantity: 10 },
        { name: 'Chocolate Bar', quantity: 1 }
      ]
    };
    const result = validateAndMendManifest(manifest);
    expect(result.suggestions).not.toContainEqual(expect.objectContaining({
      severity: 'warning',
      suggestion: expect.stringContaining('high proportion of luxury items')
    }));
  });

  test('should suggest removing expired items (Warning)', () => {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const manifest: Manifest = {
      items: [
        { name: 'Expired Ration Pack', quantity: 1, expiryDate: yesterday.toISOString().split('T')[0] },
        { name: 'Water', quantity: 5 }
      ]
    };
    const result = validateAndMendManifest(manifest);
    expect(result.suggestions).toContainEqual(expect.objectContaining({
      severity: 'warning',
      suggestion: expect.stringContaining('items have expired')
    }));
  });

  test('should not suggest removing items if none are expired', () => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const manifest: Manifest = {
      items: [
        { name: 'Fresh Ration Pack', quantity: 1, expiryDate: tomorrow.toISOString().split('T')[0] },
        { name: 'Water', quantity: 5 }
      ]
    };
    const result = validateAndMendManifest(manifest);
    expect(result.suggestions).not.toContainEqual(expect.objectContaining({
      severity: 'warning',
      suggestion: expect.stringContaining('items have expired')
    }));
  });

  test('should handle empty items array gracefully', () => {
    const manifest: Manifest = { items: [] };
    const result = validateAndMendManifest(manifest);
    expect(result.isValid).toBe(true);
    expect(result.suggestions).toContainEqual(expect.objectContaining({
      severity: 'critical',
      suggestion: expect.stringContaining('Add a reliable water source')
    }));
    expect(result.suggestions).toContainEqual(expect.objectContaining({
      severity: 'warning',
      suggestion: expect.stringContaining('Ensure a comprehensive first aid kit')
    }));
  });

  test('should use custom schema if provided', () => {
    const customSchema = {
      type: 'object',
      properties: {
        cacheName: { type: 'string' },
        items: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' } }, required: ['id'] } }
      },
      required: ['cacheName', 'items']
    };
    const manifest: any = {
      cacheName: 'My Secret Stash',
      items: [
        { id: 'item-123' }
      ]
    };
    const result = validateAndMendManifest(manifest, customSchema);
    expect(result.isValid).toBe(true);
    expect(result.errors).toBeNull();

    const invalidManifest: any = {
      items: [
        { id: 'item-123' }
      ]
    }; // Missing cacheName
    const invalidResult = validateAndMendManifest(invalidManifest, customSchema);
    expect(invalidResult.isValid).toBe(false);
    expect(invalidResult.errors).not.toBeNull();
    expect(invalidResult.errors?.[0].message).toContain("must have required property 'cacheName'");
  });
});
