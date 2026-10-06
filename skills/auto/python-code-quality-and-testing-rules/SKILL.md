---
name: python-code-quality-and-testing-rules
description: Use when modifying Python packages, adding bug fixes, or writing tests.
---
# Python Code Quality and Testing Rules

- **Do Not Modify Original Tests:** Never edit existing test files provided in the repository. Add new test files (e.g., `tests/test_regressions.py`) if additional tests are needed.
- **Type Annotations:** Ensure *every* public function (any function whose name does not start with an underscore `_`) has explicit type annotations on all parameters and on its return value.
- **Regression Tests:** Add a regression test file (`tests/test_regressions.py`) containing at least one test function per fixed bug (minimum 3 tests total), and verify that all tests pass.
- **Changelog Updates:** Record each bug fix in `CHANGELOG.md` under the heading `## Unreleased` as a bullet point in the format `- fix(<function name>): <short description>` (at least 3 bullets).