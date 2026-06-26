# How Data Flows — Copilot Instructions

## What This Is

Interactive Streamlit course teaching non-technical HR users how employee data flows through organizational systems. Part of the HR Analytics Academy.

## Architecture

Strict separation of concerns:
- `app/` — Streamlit UI only (no business logic)
- `src/` — business logic (data, models, gamification)
- `tests/` — pytest tests

## Commands

```bash
streamlit run app/main.py     # Run app
.venv/bin/pytest -v            # Run tests
.venv/bin/ruff check .         # Lint
.venv/bin/ruff format .        # Format
```

## Lesson Pattern (MANDATORY)

Every lesson follows this exact structure:
1. Concept — plain-language principle
2. Body with 5 tabbed sections: Why This Matters, Key Vocabulary, How to Spot It, Common Mistakes, How to Fix It
3. Bad data — DataFrame with realistic HR data showing the problem
4. What breaks downstream — business impact starting with "**What breaks:**"
5. Good data — corrected DataFrame
6. Quiz — 2 multiple choice questions
7. Tip — practical advice

Core principle: **Bad Data → Bad Report → Bad Decisions**

## Adding a New Lesson

1. Add a builder function in `src/data/examples.py` returning a `Lesson`
2. Add the builder to `get_all_lessons()`
3. Create a page file in `app/pages/lesson_<name>.py` (follow existing pattern)
4. Register in `app/pages/registry.py`

## Key Dataclasses

- `Lesson` — id, title, icon, order, concept, bad_data, downstream_impact, good_data, body, quiz, tip
- `QuizQuestion` — question, options, correct_index, explanation
- `UserProgress` — total_xp, completed_lesson_ids, earned_badge_ids, quiz_scores
- `Badge` — id, name, icon, description

## Gamification System

- XP: 25 per lesson completion, 5 per quiz question, 15 bonus for perfect quiz
- Levels: Newcomer (0) → Data Curious (50) → Flow Tracker (100) → Pipeline Thinker (150) → Data Navigator (200)
- 6 badges with trigger conditions in `badges.py`

## Coding Standards

- Type hints on all functions
- DRY, SOLID, KISS
- No hardcoding in UI — all lesson data lives in `src/data/examples.py`
- Lesson pages are thin wrappers calling `render_lesson()`
- Keep language simple — audience is non-technical HR users
