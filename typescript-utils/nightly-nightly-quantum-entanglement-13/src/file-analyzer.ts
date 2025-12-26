import * as fs from 'fs';
import * as path from 'path';
import { ComponentAnalysis, FileAnalysis } from './types';

export class FileAnalyzer {
  private supportedExtensions = ['.ts', '.js', '.tsx', '.jsx'];

  async analyzeDirectory(targetPath: string): Promise<FileAnalysis> {
    const files: string[] = [];
    const components: ComponentAnalysis[] = [];

    await this.scanDirectory(targetPath, files);

    for (const filePath of files) {
      const component = await this.analyzeFile(filePath);
      if (component) {
        components.push(component);
      }
    }

    return { files, components };
  }

  private async scanDirectory(dirPath: string, files: string[]): Promise<void> {
    try {
      const entries = await fs.promises.readdir(dirPath);

      for (const entry of entries) {
        const fullPath = path.join(dirPath, entry);
        const stat = await fs.promises.stat(fullPath);

        if (stat.isDirectory()) {
          // Skip node_modules and other common directories
          if (!this.shouldSkipDirectory(entry)) {
            await this.scanDirectory(fullPath, files);
          }
        } else if (this.isSupportedFile(entry)) {
          files.push(fullPath);
        }
      }
    } catch (error) {
      // Ignore permission errors and continue
      console.warn(`Warning: Could not read directory ${dirPath}:`, error);
    }
  }

  private shouldSkipDirectory(dirName: string): boolean {
    const skipDirs = [
      'node_modules',
      '.git',
      'dist',
      'build',
      '.next',
      '.nuxt',
      'coverage',
      '.vscode',
      '.idea'
    ];
    return skipDirs.includes(dirName);
  }

  private isSupportedFile(fileName: string): boolean {
    return this.supportedExtensions.some(ext => fileName.endsWith(ext));
  }

  private async analyzeFile(filePath: string): Promise<ComponentAnalysis | null> {
    try {
      const content = await fs.promises.readFile(filePath, 'utf-8');
      const lines = content.split('\n');

      // Extract component name from file path
      const fileName = path.basename(filePath, path.extname(filePath));
      const componentName = this.normalizeComponentName(fileName);

      // Analyze dependencies
      const dependencies = this.extractDependencies(content, filePath);

      // Calculate complexity metrics
      const complexity = this.calculateComplexity(lines);
      const linesOfCode = this.calculateLinesOfCode(lines);

      return {
        name: componentName,
        filePath,
        dependencies,
        linesOfCode,
        complexity
      };
    } catch (error) {
      console.warn(`Warning: Could not analyze file ${filePath}:`, error);
      return null;
    }
  }

  private normalizeComponentName(fileName: string): string {
    // Convert file name to component name
    return fileName
      .replace(/[-_.]/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join('');
  }

  private extractDependencies(content: string, filePath: string): string[] {
    const dependencies: string[] = [];
    const lines = content.split('\n');

    // Extract import statements
    const importRegex = /^\s*(?:import|require)\s+(?:[^\s]+\s+from\s+)?["']([^"']+)['"];/gm;
    let match;

    while ((match = importRegex.exec(content)) !== null) {
      const importPath = match[1];
      const dependencyName = this.normalizeDependencyName(importPath, filePath);
      if (dependencyName && !dependencies.includes(dependencyName)) {
        dependencies.push(dependencyName);
      }
    }

    return dependencies;
  }

  private normalizeDependencyName(importPath: string, currentFile: string): string | null {
    // Skip external dependencies (node_modules)
    if (importPath.startsWith('node_modules') || !importPath.startsWith('.')) {
      return null;
    }

    // Convert relative path to component name
    const currentDir = path.dirname(currentFile);
    const resolvedPath = path.resolve(currentDir, importPath);
    const fileName = path.basename(resolvedPath, path.extname(resolvedPath));

    return this.normalizeComponentName(fileName);
  }

  private calculateComplexity(lines: string[]): number {
    let complexity = 1; // Base complexity

    // Count control flow statements
    const controlFlowPatterns = [
      /\bif\b/g,
      /\belse\b/g,
      /\bfor\b/g,
      /\bwhile\b/g,
      /\bswitch\b/g,
      /\bcase\b/g,
      /\btry\b/g,
      /\bcatch\b/g,
      /\bfinally\b/g,
      /\bfunction\b/g,
      /\b=>\b/g,
      /\?.*:/g // Ternary operators
    ];

    for (const line of lines) {
      for (const pattern of controlFlowPatterns) {
        const matches = line.match(pattern);
        if (matches) {
          complexity += matches.length;
        }
      }
    }

    return complexity;
  }

  private calculateLinesOfCode(lines: string[]): number {
    return lines.filter(line => {
      const trimmed = line.trim();
      return trimmed.length > 0 && !trimmed.startsWith('//') && !trimmed.startsWith('/*');
    }).length;
  }
}
