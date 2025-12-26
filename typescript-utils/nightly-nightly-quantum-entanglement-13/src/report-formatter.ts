import { EntanglementResult, ReportType } from './types';

export function formatReport(result: EntanglementResult, reportType: ReportType): string {
  switch (reportType) {
    case 'simple':
      return formatSimpleReport(result);
    case 'detailed':
      return formatDetailedReport(result);
    case 'json':
      return formatJsonReport(result);
    default:
      return formatDetailedReport(result);
  }
}

function formatSimpleReport(result: EntanglementResult): string {
  const status = result.entanglementScore > 0.7 ? '⚠️  HIGH' : 
                 result.entanglementScore > 0.4 ? '⚠️  MEDIUM' : '✅ LOW';

  return `
🔬 Quantum Entanglement Analysis
================================

📁 Target: ${result.targetPath}
📅 Generated: ${result.timestamp}
⏱️  Analysis Time: ${result.analysisTime}ms

📊 Overall Score: ${result.entanglementScore.toFixed(2)} (${status})
📁 Files Analyzed: ${result.totalFiles}
🧩 Components: ${result.totalComponents}

🔍 High Entanglement Pairs: ${result.entangledPairs.filter(p => p.type === 'high').length}

💡 ${result.recommendations[0] || 'No specific recommendations'}
`;
}

function formatDetailedReport(result: EntanglementResult): string {
  const statusEmoji = result.entanglementScore > 0.7 ? '⚠️' : 
                     result.entanglementScore > 0.4 ? '⚠️' : '✅';

  let report = `
🔬 Quantum Entanglement Analysis Report
=====================================

📁 Target: ${result.targetPath}
📅 Generated: ${result.timestamp}
⏱️  Analysis Time: ${result.analysisTime}ms

📊 Overall Entanglement Score: ${result.entanglementScore.toFixed(2)} ${statusEmoji}
📁 Files Analyzed: ${result.totalFiles}
🧩 Components: ${result.totalComponents}

`;

  // Group entangled pairs by type
  const highPairs = result.entangledPairs.filter(p => p.type === 'high');
  const mediumPairs = result.entangledPairs.filter(p => p.type === 'medium');
  const lowPairs = result.entangledPairs.filter(p => p.type === 'low');

  if (highPairs.length > 0) {
    report += `⚠️  High Entanglement Detected (${highPairs.length} pairs):
`;
    highPairs.forEach(pair => {
      report += `   • ${pair.component1} ↔ ${pair.component2} (Score: ${pair.score.toFixed(2)})
`;
    });
    report += '\n';
  }

  if (mediumPairs.length > 0) {
    report += `⚠️  Medium Entanglement (${mediumPairs.length} pairs):
`;
    mediumPairs.slice(0, 5).forEach(pair => {
      report += `   • ${pair.component1} ↔ ${pair.component2} (Score: ${pair.score.toFixed(2)})
`;
    });
    if (mediumPairs.length > 5) {
      report += `   ... and ${mediumPairs.length - 5} more\n`;
    }
    report += '\n';
  }

  if (lowPairs.length > 0) {
    report += `💡 Low Entanglement (${lowPairs.length} pairs):
`;
    lowPairs.slice(0, 3).forEach(pair => {
      report += `   • ${pair.component1} ↔ ${pair.component2} (Score: ${pair.score.toFixed(2)})
`;
    });
    if (lowPairs.length > 3) {
      report += `   ... and ${lowPairs.length - 3} more\n`;
    }
    report += '\n';
  }

  if (result.recommendations.length > 0) {
    report += `💡 Recommendations:\n`;
    result.recommendations.forEach(rec => {
      report += `   ${rec}\n`;
    });
  }

  return report;
}

function formatJsonReport(result: EntanglementResult): string {
  return JSON.stringify(result, null, 2);
}
