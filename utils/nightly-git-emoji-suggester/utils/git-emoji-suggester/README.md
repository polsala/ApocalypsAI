# Git Emoji Suggester

## 🌟 What is this?

The Git Emoji Suggester is a delightful little utility that peeks into your staged Git changes (your diff) and, with a sprinkle of AI-powered whimsy, suggests relevant emojis to adorn your commit messages. Ever stared blankly at your terminal, wondering if your `feat: add user authentication` commit deserves a ✨ or a 🚀? This tool is for you!

It helps standardize and beautify your commit history, making it more readable and fun for everyone involved in the project. No more guessing which emoji fits best – let the Suggester guide you!

## 🚀 How to Use

1.  **Ensure you have `git` installed.** This utility relies on `git diff` output.
2.  **Run the script with your diff content.** You can pipe `git diff` output directly to it.

    ```bash
    # For staged changes:
    git diff --cached | python3 utils/git-emoji-suggester/src/emoji_suggester.py

    # For unstaged changes:
    git diff | python3 utils/git-emoji-suggester/src/emoji_suggester.py

    # Or pass content directly (for testing/integration):
    echo "<your_diff_content_here>" | python3 utils/git-emoji-suggester/src/emoji_suggester.py
    ```

3.  The script will output a space-separated list of suggested emojis, followed by a newline.

## 💡 Example

Let's say you've added a new feature and fixed a small bug:

```bash
$ git diff --cached
diff --git a/src/feature.py b/src/feature.py
index abc1234..def5678 100644
--- a/src/feature.py
+++ b/src/feature.py
@@ -1,4 +1,8 @@
 class NewFeature:
     def __init__(self):
         pass
+    def new_method(self):
+        # This is a new feature
+        pass
 
 class BuggyCode:
     def old_method(self):
-        print("Bug here")
+        print("Bug fixed") # Fix for issue #123
```

Running the suggester:

```bash
$ git diff --cached | python3 utils/git-emoji-suggester/src/emoji_suggester.py
✨ 🐛
```

Suggested commit message: `feat(auth): Add user authentication ✨, fix(bug): Resolve login issue 🐛`

## 🛠️ Development

To run tests:

```bash
python3 -m unittest utils/git-emoji-suggester/tests/test_emoji_suggester.py
```
