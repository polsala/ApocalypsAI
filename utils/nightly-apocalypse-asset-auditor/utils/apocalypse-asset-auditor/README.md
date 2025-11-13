# Apocalypse Asset Auditor

## 🚨 Ensuring Your Digital Bunker is Stocked for the Code-pocalypse! 🚨

This utility, the **Apocalypse Asset Auditor**, acts as your project's vigilant quartermaster, scanning your repository to ensure all critical foundational files are present and accounted for. Just as a prepper checks their supplies before the big one, this tool helps you verify your project's essential documentation and automation are ready for anything – from a sudden influx of new contributors to the inevitable digital decay.

### Why is this useful?

*   **Project Health**: Quickly identify missing key files that are crucial for project understanding, legal compliance, and community engagement.
*   **Onboarding**: New contributors can instantly see if a project is well-maintained and documented.
*   **Automation Readiness**: Verify that your `.github/workflows/` directory exists and contains active workflows, ensuring your CI/CD pipeline is operational.
*   **Whimsical Peace of Mind**: Sleep soundly knowing your digital assets are audited and ready.

### Usage

To run the auditor, navigate to your repository's root directory (or the directory you wish to audit) and execute the `auditor.py` script. You can optionally specify a custom path to audit as an argument.

```bash
# Audit the current directory
python src/auditor.py

# Audit a specific directory
python src/auditor.py /path/to/your/repo
```

#### Example Output:

```
🚨 Apocalypse Asset Auditor Report 🚨

Scanning repository at: /path/to/your/repo

✅ README.md: Present and accounted for.
✅ LICENSE: Present and accounted for.
❌ CONTRIBUTING.md: Missing! Consider adding guidelines for new survivors.
✅ .gitignore: Present and accounted for.
✅ .github/workflows/: Directory exists with 2 workflows. Automation online!

---
--- Bunker Readiness Status: PARTIALLY STOCKED ---
(1 critical asset(s) are missing. Recommend immediate action!)
```

### Configuration

The `auditor.py` script can be configured to check for a custom list of critical assets by modifying the `CRITICAL_ASSETS` list within the script.

**Default Critical Assets:**

*   `README.md`
*   `LICENSE`
*   `CONTRIBUTING.md` (Optional, but highly recommended)
*   `.gitignore`
*   `.github/workflows/` (Checks for directory existence and at least one `.yml` or `.yaml` file within it)
