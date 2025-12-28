# Contributing to Chaos Monkey

Thank you for considering contributing to the Chaos Monkey Terraform module! We welcome contributions from everyone.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Code Style](#code-style)
5. [Testing](#testing)
6. [Documentation](#documentation)
7. [Submitting Changes](#submitting-changes)
8. [Security](#security)
9. [License](#license)

## Code of Conduct

We are committed to providing a friendly, safe, and welcoming environment for all, regardless of gender, sexual orientation, disability, ethnicity, religion, or similar personal characteristic.

Please avoid using overtly sexual aliases or other nicknames that might detract from a friendly, safe, and welcoming environment for all.

## Getting Started

### Prerequisites

- Terraform 1.0+
- Python 3.11+
- AWS CLI configured with appropriate permissions
- Git

### Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ApocalypsAI.git
   cd ApocalypsAI/terraform-modules/nightly-terraform-chaos-monkey
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

We follow a standard GitHub workflow:

1. **Create a branch** from `main` for your changes
2. **Make your changes** following our code style guidelines
3. **Write tests** for your changes
4. **Run the test suite** to ensure everything works
5. **Update documentation** if needed
6. **Submit a pull request**

### Branch Naming

Use descriptive branch names:

- `feature/add-new-resource-type`
- `bugfix/fix-termination-logic`
- `docs/update-readme`
- `test/add-integration-tests`

## Code Style

### Terraform

- Use 2 spaces for indentation
- Follow HashiCorp's Terraform style guide
- Use descriptive variable and resource names
- Add comments for complex logic
- Use consistent naming conventions

### Python

- Follow PEP 8 style guidelines
- Use Black for code formatting
- Use type hints where appropriate
- Write docstrings for all functions and classes

### Git Commit Messages

Write clear, descriptive commit messages:

```
feat: add support for ECS service termination

- Add ECS service detection logic
- Implement ECS service termination function
- Add tests for ECS service chaos
- Update documentation with ECS examples
```

## Testing

### Test Structure

Tests are organized as follows:

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── examples/       # Example configuration tests
└── fixtures/       # Test data and mock objects
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test category
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
python -m pytest tests/examples/ -v

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run Terraform validation
terraform validate

# Run Terraform fmt
terraform fmt -check
```

### Test Requirements

- All new features must include tests
- Tests must be deterministic
- Tests should cover both positive and negative cases
- Integration tests should use mocking for AWS services
- Unit tests should test individual functions in isolation

## Documentation

### README.md

Keep the README updated with:

- Clear usage instructions
- Configuration examples
- Safety warnings
- Troubleshooting guide

### Code Comments

- Add comments for complex logic
- Document public functions and classes
- Explain non-obvious decisions

### Examples

- Provide working examples in the `examples/` directory
- Include both basic and advanced configurations
- Document any assumptions or prerequisites

## Submitting Changes

### Pull Request Guidelines

1. **Ensure tests pass** before submitting
2. **Update documentation** if your changes affect usage
3. **Add a clear PR description** explaining:
   - What the change does
   - Why it's needed
   - Any breaking changes
4. **Reference issues** if applicable
5. **Be responsive** to review feedback

### Review Process

- All changes require at least one review
- Automated tests must pass
- Documentation changes may have a lighter review process
- Breaking changes require additional review and discussion

## Security

### Security Best Practices

- Never commit secrets or credentials
- Use IAM roles with minimal permissions
- Follow AWS security best practices
- Report security vulnerabilities privately

### Safety Features

The Chaos Monkey includes several safety features:

- **Safe mode**: Prevents actual resource termination
- **Excluded tags**: Protects critical resources
- **Resource limits**: Prevents excessive chaos
- **Time windows**: Limits when chaos can occur
- **Dry run mode**: Only logs what would be done

When contributing:

- Never remove or weaken safety features
- Add additional safety checks when appropriate
- Test safety features thoroughly
- Document any new safety mechanisms

### Reporting Security Issues

To report a security vulnerability:

1. Do not open a public issue
2. Contact the maintainers privately
3. Include details about the vulnerability
4. Suggest a fix if possible

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Questions?

If you have questions about contributing:

1. Check the existing issues and discussions
2. Open a new issue for questions
3. Join our community discussions

Thank you for contributing to Chaos Monkey! 🎉

---

**Note**: This is a chaos engineering tool that terminates cloud resources. Always use with extreme caution and never in production environments without proper safeguards and approvals.
