import argparse
import re
import os

def purify_content(
    content: str,
    redact_api_keys: bool = True,
    redact_emails: bool = True,
    redact_ips: bool = True,
    optimize_whitespace: bool = True,
    custom_keywords: dict = None
) -> str:
    """Purifies the given content by redacting sensitive information and optimizing whitespace."""
    if custom_keywords is None:
        custom_keywords = {}

    purified_text = content

    # 1. Redact API Keys
    if redact_api_keys:
        # Common patterns: KEY=value, KEY: value, Bearer token, etc.
        # This regex is broad and might catch non-API keys, but better safe than sorry for 'purification'
        api_key_patterns = [
            r'([A-Z_]+_API_KEY|API_KEY|TOKEN|SECRET|PASSWORD|AUTH_KEY|BEARER)\s*[=:]\s*["']?[a-zA-Z0-9_-]{16,}["']?',
            r'ghp_[a-zA-Z0-9_]{36}', # GitHub Personal Access Token
            r'sk-[a-zA-Z0-9_]{32,}', # OpenAI API Key pattern
            r'pk_live_[a-zA-Z0-9_]{24,}', # Stripe Public Key (example)
            r'rk_live_[a-zA-Z0-9_]{24,}', # Stripe Restricted Key (example)
            r'AKIA[0-9A-Z]{16}', # AWS Access Key ID
            r'[a-zA-Z0-9+/]{40}=', # AWS Secret Access Key (base64-encoded)
            r'ya29\.[a-zA-Z0-9_-]+' # Google OAuth token (example)
        ]
        for pattern in api_key_patterns:
            # Use a callback function for replacement to handle groups and ensure consistent redaction
            purified_text = re.sub(pattern, lambda m: f"{m.group(1) if m.group(1) else ''}=[REDACTED_API_KEY]", purified_text, flags=re.IGNORECASE)

    # 2. Redact Email Addresses
    if redact_emails:
        purified_text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[REDACTED_EMAIL]', purified_text)

    # 3. Redact IP Addresses (IPv4 only for simplicity)
    if redact_ips:
        purified_text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[REDACTED_IP]', purified_text)

    # 4. Custom Keyword Replacement
    for original, replacement in custom_keywords.items():
        # Use re.escape to handle special characters in original keyword
        # Use re.IGNORECASE for case-insensitive replacement
        purified_text = re.sub(re.escape(original), replacement, purified_text, flags=re.IGNORECASE)

    # 5. Optimize Whitespace
    if optimize_whitespace:
        # Remove multiple consecutive blank lines (more than 2 newlines -> 2 newlines)
        purified_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', purified_text)
        # Strip leading/trailing whitespace from each line and the whole text
        purified_text = '\n'.join(line.strip() for line in purified_text.splitlines())
        purified_text = purified_text.strip()

    return purified_text

def main():
    parser = argparse.ArgumentParser(
        description="Purify a text file by redacting sensitive information and optimizing whitespace."
    )
    parser.add_argument('--input', required=True, help='Path to the input text file.')
    parser.add_argument('--output', required=True, help='Path where the purified output will be saved.')
    parser.add_argument('--keywords', help='Comma-separated list of original=replacement pairs for custom redaction.', default='')
    parser.add_argument('--no-api-keys', action='store_false', dest='redact_api_keys', help='Disable API key redaction.')
    parser.add_argument('--no-emails', action='store_false', dest='redact_emails', help='Disable email address redaction.')
    parser.add_argument('--no-ips', action='store_false', dest='redact_ips', help='Disable IPv4 address redaction.')
    parser.add_argument('--no-whitespace', action='store_false', dest='optimize_whitespace', help='Disable whitespace optimization.')

    args = parser.parse_args()

    custom_keywords = {}
    if args.keywords:
        for item in args.keywords.split(','):
            if '=' in item:
                key, value = item.split('=', 1)
                custom_keywords[key.strip()] = value.strip()
            else:
                print(f"Warning: Invalid keyword format '{item}'. Expected 'key=value'. Skipping.")

    try:
        with open(args.input, 'r', encoding='utf-8') as f_in:
            content = f_in.read()

        purified_content_str = purify_content(
            content,
            redact_api_keys=args.redact_api_keys,
            redact_emails=args.redact_emails,
            redact_ips=args.redact_ips,
            optimize_whitespace=args.optimize_whitespace,
            custom_keywords=custom_keywords
        )

        # Ensure output directory exists
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(args.output, 'w', encoding='utf-8') as f_out:
            f_out.write(purified_content_str)

        print(f"Successfully purified '{args.input}' to '{args.output}'.")

    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == '__main__':
    main()
