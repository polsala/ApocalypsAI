import { classifyFile, FileMetadata, RelicCategory, RelicConfig } from '../src/relicClassifier';

describe('classifyFile', () => {
  const now = new Date();
  const defaultAncientDays = 365;
  const defaultForgottenDays = 90;
  const defaultMinSizeKB = 0;

  const defaultConfig: RelicConfig = {
    ancientDays: defaultAncientDays,
    forgottenDays: defaultForgottenDays,
    minSizeKB: defaultMinSizeKB,
  };

  // Helper to create a date N days ago
  const daysAgo = (days: number) => new Date(now.getTime() - days * 24 * 60 * 60 * 1000);

  it('should classify a very old, untouched file as Ancient Relic', () => {
    const metadata: FileMetadata = {
      path: '/test/ancient.txt',
      size: 10000, // 10 KB
      createdAt: daysAgo(400),
      modifiedAt: daysAgo(400),
      accessedAt: daysAgo(400),
      isDirectory: false,
    };
    const result = classifyFile(metadata, defaultConfig);
    expect(result.category).toBe(RelicCategory.AncientRelic);
    expect(result.reason).toContain('File is very old (400 days) and has not been modified or accessed recently.');
  });

  it('should classify an old but recently accessed file as Forgotten Artifact', () => {
    const metadata: FileMetadata = {
      path: '/test/forgotten_accessed.doc',
      size: 50000,
      createdAt: daysAgo(150),
      modifiedAt: daysAgo(150),
      accessedAt: daysAgo(5),
      isDirectory: false,
    };
    const result = classifyFile(metadata, defaultConfig);
    expect(result.category).toBe(RelicCategory.ForgottenArtifact);
    expect(result.reason).toContain('File is old (150 days) but not ancient, and has not been modified or accessed recently.');
  });

  it('should classify an old but recently modified file as Forgotten Artifact', () => {
    const metadata: FileMetadata = {
      path: '/test/forgotten_modified.xls',
      size: 70000,
      createdAt: daysAgo(150),
      modifiedAt: daysAgo(5),
      accessedAt: daysAgo(150),
      isDirectory: false,
    };
    const result = classifyFile(metadata, defaultConfig);
    expect(result.category).toBe(RelicCategory.ForgottenArtifact);
    expect(result.reason).toContain('File is old (150 days) but not ancient, and has not been modified or accessed recently.');
  });

  it('should classify a relatively new, inactive file as Recent Find', () => {
    const metadata: FileMetadata = {
      path: '/test/recent_inactive.jpg',
      size: 20000,
      createdAt: daysAgo(60),
      modifiedAt: daysAgo(60),
      accessedAt: daysAgo(60),
      isDirectory: false,
    };
    const result = classifyFile(metadata, defaultConfig);
    expect(result.category).toBe(RelicCategory.RecentFind);
    expect(result.reason).toContain('File is relatively new (60 days) but has not been actively modified or accessed in the last 30 days.');
  });

  it('should classify a recently active file as Active Data', () => {
    const metadata: FileMetadata = {
      path: '/test/active.js',
      size: 5000,
      createdAt: daysAgo(10),
      modifiedAt: daysAgo(2),
      accessedAt: daysAgo(1),
      isDirectory: false,
    };
    const result = classifyFile(metadata, defaultConfig);
    expect(result.category).toBe(RelicCategory.ActiveData);
    expect(result.reason).toContain('File is recent (10 days) and actively used.');
  });

  it('should classify a directory as Active Data (not a relic)', () => {
    const metadata: FileMetadata = {
      path: '/test/my_folder',
      size: 4096,
      createdAt: daysAgo(100),
      modifiedAt: daysAgo(50),
      accessedAt: daysAgo(10),
      isDirectory: true,
    };
    const result = classifyFile(metadata, defaultConfig);
    expect(result.category).toBe(RelicCategory.ActiveData);
    expect(result.reason).toContain('Is a directory, not classified as a relic.');
  });

  it('should ignore files smaller than minSizeKB threshold', () => {
    const configWithMinSize: RelicConfig = { ...defaultConfig, minSizeKB: 50 }; // 50 KB
    const metadata: FileMetadata = {
      path: '/test/small_file.log',
      size: 10 * 1024, // 10 KB
      createdAt: daysAgo(400),
      modifiedAt: daysAgo(400),
      accessedAt: daysAgo(400),
      isDirectory: false,
    };
    const result = classifyFile(metadata, configWithMinSize);
    expect(result.category).toBe(RelicCategory.ActiveData);
    expect(result.reason).toContain('File size (10.00 KB) is below minimum threshold (50 KB).');
  });

  it('should correctly apply custom ancientDays threshold', () => {
    const customConfig: RelicConfig = { ...defaultConfig, ancientDays: 100 };
    const metadata: FileMetadata = {
      path: '/test/custom_ancient.txt',
      size: 10000,
      createdAt: daysAgo(120),
      modifiedAt: daysAgo(120),
      accessedAt: daysAgo(120),
      isDirectory: false,
    };
    const result = classifyFile(metadata, customConfig);
    expect(result.category).toBe(RelicCategory.AncientRelic);
    expect(result.reason).toContain('File is very old (120 days) and has not been modified or accessed recently.');
  });

  it('should correctly apply custom forgottenDays threshold', () => {
    const customConfig: RelicConfig = { ...defaultConfig, forgottenDays: 30 };
    const metadata: FileMetadata = {
      path: '/test/custom_forgotten.txt',
      size: 10000,
      createdAt: daysAgo(45),
      modifiedAt: daysAgo(45),
      accessedAt: daysAgo(45),
      isDirectory: false,
    };
    const result = classifyFile(metadata, customConfig);
    expect(result.category).toBe(RelicCategory.ForgottenArtifact);
    expect(result.reason).toContain('File is old (45 days) but not ancient, and has not been modified or accessed recently.');
  });

  it('should handle edge case where age is exactly ancient threshold', () => {
    const metadata: FileMetadata = {
      path: '/test/edge_ancient.txt',
      size: 10000,
      createdAt: daysAgo(defaultAncientDays),
      modifiedAt: daysAgo(defaultAncientDays),
      accessedAt: daysAgo(defaultAncientDays),
      isDirectory: false,
    };
    const result = classifyFile(metadata, defaultConfig);
    expect(result.category).toBe(RelicCategory.AncientRelic);
  });

  it('should handle edge case where age is exactly forgotten threshold', () => {
    const metadata: FileMetadata = {
      path: '/test/edge_forgotten.txt',
      size: 10000,
      createdAt: daysAgo(defaultForgottenDays),
      modifiedAt: daysAgo(defaultForgottenDays),
      accessedAt: daysAgo(defaultForgottenDays),
      isDirectory: false,
    };
    const result = classifyFile(metadata, defaultConfig);
    expect(result.category).toBe(RelicCategory.ForgottenArtifact);
  });
});
