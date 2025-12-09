# Security Policy

## Supported Versions

This action is actively maintained and security updates are provided for the latest version.

## Reporting Vulnerabilities

To report a security vulnerability, please use GitHub's Security Advisory feature:

1. Go to the repository's Security tab
2. Click "Report a vulnerability"
3. Fill out the form with details about the vulnerability

### What to Include

When reporting a vulnerability, please include:

- A clear description of the vulnerability
- Steps to reproduce the issue
- Potential impact of the vulnerability
- Any suggested fixes or mitigations

## Security Considerations

### Token Permissions

This action requires a GitHub token with the following minimum permissions:

- `contents:read` - To read repository branches
- `pull-requests:write` - To create pull requests for closing branches

### Protected Branches

The action includes multiple layers of protection for important branches:

1. **Default protected branches**: `main`, `master`, `develop`, `dev`, `release/*`
2. **Configurable protection**: Users can specify additional protected branch patterns
3. **Wildcard support**: Protect entire categories of branches (e.g., `release/*`, `hotfix/*`)

### Dry Run Mode

Always test the action in dry run mode first to ensure it behaves as expected:

```yaml
- name: Prune stale branches (dry run)
  uses: polsala/ApocalypsAI/nightly-git-branch-pruner@main
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
    dry-run: true
```

### Branch Closure vs. Deletion

This action closes branches by creating pull requests rather than force-deleting them. This approach:

- Preserves branch history
- Allows for review before merging
- Prevents accidental data loss
- Maintains audit trails

## Best Practices

1. **Use dedicated tokens**: Create repository-specific tokens with minimal required permissions
2. **Test in dry run mode**: Always verify behavior before enabling actual branch closure
3. **Review protected branches**: Regularly review and update the list of protected branches
4. **Monitor logs**: Check action logs for any unexpected behavior
5. **Start conservatively**: Begin with a higher inactivity threshold and adjust as needed

## Incident Response

If you discover a security issue:

1. Report it immediately using the vulnerability reporting process above
2. If the issue affects live systems, consider disabling the action temporarily
3. Document the incident and steps taken for future reference

## Contact

For security-related questions or concerns, please open a discussion in the repository's Discussions tab.
