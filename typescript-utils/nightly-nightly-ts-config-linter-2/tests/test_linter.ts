import { lintConfig } from '../src/linter';
import { ConfigRule } from '../src/types';

describe('lintConfig', () => {
  // Mock rationale: These tests are deterministic and do not rely on external services or complex setups.
  // They directly test the logic of the lintConfig function with predefined inputs.

  const mockConfig = {
    database: {
      host: 'localhost',
      port: 5432,
      user: 'admin',
      ssl: false
    },
    logging: {
      level: 'info',
      file: '/var/log/app.log'
    },
    features: {
      newUI: true,
      betaAccess: false
    }
  };

  it('should return no errors for a valid configuration', () => {
    const rules: ConfigRule[] = [
      {
        path: 'database.host',
        description: 'Database host must be a string',
        validator: (value: any) => typeof value === 'string'
      },
      {
        path: 'database.port',
        description: 'Database port must be a number',
        validator: (value: any) => typeof value === 'number'
      },
      {
        path: 'logging.level',
        description: 'Logging level must be one of [debug, info, warn, error]',
        validator: (value: any) => ['debug', 'info', 'warn', 'error'].includes(value)
      }
    ];
    const errors = lintConfig(mockConfig, rules);
    expect(errors).toEqual([]);
  });

  it('should return errors for invalid string values', () => {
    const invalidConfig = { ...mockConfig, database: { ...mockConfig.database, host: '' } };
    const rules: ConfigRule[] = [
      {
        path: 'database.host',
        description: 'Database host cannot be empty',
        validator: (value: any) => typeof value === 'string' && value.length > 0
      }
    ];
    const errors = lintConfig(invalidConfig, rules);
    expect(errors).toEqual([
      { path: 'database.host', message: 'Database host cannot be empty' }
    ]);
  });

  it('should return errors for invalid number values', () => {
    const invalidConfig = { ...mockConfig, database: { ...mockConfig.database, port: 'not-a-number' } };
    const rules: ConfigRule[] = [
      {
        path: 'database.port',
        description: 'Database port must be a number',
        validator: (value: any) => typeof value === 'number'
      }
    ];
    const errors = lintConfig(invalidConfig, rules);
    expect(errors).toEqual([
      { path: 'database.port', message: 'Database port must be a number' }
    ]);
  });

  it('should return errors for invalid enum values', () => {
    const invalidConfig = { ...mockConfig, logging: { ...mockConfig.logging, level: 'verbose' } };
    const rules: ConfigRule[] = [
      {
        path: 'logging.level',
        description: 'Logging level must be one of [debug, info, warn, error]',
        validator: (value: any) => ['debug', 'info', 'warn', 'error'].includes(value)
      }
    ];
    const errors = lintConfig(invalidConfig, rules);
    expect(errors).toEqual([
      { path: 'logging.level', message: 'Logging level must be one of [debug, info, warn, error]' }
    ]);
  });

  it('should handle nested paths correctly', () => {
    const rules: ConfigRule[] = [
      {
        path: 'features.newUI',
        description: 'New UI feature should be a boolean',
        validator: (value: any) => typeof value === 'boolean'
      }
    ];
    const errors = lintConfig(mockConfig, rules);
    expect(errors).toEqual([]);
  });

  it('should not report errors for missing optional paths', () => {
    const rules: ConfigRule[] = [
      {
        path: 'database.password',
        description: 'Database password should be a string',
        validator: (value: any) => typeof value === 'string'
      }
    ];
    // The 'password' path does not exist in mockConfig, so no error should be reported by default.
    const errors = lintConfig(mockConfig, rules);
    expect(errors).toEqual([]);
  });

  it('should report multiple errors', () => {
    const invalidConfig = {
      database: { host: '', port: 'invalid' },
      logging: { level: 'verbose' }
    };
    const rules: ConfigRule[] = [
      {
        path: 'database.host',
        description: 'Database host cannot be empty',
        validator: (value: any) => typeof value === 'string' && value.length > 0
      },
      {
        path: 'database.port',
        description: 'Database port must be a number',
        validator: (value: any) => typeof value === 'number'
      },
      {
        path: 'logging.level',
        description: 'Logging level must be one of [debug, info, warn, error]',
        validator: (value: any) => ['debug', 'info', 'warn', 'error'].includes(value)
      }
    ];
    const errors = lintConfig(invalidConfig, rules);
    expect(errors).toEqual([
      { path: 'database.host', message: 'Database host cannot be empty' },
      { path: 'database.port', message: 'Database port must be a number' },
      { path: 'logging.level', message: 'Logging level must be one of [debug, info, warn, error]' }
    ]);
  });
});
