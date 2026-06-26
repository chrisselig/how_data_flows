"""Lesson: Why Finance and HR Never Agree on Headcount."""

from app.components.lesson import render_lesson
from src.data.examples import lesson_headcount_disagreement
from src.gamification.progress import UserProgress


def render(progress: UserProgress, total_lessons: int) -> None:
    """Render the headcount disagreement lesson."""
    render_lesson(lesson_headcount_disagreement(), progress, total_lessons)
