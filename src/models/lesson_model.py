"""Structured lesson data model.

Each lesson follows the teaching pattern:
  Concept -> Bad Data -> What Breaks -> Fixed Data
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass(frozen=True)
class QuizQuestion:
    """A single quiz question for a lesson."""

    question: str
    options: list[str]
    correct_index: int
    explanation: str


@dataclass(frozen=True)
class Lesson:
    """A single data governance lesson.

    Attributes:
        id: Unique lesson identifier (e.g. "job_titles").
        title: Display title shown to user.
        icon: Emoji icon for sidebar navigation.
        order: Sort position in lesson list.
        concept: Plain-language explanation of the principle.
        bad_data: DataFrame showing messy/inconsistent data.
        downstream_impact: Text explaining what breaks when data is bad.
        good_data: DataFrame showing the corrected version.
        body: Rich markdown lesson content (analogies, vocabulary, tips).
        body_sections: Body split into tabbed sections (auto-derived from body headers).
        quiz: Optional quiz questions for gamification.
        tip: Optional practical tip for the user.
    """

    id: str
    title: str
    icon: str
    order: int
    concept: str
    bad_data: pd.DataFrame
    downstream_impact: str
    good_data: pd.DataFrame
    body: str = ""
    body_sections: dict[str, str] = field(default_factory=dict)
    quiz: list[QuizQuestion] = field(default_factory=list)
    tip: str = ""

    def __post_init__(self) -> None:
        """Auto-derive body_sections from body markdown headers."""
        if self.body and not self.body_sections:
            sections: dict[str, str] = {}
            current_key = ""
            current_lines: list[str] = []
            for line in self.body.split("\n"):
                if line.startswith("### "):
                    if current_key:
                        sections[current_key] = "\n".join(current_lines).strip()
                    current_key = line[4:].strip()
                    current_lines = []
                else:
                    current_lines.append(line)
            if current_key:
                sections[current_key] = "\n".join(current_lines).strip()
            object.__setattr__(self, "body_sections", sections)
