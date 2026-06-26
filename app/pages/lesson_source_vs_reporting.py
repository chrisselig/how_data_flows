"""Lesson: Source Systems vs Reporting Systems."""

from app.components.lesson import render_lesson
from src.data.examples import lesson_source_vs_reporting
from src.gamification.progress import UserProgress


def render(progress: UserProgress, total_lessons: int) -> None:
    """Render the source vs reporting lesson."""
    render_lesson(lesson_source_vs_reporting(), progress, total_lessons)
