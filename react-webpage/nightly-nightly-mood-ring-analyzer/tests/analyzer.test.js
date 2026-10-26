import { analyzeUtility } from '../src/analyzer';

describe('analyzeUtility', () => {
  // Mock rationale: We are testing the `analyzeUtility` function in isolation.
  // We provide synthetic utility JSON objects as input to simulate various scenarios
  // without needing to read actual files or interact with a real utility generation process.
  // This ensures deterministic and offline testing.

  test('should return Neutral Stability for empty or irrelevant input', () => {
    const utility = {
      util_name: 'nightly-random-number-generator',
      summary: 'Generates a random number.',
      classifier: 'python-utils',
      files: []
    };
    const mood = analyzeUtility(utility);
    expect(mood.name).toBe('Neutral Stability');
    expect(mood.color).toBe('#808080');
  });

  test('should detect Temporal Flux mood', () => {
    const utility = {
      util_name: 'nightly-temporal-anomaly-detector',
      summary: 'Detects temporal rifts and time distortions.',
      classifier: 'go-utils',
      files: [
        { path: 'src/main.go', content: 'package main\n// Detects temporal anomalies' }
      ]
    };
    const mood = analyzeUtility(utility);
    expect(mood.name).toBe('Temporal Flux');
    expect(mood.color).toBe('#4A90E2');
  });

  test('should detect Wasteland Wanderlust mood', () => {
    const utility = {
      util_name: 'nightly-wasteland-resource-tracker',
      summary: 'Tracks survival resources across the wasteland.',
      classifier: 'rust-utils',
      files: [
        { path: 'src/lib.rs', content: 'fn track_survival_resources() { /* ... */ }' }
      ]
    };
    const mood = analyzeUtility(utility);
    expect(mood.name).toBe('Wasteland Wanderlust');
    expect(mood.color).toBe('#7ED321');
  });

  test('should detect Whimsical Whimsy mood', () => {
    const utility = {
      util_name: 'nightly-whimsical-emoji-clock',
      summary: 'A clock that tells time with whimsical emojis.',
      classifier: 'js-utils',
      files: [
        { path: 'src/clock.js', content: 'const emojis = ["⏰", "✨"]; // whimsical' }
      ]
    };
    const mood = analyzeUtility(utility);
    expect(mood.name).toBe('Whimsical Whimsy');
    expect(mood.color).toBe('#F5A623');
  });

  test('should detect DevOps Drive mood', () => {
    const utility = {
      util_name: 'nightly-ansible-docker-compo',
      summary: 'Deploys Docker Compose stacks using Ansible.',
      classifier: 'ansible-playbooks',
      files: [
        { path: 'src/deploy.yml', content: '- name: Deploy docker-compose' }
      ]
    };
    const mood = analyzeUtility(utility);
    expect(mood.name).toBe('DevOps Drive');
    expect(mood.color).toBe('#BD10E0');
  });

  test('should detect CLI Command mood', () => {
    const utility = {
      util_name: 'nightly-text-similarity-cli',
      summary: 'A CLI tool for comparing text similarity.',
      classifier: 'cli-apps',
      files: [
        { path: 'src/main.py', content: 'import click\n# CLI application' }
      ]
    };
    const mood = analyzeUtility(utility);
    expect(mood.name).toBe('CLI Command');
    expect(mood.color).toBe('#50E3C2');
  });

  test('should detect Data Deep Dive mood', () => {
    const utility = {
      util_name: 'nightly-ml-notebook-data-prep',
      summary: 'Prepares data for ML models in a notebook.',
      classifier: 'ml-notebooks',
      files: [
        { path: 'src/notebook.ipynb', content: 'import pandas as pd\n# Data analysis' }
      ]
    };
    const mood = analyzeUtility(utility);
    expect(mood.name).toBe('Data Deep Dive');
    expect(mood.color).toBe('#F8E71C');
  });

  test('should prioritize mood with higher keyword count', () => {
    const utility = {
      util_name: 'nightly-temporal-wasteland-tracker',
      summary: 'Tracks temporal anomalies in the wasteland.',
      classifier: 'python-utils',
      files: [
        { path: 'src/main.py', content: 'temporal rift wasteland survival time anomaly' }
      ]
    };
    const mood = analyzeUtility(utility);
    // 'temporal' (2), 'rift' (1), 'time' (1), 'anomaly' (1) => 5 for Temporal Flux
    // 'wasteland' (2), 'survival' (1) => 3 for Wasteland Wanderlust
    expect(mood.name).toBe('Temporal Flux');
  });

  test('should handle missing fields gracefully', () => {
    const utility = {
      util_name: 'minimal-util',
      summary: 'A very minimal utility.',
      // classifier and files are missing
    };
    const mood = analyzeUtility(utility);
    expect(mood.name).toBe('Neutral Stability');
  });
});
