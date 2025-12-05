import re
import argparse
import sys
from typing import Optional


def sanitize_branch_name(branch_name: str, allow_special_chars: Optional[str] = None) -> str:
    """
    Sanitize a Git branch name to be safe for CI/CD pipelines and file systems.
    
    Args:
        branch_name: The original branch name
        allow_special_chars: Additional special characters to allow (optional)
    
    Returns:
        Sanitized branch name
    """
    if not branch_name:
        raise ValueError("Branch name cannot be empty")
    
    # Define safe characters (letters, numbers, hyphens, underscores, slashes)
    safe_pattern = r'[^a-zA-Z0-9/_-]'
    
    # If additional special chars are allowed, include them
    if allow_special_chars:
        # Escape special regex characters in the allowed list
        escaped_chars = re.escape(allow_special_chars)
        safe_pattern = f'[^a-zA-Z0-9/_-{escaped_chars}]'
    
    # Replace unsafe characters with hyphens
    sanitized = re.sub(safe_pattern, '-', branch_name)
    
    # Remove multiple consecutive hyphens
    sanitized = re.sub(r'-+', '-', sanitized)
    
    # Remove leading/trailing hyphens
    sanitized = sanitized.strip('-')
    
    # Ensure it doesn't start with a slash
    sanitized = sanitized.lstrip('/')
    
    # Ensure it doesn't end with a slash
    sanitized = sanitized.rstrip('/')
    
    # Ensure it's not empty after sanitization
    if not sanitized:
        sanitized = 'sanitized-branch'
    
    return sanitized


def validate_branch_name(branch_name: str) -> bool:
    """
    Validate if a branch name is safe for Git.
    
    Args:
        branch_name: The branch name to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not branch_name:
        return False
    
    # Git branch name restrictions:
    # - Cannot contain two consecutive dots
    # - Cannot contain any of ~^:?*[]\ (except in ref part)
    # - Cannot start with -
    # - Cannot contain whitespace
    
    invalid_patterns = [
        r'\s',           # Whitespace
        r'\.{2,}',       # Multiple consecutive dots
        r'[~^:?*\\\[\]]',  # Invalid characters
        r'^-',            # Starts with dash
        r'/$',            # Ends with slash
        r'/\./',          # Contains /./
        r'/\.\./',       # Contains /../
        r'^\.',           # Starts with dot
        r'@\{',           # Contains @{
        r'\^',           # Contains ^
        r'~',             # Contains ~
        r'\s+$',         # Ends with whitespace
        r'^\s+'           # Starts with whitespace
    ]
    
    for pattern in invalid_patterns:
        if re.search(pattern, branch_name):
            return False
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Sanitize Git branch names for CI/CD safety'
    )
    parser.add_argument(
        '--branch', '-b',
        required=True,
        help='The branch name to sanitize'
    )
    parser.add_argument(
        '--allow', '-a',
        help='Additional special characters to allow (e.g., "+=")'
    )
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='Show what would be done without writing output'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file to write sanitized name (default: stdout)'
    )
    
    args = parser.parse_args()
    
    try:
        # Sanitize the branch name
        sanitized = sanitize_branch_name(args.branch, args.allow)
        
        # Validate the result
        is_valid = validate_branch_name(sanitized)
        
        if args.dry_run:
            print(f"Original: {args.branch}")
            print(f"Sanitized: {sanitized}")
            print(f"Valid for Git: {is_valid}")
            return
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(sanitized + '\n')
            print(f"Sanitized branch name written to {args.output}")
        else:
            print(sanitized)
        
        if not is_valid:
            print("Warning: Sanitized name may not be valid for Git", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
