"""Lesson: The People Between the Systems."""

from app.components.lesson import render_lesson
from src.data.examples import lesson_human_handoffs
from src.gamification.progress import UserProgress


def render(progress: UserProgress, total_lessons: int) -> None:
    """Render the human handoffs lesson."""
    render_lesson(lesson_human_handoffs(), progress, total_lessons)
