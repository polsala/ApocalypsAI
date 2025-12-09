import { describe, it, expect, beforeEach } from '@jest/globals';
import { main } from '../src/main';
import { parseArgs } from '../src/utils/args-parser';

/**
 * Tests for the main application entry point.
 * 
 * These tests verify that the CLI correctly parses arguments
 * and routes to the appropriate functionality.
 * 
 * Mock rationale: We mock the CLI module to test argument parsing
 * without actually running the full application.
 */

describe('Main Application', () => {
  let consoleSpy: jest.SpyInstance;
  let processSpy: jest.SpyInstance;
  
  beforeEach(() => {
    consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    processSpy = jest.spyOn(process, 'exit').mockImplementation(() => {});
  });
  
  afterEach(() => {
    consoleSpy.mockRestore();
    processSpy.mockRestore();
  });
  
  it('should parse verify command correctly', () => {
    const args = parseArgs(['verify', '--nodes', '3', '--iterations', '1000']);
    
    expect(args.command).toBe('verify');
    expect(args.nodes).toBe(3);
    expect(args.iterations).toBe(1000);
  });
  
  it('should parse bell command correctly', () => {
    const args = parseArgs(['bell', '--state', '|00⟩ + |11⟩', '--measurements', '500']);
    
    expect(args.command).toBe('bell');
    expect(args.state).toBe('|00⟩ + |11⟩');
    expect(args.measurements).toBe(500);
  });
  
  it('should parse chsh command correctly', () => {
    const args = parseArgs(['chsh', '--trials', '10000']);
    
    expect(args.command).toBe('chsh');
    expect(args.trials).toBe(10000);
  });
  
  it('should parse network command correctly', () => {
    const args = parseArgs(['network', '--latency', '50ms', '--packet-loss', '0.01']);
    
    expect(args.command).toBe('network');
    expect(args.latency).toBe(50);
    expect(args.packetLoss).toBe(0.01);
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
  
  it('should handle latency with ms suffix', () => {
    const args = parseArgs(['--latency', '100ms']);
    expect(args.latency).toBe(100);
  });
  
  it('should handle packet loss as percentage', () => {
    const args = parseArgs(['--packet-loss', '5%']);
    expect(args.packetLoss).toBe(0.05);
  });
  
  it('should handle packet loss as decimal', () => {
    const args = parseArgs(['--packet-loss', '0.02']);
    expect(args.packetLoss).toBe(0.02);
  });
});
