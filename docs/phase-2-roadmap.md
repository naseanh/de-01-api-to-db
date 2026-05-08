# Phase 2 Roadmap

## Objective

Phase 2 focuses on improving pipeline reliability, testability,
observability, and operational resilience.

## Completed Enhancements

- Added pytest testing framework
- Added transform unit tests
- Added pipeline orchestration tests
- Added API timeout handling
- Added retry logic with exponential backoff
- Replaced print statements with structured logging
- Centralized pytest/pylint configuration using pyproject.toml
- Expanded GitHub Actions CI validation
- Add additional negative-path testing
- Improve operational troubleshooting documentation

## Remaining Goals

- Improve exception handling
- Expand SQL query examples

## Engineering Concepts Practiced

- Unit testing
- Mocking external dependencies
- Retry/backoff strategies
- Timeout handling
- Structured logging
- CI/CD validation
- Test isolation
- Failure injection testing
