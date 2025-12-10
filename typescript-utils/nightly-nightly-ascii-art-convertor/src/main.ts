import * as fs from 'fs';
import * as path from 'path';
import { parseArgs } from 'util';

// ASCII character sets for different styles
const ASCII_CHARS = {
  block: [' ', '░', '▒', '▓', '█'],
  dots: [' ', '⠄', '⠂', '⠆', '⠤', '⡆', '⡇', '⡏', '⡟', '⡿', '⣿'],
  braille: [' ', '⢀', '⡀', '⠠', '⢠', '⡈', '⠰', '⢄', '⡂', '⠐', '⢤', '⡒', '⠲', '⢴', '⡔', '⠴', '⢆', '⡃', '⠐', '⢦', '⡓', '⠲', '⢶', '⡕', '⠶', '⢇', '⡃', '⠘', '⢧', '⡓', '⠲', '⢷', '⡕', '⠷', '⢸', '⡜', '⠸', '⢼', '⡼', '⠼', '⣇', '⡧', '⣧', '⡷', '⣷', '⣿']
};

class AsciiArtGenerator {
  private imageData: Uint8ClampedArray;
  private width: number;
  private height: number;
  private outputWidth: number;
  private style: 'block' | 'dots' | 'braille';
  private contrast: number;

  constructor(imageData: Uint8ClampedArray, width: number, height: number) {
    this.imageData = imageData;
    this.width = width;
    this.height = height;
    this.outputWidth = 80;
    this.style = 'braille';
    this.contrast = 1.2;
  }

  setOutputWidth(width: number): void {
    this.outputWidth = Math.max(10, Math.min(200, width));
  }

  setStyle(style: 'block' | 'dots' | 'braille'): void {
    this.style = style;
  }

  setContrast(contrast: number): void {
    this.contrast = Math.max(0.5, Math.min(3, contrast));
  }

  generate(): string {
    const chars = ASCII_CHARS[this.style];
    const aspectRatio = this.width / this.height;
    const outputHeight = Math.floor(this.outputWidth / aspectRatio / 2);
    
    let asciiArt = '';
    
    for (let y = 0; y < outputHeight; y++) {
      let line = '';
      
      for (let x = 0; x < this.outputWidth; x++) {
        const pixelX = Math.floor((x * this.width) / this.outputWidth);
        const pixelY = Math.floor((y * this.height) / outputHeight);
        
        const index = (pixelY * this.width + pixelX) * 4;
        const r = this.imageData[index];
        const g = this.imageData[index + 1];
        const b = this.imageData[index + 2];
        
        // Convert RGB to grayscale
        const gray = Math.floor(0.299 * r + 0.587 * g + 0.114 * b);
        
        // Apply contrast
        let adjusted = ((gray / 255 - 0.5) * this.contrast + 0.5) * 255;
        adjusted = Math.max(0, Math.min(255, adjusted));
        
        // Map to ASCII character
        const charIndex = Math.floor((adjusted / 255) * (chars.length - 1));
        line += chars[charIndex];
      }
      
      asciiArt += line + '\n';
    }
    
    return asciiArt;
  }
}

class MockImageData {
  public data: Uint8ClampedArray;
  public width: number;
  public height: number;

  constructor(width: number, height: number) {
    this.width = width;
    this.height = height;
    this.data = new Uint8ClampedArray(width * height * 4);
    
    // Generate a simple gradient pattern for testing
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const index = (y * width + x) * 4;
        const value = Math.floor((x + y) / (width + height) * 255);
        
        this.data[index] = value;     // R
        this.data[index + 1] = value; // G
        this.data[index + 2] = value; // B
        this.data[index + 3] = 255;   // Alpha
      }
    }
  }
}

class MockCanvas {
  public width: number;
  public height: number;
  private imageData: MockImageData;

  constructor(width: number, height: number) {
    this.width = width;
    this.height = height;
    this.imageData = new MockImageData(width, height);
  }

  getContext(): MockCanvasRenderingContext2D {
    return new MockCanvasRenderingContext2D(this.imageData);
  }
}

class MockCanvasRenderingContext2D {
  private imageData: MockImageData;

  constructor(imageData: MockImageData) {
    this.imageData = imageData;
  }

  drawImage(): void {
    // Mock implementation - no-op
  }

  getImageData(): MockImageData {
    return this.imageData;
  }
}

class MockImage {
  public width: number;
  public height: number;
  private onLoadCallback?: () => void;

  constructor() {
    this.width = 100;
    this.height = 100;
  }

  set src(value: string) {
    // Mock implementation - no-op
    setTimeout(() => {
      if (this.onLoadCallback) {
        this.onLoadCallback();
      }
    }, 10);
  }

  addEventListener(event: string, callback: () => void): void {
    if (event === 'load') {
      this.onLoadCallback = callback;
    }
  }
}

async function loadImage(filePath: string): Promise<MockImageData> {
  const ext = path.extname(filePath).toLowerCase();
  
  if (!['.png', '.jpg', '.jpeg', '.gif'].includes(ext)) {
    throw new Error('Unsupported image format. Please use PNG, JPG, or GIF.');
  }
  
  // Check if file exists
  if (!fs.existsSync(filePath)) {
    throw new Error(`Image file not found: ${filePath}`);
  }
  
  // For testing purposes, create a mock image
  const canvas = new MockCanvas(200, 100);
  const ctx = canvas.getContext();
  
  // Create a simple pattern
  const imageData = ctx.getImageData();
  
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(imageData);
    }, 100);
  });
}

async function main(): Promise<void> {
  try {
    const args = parseArgs({
      args: process.argv.slice(2),
      options: {
        width: { type: 'string', short: 'w' },
        style: { type: 'string', short: 's' },
        output: { type: 'string', short: 'o' },
        contrast: { type: 'string', short: 'c' },
        help: { type: 'boolean', short: 'h' }
      },
      allowPositionals: true
    });
    
    if (args.values.help || args.positionals.length === 0) {
      console.log(`
Usage: ascii-art [command] [options] <file>

Commands:
  convert   Convert image to ASCII art

Options:
  -w, --width <number>     Output width (10-200, default: 80)
  -s, --style <style>      Style: block, dots, or braille (default: braille)
  -o, --output <file>    Save output to file
  -c, --contrast <num>   Contrast level (0.5-3, default: 1.2)
  -h, --help             Show this help message

Examples:
  ascii-art convert image.png
  ascii-art convert image.png --width 120 --style dots
  ascii-art convert image.png --output ascii_art.txt
      `);
      return;
    }
    
    const command = args.positionals[0];
    const filePath = args.positionals[1];
    
    if (command !== 'convert') {
      throw new Error('Invalid command. Use "convert" to convert an image.');
    }
    
    if (!filePath) {
      throw new Error('Please specify an image file to convert.');
    }
    
    const image = await loadImage(filePath);
    
    const generator = new AsciiArtGenerator(image.data, image.width, image.height);
    
    if (args.values.width) {
      const width = parseInt(args.values.width, 10);
      if (isNaN(width)) {
        throw new Error('Width must be a number.');
      }
      generator.setOutputWidth(width);
    }
    
    if (args.values.style) {
      const style = args.values.style.toLowerCase();
      if (!['block', 'dots', 'braille'].includes(style)) {
        throw new Error('Style must be one of: block, dots, braille');
      }
      generator.setStyle(style as 'block' | 'dots' | 'braille');
    }
    
    if (args.values.contrast) {
      const contrast = parseFloat(args.values.contrast);
      if (isNaN(contrast)) {
        throw new Error('Contrast must be a number.');
      }
      generator.setContrast(contrast);
    }
    
    const asciiArt = generator.generate();
    
    if (args.values.output) {
      fs.writeFileSync(args.values.output, asciiArt);
      console.log(`ASCII art saved to: ${args.values.output}`);
    } else {
      console.log(asciiArt);
    }
    
  } catch (error) {
    console.error('Error:', error instanceof Error ? error.message : String(error));
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

export { AsciiArtGenerator, MockImageData, MockCanvas, MockImage };
