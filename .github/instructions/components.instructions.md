---
applyTo: app/components/**/*.py
---

# Component Instructions

## Purpose
Reusable Streamlit UI components. No business logic — only rendering.

## Key Components

### `lesson.py`
- `render_lesson()` is the single entry point for rendering any lesson
- Follows the teaching pattern: Concept → Body tabs → Spot the Problem → Reveal → Before/After → Quiz
- Handles XP awards, badge checks, and quiz scoring
- All lesson data comes from the `Lesson` dataclass — no hardcoded content

### `sidebar.py`
- Renders navigation, progress bar, and badges
- Returns the selected lesson ID
- Uses `st.session_state` for navigation state

## Rules
- No business logic in components — delegate to `src/` modules
- Use `st.session_state` for UI state management
- All text content comes from dataclass fields, not hardcoded strings
- Use Streamlit's built-in components (st.tabs, st.expander, st.dataframe)
