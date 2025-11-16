import argparse
import re
import sys
from collections import defaultdict

class LogLuminary:
    def __init__(self, log_file_path, output_file_path=None, custom_patterns=None, case_sensitive=False):
        self.log_file_path = log_file_path
        self.output_file_path = output_file_path
        self.custom_patterns = custom_patterns if custom_patterns else []
        self.case_sensitive = case_sensitive
        self.log_levels = ['ERROR', 'WARNING', 'INFO', 'DEBUG']
        self.level_regexes = {
            level: re.compile(rf'\b{level}\b', re.IGNORECASE if not case_sensitive else 0)
            for level in self.log_levels
        }
        self.custom_compiled_patterns = [
            re.compile(pattern, re.IGNORECASE if not case_sensitive else 0)
            for pattern in self.custom_patterns
        ]

    def analyze_log(self):
        total_lines = 0
        level_counts = defaultdict(int)
        custom_pattern_counts = defaultdict(int)
        error_samples = []
        custom_pattern_samples = defaultdict(list)

        try:
            with open(self.log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    total_lines += 1
                    line = line.strip()

                    # Check for standard log levels
                    matched_level = False
                    for level, regex in self.level_regexes.items():
                        if regex.search(line):
                            level_counts[level] += 1
                            matched_level = True
                            if level == 'ERROR' and len(error_samples) < 10:
                                error_samples.append(f"Line {line_num}: {line}")
                            break
                    
                    # If no standard level matched, count as 'OTHER'
                    if not matched_level:
                        level_counts['OTHER'] += 1

                    # Check for custom patterns
                    for i, pattern_regex in enumerate(self.custom_compiled_patterns):
                        if pattern_regex.search(line):
                            pattern_name = self.custom_patterns[i] # Use original pattern string as key
                            custom_pattern_counts[pattern_name] += 1
                            if len(custom_pattern_samples[pattern_name]) < 10:
                                custom_pattern_samples[pattern_name].append(f"Line {line_num}: {line}")

        except FileNotFoundError:
            print(f"Error: Log file not found at '{self.log_file_path}'", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred while reading the log file: {e}", file=sys.stderr)
            sys.exit(1)

        return {
            'total_lines': total_lines,
            'level_counts': dict(level_counts),
            'custom_pattern_counts': dict(custom_pattern_counts),
            'error_samples': error_samples,
            'custom_pattern_samples': {k: v for k, v in custom_pattern_samples.items() if v}
        }

    def generate_report(self, analysis_results):
        report_lines = []
        report_lines.append("--- Log Luminary Report ---")
        report_lines.append(f"Log File: {self.log_file_path}")
        report_lines.append(f"Total Lines Processed: {analysis_results['total_lines']}")
        report_lines.append("\n--- Log Level Summary ---")
        
        # Sort levels for consistent output, putting known levels first, then 'OTHER'
        sorted_levels = sorted(self.log_levels, key=lambda x: (self.log_levels.index(x) if x in self.log_levels else len(self.log_levels)))
        if 'OTHER' in analysis_results['level_counts']:
            sorted_levels.append('OTHER') # Ensure 'OTHER' is at the end if it exists

        for level in sorted_levels:
            if level in analysis_results['level_counts']:
                report_lines.append(f"{level}: {analysis_results['level_counts'][level]}")

        if analysis_results['custom_pattern_counts']:
            report_lines.append("\n--- Custom Pattern Summary ---")
            for pattern, count in analysis_results['custom_pattern_counts'].items():
                report_lines.append(f"Pattern '{pattern}': {count}")

        if analysis_results['error_samples']:
            report_lines.append("\n--- Sample ERROR Lines (First 10) ---")
            for sample in analysis_results['error_samples']:
                report_lines.append(sample)

        for pattern, samples in analysis_results['custom_pattern_samples'].items():
            report_lines.append(f"\n--- Sample '{pattern}' Lines (First 10) ---")
            for sample in samples:
                report_lines.append(sample)

        report_lines.append("\n--- End of Report ---")

        report_content = "\n".join(report_lines)

        if self.output_file_path:
            try:
                with open(self.output_file_path, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                print(f"Report saved to '{self.output_file_path}'")
            except Exception as e:
                print(f"Error: Could not write report to '{self.output_file_path}': {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print(report_content)

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Log Luminary: Analyze log files and generate summaries."
    )
    parser.add_argument(
        '--log-file', 
        required=True, 
        help='Path to the log file to analyze.'
    )
    parser.add_argument(
        '--output-file', 
        help='Optional path to save the analysis report. If not provided, prints to console.'
    )
    parser.add_argument(
        '--pattern', 
        action='append', 
        help='Optional custom regular expression pattern to search for. Can be specified multiple times.'
    )
    parser.add_argument(
        '--case-sensitive', 
        action='store_true', 
        help='Make pattern matching case-sensitive. By default, it\'s case-insensitive.'
    )

    args = parser.parse_args()

    luminary = LogLuminary(
        log_file_path=args.log_file,
        output_file_path=args.output_file,
        custom_patterns=args.pattern,
        case_sensitive=args.case_sensitive
    )
    results = luminary.analyze_log()
    luminary.generate_report(results)

if __name__ == '__main__':
    main()
