Nightly Issue Labeler

One sentence overview: A GitHub Action that automatically adds apocalypseâthemed labels to newly opened issues based on detected keywords.

Purpose
-------
Keeps issue triage fun and organized by applying labels such as "radiation", "mutant", or "survivor" when those words appear in the issue title or body.

Inputs
------
- github-token (required): Personal access token or the default GITHUB_TOKEN with repo scope.
- label-config (optional): JSON string mapping keywords to label names. Default mapping is {"radiation":"radiation","mutant":"mutant","survivor":"survivor"}.

How to use
----------
Add the action to a workflow that triggers on issue creation. Example:

name: Autoâlabel new issues
on:
  issues:
    types: [opened]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Apply apocalypse labels
        uses: ./
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}

The action reads the issue event payload, matches configured keywords, and adds the corresponding labels via the GitHub REST API.

Testing
-------
A bash test script is provided under the tests/ directory. It runs the labeler with a mock payload and a stubbed curl command to verify that the correct labels are selected.

License
-------
MIT
