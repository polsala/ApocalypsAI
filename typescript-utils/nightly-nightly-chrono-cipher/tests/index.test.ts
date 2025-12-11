import { encryptMessage, decryptMessage, xorCipher, generateTimeKey } from '../src/index';
import { ChronoMessage } from '../src/index';

/**
 * Mock Date to control time in tests
 */
class MockDate extends Date {
  static now(): number {
    return new Date('2024-12-01T12:00:00Z').getTime();
  }
  
  constructor(date?: any) {
    if (date) {
      super(date);
    } else {
      super('2024-12-01T12:00:00Z');
    }
  }
}

// Mock the Date constructor
(global as any).Date = MockDate;

/**
 * Test suite for Chrono Cipher
 */
describe('Nightly Chrono Cipher', () => {
  describe('xorCipher', () => {
    test('should encrypt and decrypt correctly', () => {
      const message = 'Hello, World!';
      const key = 'test-key-123';
      
      const encrypted = xorCipher(message, key);
      const decrypted = xorCipher(encrypted, key);
      
      expect(decrypted).toBe(message);
    });
    
    test('should handle empty strings', () => {
      const message = '';
      const key = 'test-key';
      
      const encrypted = xorCipher(message, key);
      const decrypted = xorCipher(encrypted, key);
      
      expect(decrypted).toBe(message);
    });
    
    test('should handle special characters', () => {
      const message = 'Special chars: !@#$%^&*()_+-=[]{}|;:,.<>?';
      const key = 'special-key';
      
      const encrypted = xorCipher(message, key);
      const decrypted = xorCipher(encrypted, key);
      
      expect(decrypted).toBe(message);
    });
  });
  
  describe('generateTimeKey', () => {
    test('should generate consistent keys for same timestamp', () => {
      const time1 = new Date('2024-12-25T15:30:00Z');
      const time2 = new Date('2024-12-25T15:30:00Z');
      
      const key1 = generateTimeKey(time1);
      const key2 = generateTimeKey(time2);
      
      expect(key1).toBe(key2);
      expect(key1.length).toBe(32);
    });
    
    test('should generate different keys for different timestamps', () => {
      const time1 = new Date('2024-12-25T15:30:00Z');
      const time2 = new Date('2024-12-25T15:31:00Z');
      
      const key1 = generateTimeKey(time1);
      const key2 = generateTimeKey(time2);
      
      expect(key1).not.toBe(key2);
    });
  });
  
  describe('encryptMessage', () => {
    test('should encrypt message with exact time', () => {
      const message = 'Secret message';
      const time = new Date('2024-12-25T15:30:00Z');
      
      const encrypted = encryptMessage(message, time, time);
      
      // Should be base64 encoded JSON
      const decoded = Buffer.from(encrypted, 'base64').toString('utf8');
      const chronoMessage: ChronoMessage = JSON.parse(decoded);
      
      expect(chronoMessage.version).toBe('1.0');
      expect(chronoMessage.startTime).toBe(time.toISOString());
      expect(chronoMessage.endTime).toBe(time.toISOString());
      expect(chronoMessage.encryptedData).toBeDefined();
      expect(typeof chronoMessage.encryptedData).toBe('string');
    });
    
    test('should encrypt message with time window', () => {
      const message = 'Window message';
      const start = new Date('2024-12-25T09:00:00Z');
      const end = new Date('2024-12-25T17:00:00Z');
      
      const encrypted = encryptMessage(message, start, end);
      
      const decoded = Buffer.from(encrypted, 'base64').toString('utf8');
      const chronoMessage: ChronoMessage = JSON.parse(decoded);
      
      expect(chronoMessage.startTime).toBe(start.toISOString());
      expect(chronoMessage.endTime).toBe(end.toISOString());
    });
    
    test('should throw error if start time is after end time', () => {
      const message = 'Test message';
      const start = new Date('2024-12-25T17:00:00Z');
      const end = new Date('2024-12-25T09:00:00Z');
      
      expect(() => {
        encryptMessage(message, start, end);
      }).toThrow('Start time must be before end time');
    });
    
    test('should throw error if start time is in the past', () => {
      const message = 'Test message';
      const start = new Date('2024-11-30T12:00:00Z'); // Before mock date
      const end = new Date('2024-12-25T17:00:00Z');
      
      expect(() => {
        encryptMessage(message, start, end);
      }).toThrow('Start time must be in the future');
    });
  });
  
  describe('decryptMessage', () => {
    test('should decrypt message successfully within time window', () => {
      const message = 'Secret Santa plans';
      const start = new Date('2024-12-25T15:30:00Z');
      const end = new Date('2024-12-25T15:30:00Z');
      
      const encrypted = encryptMessage(message, start, end);
      const decrypted = decryptMessage(encrypted);
      
      expect(decrypted).toBe(message);
    });
    
    test('should decrypt message within time window', () => {
      const message = 'Window message';
      const start = new Date('2024-12-25T09:00:00Z');
      const end = new Date('2024-12-25T17:00:00Z');
      
      const encrypted = encryptMessage(message, start, end);
      const decrypted = decryptMessage(encrypted);
      
      expect(decrypted).toBe(message);
    });
    
    test('should throw error if message is not yet valid', () => {
      const message = 'Future message';
      const start = new Date('2024-12-02T12:00:00Z'); // After mock date
      const end = new Date('2024-12-02T13:00:00Z');
      
      const encrypted = encryptMessage(message, start, end);
      
      expect(() => {
        decryptMessage(encrypted);
      }).toThrow('Message cannot be decrypted yet');
    });
    
    test('should throw error if message decryption window has expired', () => {
      const message = 'Expired message';
      const start = new Date('2024-11-30T12:00:00Z'); // Before mock date
      const end = new Date('2024-11-30T13:00:00Z');
      
      const encrypted = encryptMessage(message, start, end);
      
      expect(() => {
        decryptMessage(encrypted);
      }).toThrow('Message decryption window has expired');
    });
    
    test('should throw error for invalid message format', () => {
      const invalidMessage = Buffer.from(JSON.stringify({ invalid: 'format' }), 'utf8').toString('base64');
      
      expect(() => {
        decryptMessage(invalidMessage);
      }).toThrow('Invalid encrypted message format');
    });
    
    test('should throw error for corrupted message', () => {
      const corruptedMessage = 'invalid-base64-string!@#$%';
      
      expect(() => {
        decryptMessage(corruptedMessage);
      }).toThrow();
    });
  });
  
  describe('Integration tests', () => {
    test('should handle complex message with emojis', () => {
      const message = '🎉 Secret launch details: Project Phoenix takes off at midnight! 🚀 #Confidential';
      const start = new Date('2024-12-31T23:59:00Z');
      const end = new Date('2025-01-01T00:01:00Z');
      
      const encrypted = encryptMessage(message, start, end);
      const decrypted = decryptMessage(encrypted);
      
      expect(decrypted).toBe(message);
    });
    
    test('should handle very long messages', () => {
      const message = 'A'.repeat(10000);
      const start = new Date('2024-12-25T15:30:00Z');
      const end = new Date('2024-12-25T15:30:00Z');
      
      const encrypted = encryptMessage(message, start, end);
      const decrypted = decryptMessage(encrypted);
      
      expect(decrypted).toBe(message);
    });
    
    test('should handle messages with newlines and tabs', () => {
      const message = 'Line 1\nLine 2\tTabbed content\nLine 3';
      const start = new Date('2024-12-25T15:30:00Z');
      const end = new Date('2024-12-25T15:30:00Z');
      
      const encrypted = encryptMessage(message, start, end);
      const decrypted = decryptMessage(encrypted);
      
      expect(decrypted).toBe(message);
    });
  });
});

// Mock rationale: We mock the Date constructor to ensure deterministic tests
// that don't depend on the actual system time. This allows us to test
// time-based functionality reliably in any environment.
