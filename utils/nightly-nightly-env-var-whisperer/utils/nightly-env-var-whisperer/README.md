# Nightly Env-Var Whisperer

## 🌌 A Gentle Revelation of Your Environment's Secrets 🌌

The `Nightly Env-Var Whisperer` is a whimsical yet practical utility designed to help you peek into your system's environment variables. It gently lists them, allowing you to filter by prefix and automatically identifying potentially sensitive variables (like API keys or passwords) so you can ensure they are handled with care, without ever exposing their actual values in the output.

This tool is perfect for:
- Debugging scripts that rely on environment variables.
- Performing quick security checks to see what sensitive data might be exposed.
- Maintaining good environment hygiene by understanding what's set.

## Usage

Run the utility from its `src` directory:

```bash
python src/whisperer.py [--prefix <string>] [--sensitive-keywords <keyword1,keyword2,...>]
```

### Arguments:

*   `--prefix <string>`: (Optional) Only display environment variables whose names start with the specified string. If omitted, all variables are considered.
*   `--sensitive-keywords <keyword1,keyword2,...>`: (Optional) A comma-separated list of keywords (case-insensitive) to identify potentially sensitive environment variables. Variables containing any of these keywords in their name will be marked as sensitive and their values redacted in the output. Defaults to `KEY,TOKEN,PASSWORD,SECRET,API_KEY,AUTH`.

## Examples

### 1. List all environment variables with default sensitive keyword detection:

```bash
python src/whisperer.py
```

**Example Output:**
```
🌌 Nightly Env-Var Whisperer 🌌

Whispering environment variables (prefix: '', sensitive keywords: ['KEY', 'TOKEN', 'PASSWORD', 'SECRET', 'API_KEY', 'AUTH']):

  - HOME: /home/user
  - PATH: /usr/local/bin:/usr/bin:/bin
  - MY_APP_API_KEY: ***REDACTED*** (Sensitive? ✨)
  - USER: user
  - GITHUB_TOKEN: ***REDACTED*** (Sensitive? ✨)
```

### 2. List only variables starting with `APP_`:

```bash
python src/whisperer.py --prefix APP_
```

**Example Output:**
```
🌌 Nightly Env-Var Whisperer 🌌

Whispering environment variables (prefix: 'APP_', sensitive keywords: ['KEY', 'TOKEN', 'PASSWORD', 'SECRET', 'API_KEY', 'AUTH']):

  - APP_NAME: MyAwesomeApp
  - APP_SECRET: ***REDACTED*** (Sensitive? ✨)
```

### 3. Use custom sensitive keywords:

```bash
python src/whisperer.py --sensitive-keywords "CREDENTIAL,AUTH_CODE"
```

**Example Output:**
```
🌌 Nightly Env-Var Whisperer 🌌

Whispering environment variables (prefix: '', sensitive keywords: ['CREDENTIAL', 'AUTH_CODE']):

  - USER_CREDENTIAL: ***REDACTED*** (Sensitive? ✨)
  - MY_API_KEY: my_value_here
```
