"""Lesson: Your Data Has a Life After You."""

from app.components.lesson import render_lesson
from src.data.examples import lesson_data_life
from src.gamification.progress import UserProgress


def render(progress: UserProgress, total_lessons: int) -> None:
    """Render the data life lesson."""
    render_lesson(lesson_data_life(), progress, total_lessons)
