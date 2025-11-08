import re
import argparse

def remove_timestamps(line: str) -> str:
    """Removes common timestamp patterns from a log line."""
    # ISO 8601-like: YYYY-MM-DDTHH:MM:SS.sssZ or YYYY-MM-DD HH:MM:SS, etc.
    line = re.sub(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d{3,6})?(?:Z|[+-]\d{2}:\d{2})?', '', line)
    # Simple HH:MM:SS or HH:MM:SS.sss
    line = re.sub(r'\d{2}:\d{2}:\d{2}(?:\.\d{3,6})?', '', line)
    # Remove leading/trailing whitespace after timestamp removal
    return line.strip()

def redact_sensitive_data(line: str) -> str:
    """Redacts common sensitive data patterns (API keys, tokens, IPs)."""
    # API Keys/Tokens/Secrets patterns
    line = re.sub(r'(API_KEY|TOKEN|SECRET|PASSWORD|AUTH_KEY|AUTH_TOKEN|BEARER)\s*=\s*[\w-]{10,}', r'\1=[REDACTED_SECRET]', line, flags=re.IGNORECASE)
    line = re.sub(r'(sk_live|pk_live|AKIA|ASIA)[\w-]{16,}', '[REDACTED_SECRET]', line)
    
    # IPv4 addresses
    line = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[REDACTED_IP]', line)
    
    return line

def collapse_redundant_lines(lines: list[str]) -> list[str]:
    """Collapses consecutive identical lines into a single line."""
    if not lines:
        return []
    
    purified_lines = []
    last_line = None
    for line in lines:
        if line != last_line:
            purified_lines.append(line)
            last_line = line
    return purified_lines

def purify_log_content(log_content: str) -> str:
    """Applies all purification steps to the given log content."""
    lines = log_content.splitlines()
    
    # Step 1: Remove timestamps and redact sensitive data from each line
    processed_lines = []
    for line in lines:
        line = remove_timestamps(line)
        line = redact_sensitive_data(line)
        if line.strip(): # Only add non-empty lines after processing
            processed_lines.append(line.strip())
            
    # Step 2: Collapse redundant lines
    final_lines = collapse_redundant_lines(processed_lines)
    
    return "\n".join(final_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Chronos-Warp Log Purifier: Cleanses log files of temporal anomalies, redundant entries, and sensitive data."
    )
    parser.add_argument('--input', required=True, help='Path to the raw log file.')
    parser.add_argument('--output', required=True, help='Path to save the purified log file.')
    
    args = parser.parse_args()
    
    try:
        with open(args.input, 'r') as infile:
            raw_content = infile.read()
        
        purified_content = purify_log_content(raw_content)
        
        with open(args.output, 'w') as outfile:
            outfile.write(purified_content)
            
        print(f"Log file '{args.input}' purified and saved to '{args.output}'.")
            
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
