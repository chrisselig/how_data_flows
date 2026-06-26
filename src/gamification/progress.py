"""Session-scoped user progress state for How Data Flows."""

from __future__ import annotations

from dataclasses import dataclass, field

LEVEL_THRESHOLDS: list[tuple[int, str, str]] = [
    (0, "Newcomer", "🌱"),
    (50, "Data Curious", "🔍"),
    (100, "Flow Tracker", "🔄"),
    (150, "Pipeline Thinker", "🔧"),
    (200, "Data Navigator", "🧭"),
]


@dataclass
class UserProgress:
    """Mutable state for a single user's session."""

    total_xp: int = 0
    completed_lesson_ids: set[str] = field(default_factory=set)
    earned_badge_ids: set[str] = field(default_factory=set)
    quiz_scores: dict[str, int] = field(default_factory=dict)
    alias: str = ""

    def level_title(self) -> str:
        """Return current level title based on XP."""
        title = LEVEL_THRESHOLDS[0][1]
        for threshold, name, _ in LEVEL_THRESHOLDS:
            if self.total_xp >= threshold:
                title = name
        return title

    def level_icon(self) -> str:
        """Return current level icon based on XP."""
        icon = LEVEL_THRESHOLDS[0][2]
        for threshold, _, ico in LEVEL_THRESHOLDS:
            if self.total_xp >= threshold:
                icon = ico
        return icon

    def xp_to_next_level(self) -> int | None:
        """Return XP needed for next level, or None if max."""
        for threshold, _, _ in LEVEL_THRESHOLDS:
            if threshold > self.total_xp:
                return threshold - self.total_xp
        return None

    def progress_fraction(self) -> float:
        """Return 0.0-1.0 progress toward next level."""
        prev_threshold = 0
        for threshold, _, _ in LEVEL_THRESHOLDS:
            if threshold > self.total_xp:
                span = threshold - prev_threshold
                return (self.total_xp - prev_threshold) / span if span else 1.0
            prev_threshold = threshold
        return 1.0

    def complete_lesson(self, lesson_id: str, xp: int) -> None:
        """Mark a lesson as completed and award XP."""
        if lesson_id not in self.completed_lesson_ids:
            self.completed_lesson_ids.add(lesson_id)
            self.total_xp += xp

    def record_quiz(self, lesson_id: str, score: int, bonus_xp: int) -> None:
        """Record a quiz score and award bonus XP."""
        prev = self.quiz_scores.get(lesson_id, 0)
        if score > prev:
            self.quiz_scores[lesson_id] = score
            self.total_xp += bonus_xp
