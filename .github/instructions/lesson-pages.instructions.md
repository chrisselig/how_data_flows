---
applyTo: app/pages/lesson_*.py
---

# Lesson Page Instructions

## Pattern
Every lesson page follows this exact template:

```python
"""Lesson: <Title>."""

from app.components.lesson import render_lesson
from src.data.examples import lesson_<id>
from src.gamification.progress import UserProgress


def render(progress: UserProgress, total_lessons: int) -> None:
    """Render the <title> lesson."""
    render_lesson(lesson_<id>(), progress, total_lessons)
```

## Rules
- Lesson pages are thin wrappers — NO business logic
- They call `render_lesson()` with the lesson data from `examples.py`
- Must be registered in `app/pages/registry.py`
- Function must be named `render` with signature `(UserProgress, int) -> None`
