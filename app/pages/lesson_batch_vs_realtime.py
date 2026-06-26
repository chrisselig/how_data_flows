"""Lesson: Batch vs Real-Time: When Timing Matters."""

from app.components.lesson import render_lesson
from src.data.examples import lesson_batch_vs_realtime
from src.gamification.progress import UserProgress


def render(progress: UserProgress, total_lessons: int) -> None:
    """Render the batch vs real-time lesson."""
    render_lesson(lesson_batch_vs_realtime(), progress, total_lessons)
