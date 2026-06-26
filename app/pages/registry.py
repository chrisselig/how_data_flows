"""Lesson page registry."""

from __future__ import annotations

from typing import Callable

from app.pages import (
    lesson_batch_vs_realtime,
    lesson_data_life,
    lesson_error_multiplication,
    lesson_headcount_disagreement,
    lesson_human_handoffs,
    lesson_single_source,
    lesson_source_vs_reporting,
    lesson_trace_problem,
)
from src.gamification.progress import UserProgress

RenderFunc = Callable[[UserProgress, int], None]

LESSON_PAGES: dict[str, RenderFunc] = {
    "data_life": lesson_data_life.render,
    "source_vs_reporting": lesson_source_vs_reporting.render,
    "headcount_disagreement": lesson_headcount_disagreement.render,
    "error_multiplication": lesson_error_multiplication.render,
    "single_source": lesson_single_source.render,
    "batch_vs_realtime": lesson_batch_vs_realtime.render,
    "human_handoffs": lesson_human_handoffs.render,
    "trace_problem": lesson_trace_problem.render,
}
