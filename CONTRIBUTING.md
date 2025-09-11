# Contributing to Digital Me Community Edition

tl;dr

- Sign your commits with DCO (Developer Certificate of Origin)
- Include a component `prefix:` in your commit message (e.g., `sdk:`, `cli:`, `docs:`)
- Squash fixup commits and force push to your branch
- Follow our code style and testing guidelines

## Getting Started

First, fork the repository on GitHub to your personal account.

```bash
git clone https://github.com/YOURORG/digital-me-community.git && cd digital-me-community

# prevent accidentally pushing to YOURORG/digital-me-community
git config push.default nothing
git remote rename origin upstream

# add your fork (replace $USER with your GitHub username)
git remote add $USER git@github.com:$USER/digital-me-community.git

git fetch -av
```

## Contribution Flow

This is a rough outline of what a contributor's workflow looks like:

- Create an issue describing the feature/fix
- Create a topic branch from where you want to base your work
- Make commits of logical units
- [Sign](#sign-off-your-work) your commits with DCO
- Make sure your commit messages are in the proper format (see below)
- Push your changes to a topic branch in your fork of the repository
- Submit a pull request to `YOURORG/digital-me-community`

See [below](#format-of-the-commit-message) for details on commit best practices and **supported prefixes**.

### Sign-off Your Work

We use the [Developer Certificate of Origin](https://developercertificate.org/) (DCO) for all contributions. By adding the DCO sign-off line to their commit messages, contributors certify that they have the right to submit their changes under the project's license.

Git provides the `-s` command-line option to append the required line automatically:

```bash
git commit -s -m 'sdk: Add new plugin lifecycle method'
```

For an existing commit, you can also use this option with `--amend`:

```bash
git commit -s --amend
```

### Example Workflows

#### Example 1 - Fix a Bug in the SDK

```bash
git checkout -b fix-issue-123 main
# make your changes
git add .
git commit -s -m "sdk: Fix plugin initialization race condition" -m "Closes: #123"
git push $USER fix-issue-123
```

#### Example 2 - Add a New Plugin Example

```bash
git checkout -b add-weather-plugin main
# create the new plugin example
git add examples/plugins/weather_assistant/
git commit -s -m "examples: Add weather assistant plugin" -m "Closes: #456"
git push $USER add-weather-plugin
```

#### Example 3 - Improve CLI Tools

```bash
git checkout -b enhance-cli main
# implement CLI improvements
git add tools/cli/
git commit -s -m "cli: Add plugin validation command" -m "Closes: #789"
git push $USER enhance-cli
```

#### Example 4 - Update Documentation

```bash
git checkout -b update-docs main
# improve documentation
git add docs/
git commit -s -m "docs: Add plugin development tutorial" -m "Closes: #101"
git push $USER update-docs
```

### Stay in Sync with Upstream

When your branch gets out of sync with the main branch, use the following to update (rebase):

```bash
git checkout fix-issue-123
git fetch -a
git rebase upstream/main
git push --force-with-lease $USER fix-issue-123
```

### Updating Pull Requests

If your PR fails CI or needs changes based on code review, you can add fixup commits:

```bash
# incorporate review feedback
git add .
git commit -s --fixup HEAD
git push $USER fix-issue-123
```

Once the review is complete, squash your commits:

```bash
git rebase -i --autosquash upstream/main
git push --force-with-lease $USER fix-issue-123
```

## Code Style

### Python

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- Line length: 100 characters (not 79)
- Use `black` for code formatting
- Use `isort` for import sorting
- Use `flake8` for linting
- Use `mypy` for type checking

Run the following commands before submitting:

```bash
# Format code
black .
isort .

# Check style and types
flake8 .
mypy .

# Run tests
pytest
```

### Documentation

- Use [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Include type hints for all public APIs
- Add examples to docstrings for complex functions
- Keep line width to 100 characters for both code and markdown

## Testing Guidelines

### Unit Tests

- Write tests for all new functionality
- Use `pytest` as the testing framework
- Aim for >90% code coverage
- Mock external dependencies (LLM APIs, databases, etc.)

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=digital_me_sdk --cov-report=html
```

### Integration Tests

- Test plugin loading and execution
- Test CLI commands end-to-end
- Use Docker containers for isolated testing
- Mark slow tests with `@pytest.mark.slow`

```bash
# Run integration tests
pytest tests/integration/

# Run all tests including slow ones
pytest -m "not slow" # fast tests only
pytest # all tests
```

## Format of the Commit Message

We follow the conventions from [Conventional Commits](https://www.conventionalcommits.org/) with component prefixes.

Be sure to include any related GitHub issue references in the commit message, e.g., `Closes: #123`.

The commit message format helps generate our [CHANGELOG](CHANGELOG.md) and release notes automatically.

### Supported Prefixes

Currently the following prefixes are used:

- `sdk:` - Changes to the core SDK
- `cli:` - Changes to CLI tools
- `examples:` - Changes to example plugins
- `docs:` - Documentation updates
- `ci:` - CI/CD pipeline changes
- `test:` - Test-only changes
- `fix:` - Bug fixes
- `feat:` - New features
- `chore:` - Maintenance tasks

### Examples

```bash
# Feature addition
git commit -s -m "sdk: Add async plugin execution support" -m "Closes: #123"

# Bug fix
git commit -s -m "fix: Resolve memory leak in plugin lifecycle" -m "Closes: #456"

# Documentation update
git commit -s -m "docs: Add plugin development quickstart guide"

# Breaking change
git commit -s -m "sdk: Change plugin interface signature" -m "BREAKING: Plugin.execute() now requires context parameter"
```

## Submitting Bug Reports and Feature Requests

Please submit bug reports and feature requests using our GitHub [Issues](https://github.com/YOURORG/digital-me-community/issues).

### Bug Reports

Before submitting a bug report, please:

1. Check existing issues to avoid duplicates
2. Include version information (`digital-me --version`)
3. Provide minimal reproduction steps
4. Include relevant logs and error messages
5. Specify your environment (OS, Python version, etc.)

### Feature Requests

Feature requests should:

1. Explain the use case and problem being solved
2. Describe the proposed solution
3. Consider backward compatibility
4. Include examples of how the feature would be used

## Development Environment Setup

### Prerequisites

- Python 3.8+
- Docker (for integration tests)
- Git

### Setup

```bash
# Clone your fork
git clone https://github.com/$USER/digital-me-community.git
cd digital-me-community

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Verify setup
digital-me --version
pytest --version
```

### Running CI Checks Locally

You can run the same checks that CI runs:

```bash
# Code formatting and linting
make lint

# Type checking
make typecheck

# Security scanning
make security

# All tests
make test

# Integration tests (requires Docker)
make test-integration
```

## Community Guidelines

### Code of Conduct

This project adheres to our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

### Communication

- Use GitHub Issues for bug reports and feature requests
- Use GitHub Discussions for questions and general discussion
- Be respectful and constructive in all interactions
- Help newcomers get started

### Recognition

Contributors who make significant contributions will be:

- Added to the [AUTHORS](AUTHORS.md) file
- Mentioned in release notes
- Invited to join the maintainer team (for exceptional contributors)

## Release Process

Releases are handled by the maintainer team:

1. Version bumps follow semantic versioning
2. Releases are tagged and published automatically via CI
3. Release notes are generated from commit messages
4. PyPI packages are published automatically

## Questions?

If you have questions about contributing, please:

1. Check our [documentation](https://yourorg.github.io/digital-me-community/)
2. Search existing [GitHub Issues](https://github.com/YOURORG/digital-me-community/issues)
3. Start a [GitHub Discussion](https://github.com/YOURORG/digital-me-community/discussions)
4. Contact the maintainers via the issue tracker

Thank you for contributing to Digital Me Community Edition!
