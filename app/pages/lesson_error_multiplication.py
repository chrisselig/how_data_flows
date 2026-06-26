"""Lesson: The Telephone Game: How Small Errors Multiply."""

from app.components.lesson import render_lesson
from src.data.examples import lesson_error_multiplication
from src.gamification.progress import UserProgress


def render(progress: UserProgress, total_lessons: int) -> None:
    """Render the error multiplication lesson."""
    render_lesson(lesson_error_multiplication(), progress, total_lessons)
