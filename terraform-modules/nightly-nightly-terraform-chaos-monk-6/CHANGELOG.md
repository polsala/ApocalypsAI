# Changelog

All notable changes to the Chaos Monkey Terraform module will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-01

### Added

- Initial release of Chaos Monkey Terraform module
- Support for EC2 instance termination
- Support for RDS instance deletion
- Support for ECS service scaling
- Safe mode for testing without actual termination
- Excluded tags for protecting critical resources
- Configurable chaos intensity and scheduling
- SNS notifications for chaos events
- CloudWatch metrics and dashboards
- Comprehensive test suite
- Multiple example configurations
- Safety features including resource limits and time windows
- Audit logging and monitoring

### Features

- **Lambda-based execution**: Serverless chaos execution
- **Multi-resource support**: Terminate EC2, RDS, and ECS resources
- **Flexible scheduling**: Cron-based chaos scheduling
- **Safety mechanisms**: Multiple layers of protection
- **Monitoring integration**: CloudWatch metrics and alarms
- **Notification system**: SNS topic for chaos event notifications
- **Resource protection**: Tag-based resource exclusion
- **Dry run mode**: Test configurations without actual termination

### Security

- **Least privilege IAM**: Minimal required permissions
- **Safe mode**: Prevents actual resource termination during testing
- **Resource limits**: Maximum number of resources to terminate per run
- **Time windows**: Chaos only runs during specified time periods
- **Audit logging**: Comprehensive logging of all chaos events

### Documentation

- Complete README with usage examples
- Configuration documentation
- Safety guidelines and best practices
- Troubleshooting guide
- Contribution guidelines
- Security policy

### Testing

- Unit tests for all major functions
- Integration tests for chaos execution
- Example configuration tests
- Mock AWS services for testing
- Test coverage reporting

## [0.1.0] - 2023-12-15

### Added

- Initial development version
- Basic Lambda function structure
- EC2 instance detection and termination
- RDS instance detection and deletion
- ECS service detection and scaling
- Basic safety features
- Initial test framework

### Features

- **Basic chaos execution**: Simple resource termination logic
- **Environment variable configuration**: Basic configuration system
- **Error handling**: Basic error handling and logging
- **Mock testing**: Initial test structure with mocks

### Known Limitations

- Limited resource type support
- Basic safety mechanisms only
- No comprehensive monitoring
- Limited configuration options
- No SNS notifications
- No CloudWatch integration

## Future Releases

### Planned Features

- **Additional resource types**: Support for more AWS services
- **Multi-cloud support**: Azure and GCP resource termination
- **Advanced scheduling**: More sophisticated scheduling options
- **Resource dependency detection**: Avoid terminating dependent resources
- **Chaos experiment definitions**: Declarative chaos experiment configuration
- **Integration with chaos engineering platforms**: Integration with Gremlin, Chaos Monkey, etc.
- **Advanced monitoring**: More detailed metrics and alerting
- **Resource health checks**: Pre-chaos health validation
- **Rollback mechanisms**: Automatic rollback on chaos failure
- **Chaos experiment templates**: Pre-built chaos scenarios

### Improvements

- **Enhanced safety**: Additional safety mechanisms and validations
- **Better error handling**: More robust error handling and recovery
- **Performance optimization**: Optimized resource detection and termination
- **Documentation**: Enhanced documentation and examples
- **Testing**: More comprehensive test coverage
- **Security**: Enhanced security features and best practices

## Version History

### Development Timeline

- **2023-11-01**: Project conception and planning
- **2023-11-15**: Initial development started
- **2023-12-01**: Basic functionality implemented
- **2023-12-15**: Version 0.1.0 released
- **2023-12-20**: Enhanced safety features added
- **2023-12-25**: Monitoring and notifications implemented
- **2024-01-01**: Version 1.0.0 released

### Breaking Changes

- No breaking changes in 1.0.0
- Future breaking changes will be documented with migration guides

### Migration Notes

- No migration required for 1.0.0
- Future migrations will include detailed instructions

---

## Changelog Guidelines

### Version Numbering

We use semantic versioning:

- **MAJOR.MINOR.PATCH**
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Change Types

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon to be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security-related changes

### Release Notes

Each release includes:

- Summary of changes
- Migration instructions (if applicable)
- Known issues
- Security considerations
- Upgrade instructions

For detailed information about any release, please refer to the GitHub releases page.

---

**Note**: This changelog is maintained for transparency and to help users understand the evolution of the Chaos Monkey project. Always review release notes before upgrading in production environments.
