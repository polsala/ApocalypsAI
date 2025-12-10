import { AsciiArtGenerator, MockImageData } from '../src/main';

function assert(condition: boolean, message: string): void {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}

function testAsciiArtGenerator(): void {
  console.log('Testing AsciiArtGenerator...');
  
  // Create a simple test image
  const width = 10;
  const height = 10;
  const imageData = new MockImageData(width, height);
  
  const generator = new AsciiArtGenerator(imageData.data, width, height);
  
  // Test default settings
  generator.setOutputWidth(40);
  generator.setStyle('block');
  generator.setContrast(1.2);
  
  const asciiArt = generator.generate();
  
  // Basic validation
  assert(typeof asciiArt === 'string', 'generate() should return a string');
  assert(asciiArt.length > 0, 'ASCII art should not be empty');
  assert(asciiArt.includes('\n'), 'ASCII art should contain newlines');
  
  // Test different styles
  generator.setStyle('dots');
  const dotsArt = generator.generate();
  assert(dotsArt !== asciiArt, 'Different styles should produce different output');
  
  generator.setStyle('braille');
  const brailleArt = generator.generate();
  assert(brailleArt !== dotsArt, 'Braille style should be different from dots');
  
  // Test width constraints
  generator.setOutputWidth(5); // Should be clamped to 10
  const smallArt = generator.generate();
  assert(smallArt.length > 0, 'Small width should still produce output');
  
  generator.setOutputWidth(300); // Should be clamped to 200
  const largeArt = generator.generate();
  assert(largeArt.length > 0, 'Large width should still produce output');
  
  // Test contrast constraints
  generator.setContrast(0.1); // Should be clamped to 0.5
  generator.generate(); // Should not throw
  
  generator.setContrast(5); // Should be clamped to 3
  generator.generate(); // Should not throw
  
  console.log('✓ All AsciiArtGenerator tests passed');
}

function testMockImageData(): void {
  console.log('Testing MockImageData...');
  
  const width = 5;
  const height = 5;
  const imageData = new MockImageData(width, height);
  
  assert(imageData.width === width, 'Width should match');
  assert(imageData.height === height, 'Height should match');
  assert(imageData.data.length === width * height * 4, 'Data array should have correct size');
  
  // Check that data contains valid RGBA values
  for (let i = 0; i < imageData.data.length; i += 4) {
    const r = imageData.data[i];
    const g = imageData.data[i + 1];
    const b = imageData.data[i + 2];
    const a = imageData.data[i + 3];
    
    assert(r >= 0 && r <= 255, 'Red channel should be 0-255');
    assert(g >= 0 && g <= 255, 'Green channel should be 0-255');
    assert(b >= 0 && b <= 255, 'Blue channel should be 0-255');
    assert(a === 255, 'Alpha channel should be 255');
  }
  
  console.log('✓ All MockImageData tests passed');
}

function runTests(): void {
  console.log('Running tests...\n');
  
  testMockImageData();
  testAsciiArtGenerator();
  
  console.log('\n✓ All tests passed!');
}

// Mock the global parseArgs function for testing
(global as any).parseArgs = function(args: string[]) {
  return {
    values: {
      width: undefined,
      style: undefined,
      output: undefined,
      contrast: undefined,
      help: false
    },
    positionals: args
  };
};

// Run tests if this file is executed directly
if (require.main === module) {
  runTests();
}

export { runTests };
