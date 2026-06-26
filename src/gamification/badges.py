"""Badge definitions and trigger logic for How Data Flows."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Badge:
    """An achievement badge."""

    id: str
    name: str
    icon: str
    description: str


ALL_BADGES: list[Badge] = [
    Badge("first_lesson", "First Steps", "🎯", "Completed your first lesson."),
    Badge("perfect_quiz", "Quiz Whiz", "🧠", "Scored 100% on a quiz."),
    Badge("halfway", "Halfway There", "🌗", "Completed half of all lessons."),
    Badge("all_lessons", "Data Detective", "🕵️", "Completed every lesson."),
    Badge(
        "pipeline_thinker", "Pipeline Thinker", "🔄", "Scored 100% on the data flow tracing quiz."
    ),
    Badge("source_of_truth", "Source of Truth", "📌", "Completed lessons 5 and 8."),
]

BADGE_LOOKUP: dict[str, Badge] = {b.id: b for b in ALL_BADGES}


def check_new_badges(
    completed_ids: set[str],
    quiz_scores: dict[str, int],
    current_badges: set[str],
    total_lessons: int,
) -> list[Badge]:
    """Return any badges newly earned."""
    newly_earned: list[Badge] = []

    def earn(badge_id: str) -> None:
        if badge_id not in current_badges:
            badge = BADGE_LOOKUP.get(badge_id)
            if badge:
                newly_earned.append(badge)

    if len(completed_ids) >= 1:
        earn("first_lesson")

    if any(score == 100 for score in quiz_scores.values()):
        earn("perfect_quiz")

    if total_lessons > 0 and len(completed_ids) >= total_lessons // 2:
        earn("halfway")

    if total_lessons > 0 and len(completed_ids) >= total_lessons:
        earn("all_lessons")

    # Pipeline Thinker: perfect score on trace_problem quiz
    if quiz_scores.get("trace_problem", 0) == 100:
        earn("pipeline_thinker")

    # Source of Truth: complete both lessons 5 and 8
    if "single_source" in completed_ids and "trace_problem" in completed_ids:
        earn("source_of_truth")

    return newly_earned
