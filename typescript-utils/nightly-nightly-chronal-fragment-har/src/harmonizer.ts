import { DataFragment, FragmentCategory, HarmonizationReport } from './types';

export class ChronalFragmentHarmonizer {
  private fragments: DataFragment[];

  constructor(fragments: DataFragment[]) {
    this.fragments = this.validateAndSortFragments(fragments);
  }

  private validateAndSortFragments(fragments: DataFragment[]): DataFragment[] {
    if (!Array.isArray(fragments)) {
      throw new Error('Input must be an array of data fragments.');
    }

    for (const fragment of fragments) {
      if (typeof fragment.id !== 'string' || fragment.id.trim() === '') {
        throw new Error(`Invalid fragment: 'id' must be a non-empty string. Fragment: ${JSON.stringify(fragment)}`);
      }
      if (typeof fragment.content !== 'string') {
        throw new Error(`Invalid fragment: 'content' must be a string. Fragment ID: ${fragment.id}`);
      }
      if (typeof fragment.timestamp !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/.test(fragment.timestamp)) {
        throw new Error(`Invalid fragment: 'timestamp' must be an ISO 8601 string (e.g., 2023-01-01T12:00:00Z). Fragment ID: ${fragment.id}`);
      }
      if (typeof fragment.temporalDistortion !== 'number' || fragment.temporalDistortion < 0 || fragment.temporalDistortion > 100) {
        throw new Error(`Invalid fragment: 'temporalDistortion' must be a number between 0 and 100. Fragment ID: ${fragment.id}`);
      }
      if (typeof fragment.origin !== 'string' || fragment.origin.trim() === '') {
        throw new Error(`Invalid fragment: 'origin' must be a non-empty string. Fragment ID: ${fragment.id}`);
      }
    }

    // Sort by temporalDistortion (ascending) then timestamp (ascending)
    return [...fragments].sort((a, b) => {
      if (a.temporalDistortion !== b.temporalDistortion) {
        return a.temporalDistortion - b.temporalDistortion;
      }
      return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime();
    });
  }

  public categorizeFragment(fragment: DataFragment): FragmentCategory {
    if (fragment.temporalDistortion < 20) {
      return 'Stable';
    } else if (fragment.temporalDistortion >= 20 && fragment.temporalDistortion <= 60) {
      return 'Unstable';
    } else {
      return 'Highly Distorted';
    }
  }

  public generateReport(): HarmonizationReport {
    const stableFragments: DataFragment[] = [];
    const unstableFragments: DataFragment[] = [];
    const highlyDistortedFragments: DataFragment[] = [];

    for (const fragment of this.fragments) {
      const category = this.categorizeFragment(fragment);
      if (category === 'Stable') {
        stableFragments.push(fragment);
      } else if (category === 'Unstable') {
        unstableFragments.push(fragment);
      } else {
        highlyDistortedFragments.push(fragment);
      }
    }

    const recommendations = [
      'Prioritize integration of \'Stable Fragments\' first, as they exhibit minimal temporal distortion.',
      '\'Unstable Fragments\' may require pre-processing or additional temporal stabilization before full integration.',
      '\'Highly Distorted Fragments\' should be quarantined and analyzed for potential temporal anomalies before any integration attempts. Proceed with extreme caution.',
      'Consider cross-referencing fragments from \'Void Echo\' origins for unique insights into pre-collapse timelines, but verify their stability.'
    ];

    return {
      totalFragments: this.fragments.length,
      stableFragments,
      unstableFragments,
      highlyDistortedFragments,
      recommendations,
    };
  }

  public formatReport(report: HarmonizationReport): string {
    let output = 'Chronal Fragment Harmonization Report\n\n';
    output += `Total Fragments Processed: ${report.totalFragments}\n`;
    output += `Stable Fragments (Distortion < 20): ${report.stableFragments.length}\n`;
    output += `Unstable Fragments (Distortion 20-60): ${report.unstableFragments.length}\n`;
    output += `Highly Distorted Fragments (Distortion > 60): ${report.highlyDistortedFragments.length}\n\n`;

    const formatFragment = (fragment: DataFragment) =>
      `[${fragment.id}] (${fragment.origin}) ${fragment.timestamp} - Distortion: ${fragment.temporalDistortion}\n  Content: ${fragment.content}`;

    if (report.stableFragments.length > 0) {
      output += '--- Stable Fragments ---\n';
      output += report.stableFragments.map(formatFragment).join('\n') + '\n\n';
    }

    if (report.unstableFragments.length > 0) {
      output += '--- Unstable Fragments ---\n';
      output += report.unstableFragments.map(formatFragment).join('\n') + '\n\n';
    }

    if (report.highlyDistortedFragments.length > 0) {
      output += '--- Highly Distorted Fragments ---\n';
      output += report.highlyDistortedFragments.map(formatFragment).join('\n') + '\n\n';
    }

    output += '--- Harmonization Recommendations ---\n';
    output += report.recommendations.map(rec => `- ${rec}`).join('\n') + '\n';

    return output;
  }
}
