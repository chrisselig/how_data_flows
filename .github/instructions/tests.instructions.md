---
applyTo: tests/**/*.py
---

# Test Instructions

## Framework
- pytest with pythonpath configured in pyproject.toml
- Tests run from project root: `.venv/bin/pytest -v`

## Test Structure
- `test_examples.py` — validates lesson data integrity (counts, ordering, required fields, quiz validity)
- `test_gamification.py` — validates XP, levels, badges, and quiz scoring logic

## Standards
- Type hints on all test functions (return `-> None`)
- Descriptive docstrings explaining what each test verifies
- Test both happy paths and edge cases (double completion, score downgrade, max level)
- No mocking of Streamlit — test business logic only

## Adding Tests
When adding a new lesson, existing tests should pass automatically if the lesson follows the required pattern. Add specific tests only for unique badge triggers or custom gamification logic.
