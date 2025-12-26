import * as fs from 'fs';
import * as path from 'path';

export function watchFiles(targetPath: string, onChange: () => Promise<void>): fs.FSWatcher {
  console.log(`👀 Watching directory: ${targetPath}`);

  const watcher = fs.watch(targetPath, { recursive: true }, async (eventType, filename) => {
    if (filename && shouldWatchFile(filename)) {
      console.log(`📁 File changed: ${filename} (${eventType})`);
      try {
        await onChange();
      } catch (error) {
        console.error('❌ Error during re-analysis:', error);
      }
    }
  });

  // Handle watcher errors
  watcher.on('error', (error) => {
    console.error('❌ File watcher error:', error);
  });

  // Handle graceful shutdown
  process.on('SIGINT', () => {
    console.log('\n🛑 Stopping file watcher...');
    watcher.close();
    process.exit(0);
  });

  return watcher;
}

function shouldWatchFile(filename: string): boolean {
  const supportedExtensions = ['.ts', '.js', '.tsx', '.jsx'];
  const skipPatterns = [
    /node_modules/, /\.git/, /dist/, /build/, /\.next/, /\.nuxt/, /coverage/
  ];

  // Check file extension
  const hasSupportedExtension = supportedExtensions.some(ext => filename.endsWith(ext));
  if (!hasSupportedExtension) return false;

  // Check skip patterns
  return !skipPatterns.some(pattern => pattern.test(filename));
}
