"""Lesson: What 'Single Source of Truth' Actually Means."""

from app.components.lesson import render_lesson
from src.data.examples import lesson_single_source
from src.gamification.progress import UserProgress


def render(progress: UserProgress, total_lessons: int) -> None:
    """Render the single source of truth lesson."""
    render_lesson(lesson_single_source(), progress, total_lessons)
