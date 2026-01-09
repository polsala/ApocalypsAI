# Nightly Cosmic Env Harmonizer

Ensures your workflow's celestial constants (environment variables) are perfectly aligned before any temporal disruptions occur. This GitHub Action validates the presence of specified environment variables, helping you maintain cosmic harmony in your CI/CD pipelines.

## 🌌 Purpose

In the vast expanse of the ApocalypsAI repository, consistent environment configurations are crucial. The `Nightly Cosmic Env Harmonizer` acts as a celestial guardian, checking that all vital "celestial constants" (environment variables) are present and accounted for. Prevent unexpected temporal rifts caused by missing configurations!

## ✨ Usage

Add this action to your workflow to validate environment variables.

```yaml
name: My Harmonious Workflow
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set some cosmic constants (for testing)
        run: |
          echo "COSMIC_ENERGY=high" >> "$GITHUB_ENV"
          echo "STAR_DUST=abundant" >> "$GITHUB_ENV"

      - name: Harmonize Environment Variables (Success Expected)
        id: harmonize_success
        uses: polsala/ApocalypsAI/utils/nightly-cosmic-env-harmonizer@main
        with:
          celestial_constants: 'COSMIC_ENERGY,STAR_DUST,GITHUB_TOKEN' # GITHUB_TOKEN is always present
          fail_on_disharmony: 'true'
      - name: Report Harmony Status
        run: echo "Harmony Status: ${{ steps.harmonize_success.outputs.harmony_status }}"

      - name: Harmonize Environment Variables (Failure Expected - if not explicitly set)
        id: harmonize_failure
        uses: polsala/ApocalypsAI/utils/nightly-cosmic-env-harmonizer@main
        with:
          celestial_constants: 'MISSING_CONSTANT,COSMIC_ENERGY'
          fail_on_disharmony: 'false' # Set to false to allow workflow to continue for demonstration
      - name: Report Disharmony Status
        run: echo "Disharmony Status: ${{ steps.harmonize_failure.outputs.harmony_status }}"
```

### Inputs

*   `celestial_constants`:
    *   **Description**: A comma-separated string of environment variable names that must be present in the workflow's environment.
    *   **Required**: `true`
*   `fail_on_disharmony`:
    *   **Description**: Set to `true` to make the workflow fail if any specified `celestial_constants` are missing. Set to `false` to only log warnings and continue.
    *   **Required**: `false`
    *   **Default**: `true`

### Outputs

*   `harmony_status`:
    *   **Description**: Returns `"harmonious"` if all `celestial_constants` were found, or `"disharmonious"` if any were missing.

## 🧪 Testing

The action includes a self-contained GitHub Actions workflow (`tests/test.yml`) that demonstrates both successful harmonization and detected disharmony.

To run tests locally (conceptually, as GitHub Actions run in their own environment):
1.  Ensure you have `act` (https://github.com/nektos/act) installed.
2.  Navigate to the `utils/nightly-cosmic-env-harmonizer` directory.
3.  Run `act -W . -j test_harmonizer_success` (or other job names) to execute the test workflow.

The `test.yml` workflow simulates different scenarios:
*   **`test_harmonizer_success`**: Checks for variables that are guaranteed to be present or explicitly set.
*   **`test_harmonizer_failure_fail_true`**: Checks for a missing variable with `fail_on_disharmony: true`, expecting the job to fail.
*   **`test_harmonizer_failure_fail_false`**: Checks for a missing variable with `fail_on_disharmony: false`, expecting the job to succeed but report disharmony.
