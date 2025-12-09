import { describe, it, expect } from '@jest/globals';
import { parseArgs, validateArgs } from '../../src/utils/args-parser';

/**
 * Tests for the argument parser utility.
 * 
 * These tests verify that command-line arguments are correctly
 * parsed and validated for the Quantum Entanglement Checker CLI.
 * 
 * Mock rationale: No external dependencies are mocked as this
 * is a pure utility function that operates on string arrays.
 */

describe('Args Parser', () => {
  describe('parseArgs', () => {
    it('should parse verify command with nodes and iterations', () => {
      const args = parseArgs(['verify', '--nodes', '5', '--iterations', '2000']);
      
      expect(args.command).toBe('verify');
      expect(args.nodes).toBe(5);
      expect(args.iterations).toBe(2000);
    });
    
    it('should parse bell command with state and measurements', () => {
      const args = parseArgs(['bell', '--state', '|00⟩ + |11⟩', '--measurements', '1000']);
      
      expect(args.command).toBe('bell');
      expect(args.state).toBe('|00⟩ + |11⟩');
      expect(args.measurements).toBe(1000);
    });
    
    it('should parse chsh command with trials', () => {
      const args = parseArgs(['chsh', '--trials', '5000']);
      
      expect(args.command).toBe('chsh');
      expect(args.trials).toBe(5000);
    });
    
    it('should parse network command with latency and packet loss', () => {
      const args = parseArgs(['network', '--latency', '100ms', '--packet-loss', '0.05']);
      
      expect(args.command).toBe('network');
      expect(args.latency).toBe(100);
      expect(args.packetLoss).toBe(0.05);
    });
    
    it('should handle latency with ms suffix', () => {
      const args = parseArgs(['--latency', '250ms']);
      expect(args.latency).toBe(250);
    });
    
    it('should handle packet loss as percentage', () => {
      const args = parseArgs(['--packet-loss', '10%']);
      expect(args.packetLoss).toBe(0.1);
    });
    
    it('should handle packet loss as decimal', () => {
      const args = parseArgs(['--packet-loss', '0.15']);
      expect(args.packetLoss).toBe(0.15);
    });
    
    it('should set default values when no arguments provided', () => {
      const args = parseArgs([]);
      
      expect(args.command).toBe('help');
      expect(args.nodes).toBe(3);
      expect(args.iterations).toBe(1000);
      expect(args.measurements).toBe(500);
      expect(args.trials).toBe(10000);
      expect(args.latency).toBe(50);
      expect(args.packetLoss).toBe(0.01);
    });
    
    it('should handle help flags', () => {
      const args1 = parseArgs(['--help']);
      const args2 = parseArgs(['-h']);
      
      expect(args1.command).toBe('help');
      expect(args2.command).toBe('help');
    });
  });
  
  describe('validateArgs', () => {
    it('should validate nodes range', () => {
      const validArgs = { command: 'verify', nodes: 5 };
      const invalidArgs1 = { command: 'verify', nodes: 0 };
      const invalidArgs2 = { command: 'verify', nodes: 101 };
      
      expect(validateArgs(validArgs as any)).toBeNull();
      expect(validateArgs(invalidArgs1 as any)).toBe('Number of nodes must be between 1 and 100');
      expect(validateArgs(invalidArgs2 as any)).toBe('Number of nodes must be between 1 and 100');
    });
    
    it('should validate iterations minimum', () => {
      const validArgs = { command: 'verify', iterations: 100 };
      const invalidArgs = { command: 'verify', iterations: 50 };
      
      expect(validateArgs(validArgs as any)).toBeNull();
      expect(validateArgs(invalidArgs as any)).toBe('Number of iterations must be at least 100');
    });
    
    it('should validate measurements minimum', () => {
      const validArgs = { command: 'bell', measurements: 10 };
      const invalidArgs = { command: 'bell', measurements: 5 };
      
      expect(validateArgs(validArgs as any)).toBeNull();
      expect(validateArgs(invalidArgs as any)).toBe('Number of measurements must be at least 10');
    });
    
    it('should validate trials minimum', () => {
      const validArgs = { command: 'chsh', trials: 100 };
      const invalidArgs = { command: 'chsh', trials: 50 };
      
      expect(validateArgs(validArgs as any)).toBeNull();
      expect(validateArgs(invalidArgs as any)).toBe('Number of trials must be at least 100');
    });
    
    it('should validate latency range', () => {
      const validArgs = { command: 'network', latency: 1000 };
      const invalidArgs1 = { command: 'network', latency: -1 };
      const invalidArgs2 = { command: 'network', latency: 10001 };
      
      expect(validateArgs(validArgs as any)).toBeNull();
      expect(validateArgs(invalidArgs1 as any)).toBe('Latency must be between 0 and 10000ms');
      expect(validateArgs(invalidArgs2 as any)).toBe('Latency must be between 0 and 10000ms');
    });
    
    it('should validate packet loss range', () => {
      const validArgs = { command: 'network', packetLoss: 0.5 };
      const invalidArgs1 = { command: 'network', packetLoss: -0.1 };
      const invalidArgs2 = { command: 'network', packetLoss: 1.1 };
      
      expect(validateArgs(validArgs as any)).toBeNull();
      expect(validateArgs(invalidArgs1 as any)).toBe('Packet loss must be between 0 and 1');
      expect(validateArgs(invalidArgs2 as any)).toBe('Packet loss must be between 0 and 1');
    });
  });
});
