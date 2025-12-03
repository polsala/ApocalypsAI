# Security and Ethics Guidelines for ApocalypsAI

## Purpose

This document outlines security and ethical considerations for the ApocalypsAI project, particularly regarding automation and GitHub platform usage.

## GitHub Platform Rules and Automation

### PR Review and Approval Policies

GitHub's platform has built-in rules to ensure code quality and prevent abuse:

1. **PR authors cannot approve their own PRs**: This is a fundamental security feature that ensures all code receives independent review before merging.

2. **Branch protection rules**: These enforce review requirements and prevent unauthorized changes to protected branches.

### What is NOT Permitted

The following practices violate GitHub's Terms of Service and platform rules:

❌ **Using secondary accounts to circumvent review requirements**
- Creating a secondary account solely to approve PRs created by your primary account
- Automating approvals using tokens from accounts that don't represent actual reviewers
- Any scheme designed to bypass the "no self-approval" rule

❌ **Abusive automation patterns**
- Automating approvals without actual code review
- Using bots or secondary accounts to artificially satisfy review requirements
- Any automation that defeats the purpose of code review

### Why These Rules Exist

GitHub's platform rules serve important purposes:

1. **Code Quality**: Independent review catches bugs, security issues, and design problems
2. **Security**: Prevents malicious code from being merged without oversight
3. **Accountability**: Ensures changes are reviewed by someone other than the author
4. **Trust**: Maintains the integrity of the development process

## Legitimate Alternatives for ApocalypsAI

The ApocalypsAI project uses **multiple independent AI agents** as legitimate reviewers:

### Current Implementation (Compliant)

✅ **Multi-Agent Review System**
- Three independent AI agents: Gemini, Groq, and OpenRouter
- Each agent operates independently with different LLM providers
- PRs created by one agent are reviewed by the other two agents
- This provides genuine independent review

✅ **Automated Review, NOT Self-Approval**
- When Gemini creates a PR, Groq and OpenRouter review it
- When Groq creates a PR, Gemini and OpenRouter review it
- When OpenRouter creates a PR, Gemini and Groq review it
- Each reviewer uses the same `GH_TOKEN` but represents a different AI entity

### Why This is Acceptable

The current system is legitimate because:

1. **Independent entities**: Each AI agent operates with different models and providers
2. **Genuine review**: Reviews are generated independently by different LLMs
3. **No circumvention**: The system doesn't bypass review requirements; it fulfills them with AI reviewers
4. **Transparent**: The process is documented and visible in PR comments
5. **Valuable feedback**: AI reviews provide actual insights on code quality, security, and documentation

### What Would NOT Be Acceptable

❌ **Using REVIWER_TOKEN for self-approval**
- Having the same agent that created the PR approve it using a different token
- Creating a secondary account just to rubber-stamp approvals
- Any automation that makes reviews meaningless

## Best Practices

### For Automation

1. **Maintain independence**: Reviewers should be truly independent from PR authors
2. **Provide value**: Automated reviews should offer genuine feedback
3. **Be transparent**: Document your automation approach
4. **Respect platform rules**: Don't try to circumvent GitHub's built-in protections

### For AI-Driven Development

1. **Use multiple models**: Different AI providers offer different perspectives
2. **Preserve review intent**: Ensure reviews serve their intended purpose
3. **Human oversight**: Maintain human ability to intervene when needed
4. **Security first**: Never compromise security for automation convenience

## Handling Blocked Requests

When a feature request violates platform rules or ethical guidelines:

1. **Mark as blocked**: Use `triage/blocked` label
2. **Explain clearly**: Document why the request cannot be implemented
3. **Suggest alternatives**: Propose legitimate approaches to achieve the underlying goal
4. **Update documentation**: Use the opportunity to clarify project policies

## Questions or Concerns

If you have questions about whether a particular automation approach is acceptable:

1. Ask yourself: "Does this circumvent a security or quality control mechanism?"
2. Consider: "Would this be acceptable if everyone did it?"
3. Check: "Does this align with the spirit of the platform rules, not just the letter?"

When in doubt, err on the side of caution and transparency.

## References

- [GitHub Terms of Service](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service)
- [GitHub Acceptable Use Policies](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies)
- [GitHub API Terms](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features#a-api-terms)
