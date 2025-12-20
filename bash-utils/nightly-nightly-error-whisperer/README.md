# Nightly Error Whisperer

The digital world can be a harsh place, full of cryptic error messages that make your circuits fizzle and your spirit sag. Fear not, weary traveler! The `nightly-error-whisperer` is here to soothe your soul and gently guide you through the digital wilderness.

This whimsical utility takes those intimidating error messages and translates them into more approachable, often humorous, and sometimes even helpful suggestions. Turn your frown upside down and let the whisperer bring a little calm to your coding chaos.

## Features

*   **Whimsical Translations**: Replaces common error patterns with friendly, imaginative messages.
*   **Stress Reduction**: Aims to lighten the mood during frustrating debugging sessions.
*   **Gentle Guidance**: Provides subtle hints for resolving issues without being overly technical.
*   **Standard Input/Output**: Easily pipe error messages from other commands.

## Usage

Pipe any command's error output directly into the `nightly-error-whisperer`:

```bash
# Example 1: Command not found
non_existent_command 2>&1 | ./src/error_whisperer.sh

# Example 2: Permission denied
sudo rm /root/secret_file 2>&1 | ./src/error_whisperer.sh

# Example 3: No such file or directory
cat /path/to/non_existent_file 2>&1 | ./src/error_whisperer.sh

# Example 4: Syntax error (simulated)
echo "Error: syntax error at line 5" | ./src/error_whisperer.sh

# Example 5: Connection refused (simulated)
echo "Error: connection refused" | ./src/error_whisperer.sh

# Example 6: Unknown error
echo "FATAL: Unhandled exception 0xDEADBEEF" 2>&1 | ./src/error_whisperer.sh
```

You can also pass the error message as an argument:

```bash
./src/error_whisperer.sh "command not found: git"
```

Or read from a file:

```bash
echo "permission denied: /var/log/syslog" > error.log
./src/error_whisperer.sh < error.log
rm error.log
```

## Installation

1.  Clone the ApocalypsAI repository (if you haven't already):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```
2.  Navigate to the utility directory:
    ```bash
    cd bash-utils/nightly-error-whisperer
    ```
3.  Make the script executable:
    ```bash
    chmod +x src/error_whisperer.sh
    ```

Now you're ready to let the whisperer work its magic!

## Contributing

Feel free to add more whimsical error translations! Open a PR with new patterns and their delightful interpretations.
