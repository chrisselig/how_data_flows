"""Lesson: How to Trace a Data Problem Back to Its Source."""

from app.components.lesson import render_lesson
from src.data.examples import lesson_trace_problem
from src.gamification.progress import UserProgress


def render(progress: UserProgress, total_lessons: int) -> None:
    """Render the trace problem lesson."""
    render_lesson(lesson_trace_problem(), progress, total_lessons)
