# nightly-emoji-filename-converter

Convert filenames in a directory to a whimsical emoji representation and back.

## How it works

The script walks a target directory (non‑recursive) and renames every regular file:

* **a‑z** → regional indicator symbols 🇦‑🇿  
* **0‑9** → keycap digits 0️⃣‑9️⃣  
* **space** → ␣ (U+2423)  

All other characters (including “.”) are left untouched, so extensions stay readable.

During *encode* the script stores a hidden mapping file `.emoji_map` in the target directory:

```
original_name|emoji_name
```

Running *decode* reads this file and restores the original filenames.

## Usage

```bash
# Encode all files in ./my‑folder
./src/main.sh encode ./my‑folder

# Decode back to original names
./src/main.sh decode ./my‑folder
```

The utility is pure Bash (requires Bash 4+).
