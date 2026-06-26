"""Tests for lesson data generation."""

import pandas as pd

from src.data.examples import get_all_lessons


def test_all_lessons_load() -> None:
    """All lessons should load without errors."""
    lessons = get_all_lessons()
    assert len(lessons) == 8


def test_lessons_ordered() -> None:
    """Lessons should be sorted by order field."""
    lessons = get_all_lessons()
    orders = [lesson.order for lesson in lessons]
    assert orders == sorted(orders)


def test_unique_ids() -> None:
    """Every lesson should have a unique ID."""
    lessons = get_all_lessons()
    ids = [lesson.id for lesson in lessons]
    assert len(ids) == len(set(ids))


def test_dataframes_not_empty() -> None:
    """Bad and good DataFrames should have data."""
    for lesson in get_all_lessons():
        assert isinstance(lesson.bad_data, pd.DataFrame)
        assert isinstance(lesson.good_data, pd.DataFrame)
        assert len(lesson.bad_data) > 0
        assert len(lesson.good_data) > 0


def test_lessons_have_body() -> None:
    """Every lesson should have rich body content."""
    for lesson in get_all_lessons():
        assert lesson.body, f"Lesson '{lesson.id}' is missing body content"


def test_lessons_have_body_sections() -> None:
    """Every lesson should have body_sections auto-derived from body."""
    for lesson in get_all_lessons():
        assert lesson.body_sections, f"Lesson '{lesson.id}' is missing body_sections"
        assert isinstance(lesson.body_sections, dict)


def test_body_sections_have_expected_keys() -> None:
    """Body sections should contain the standard tab keys."""
    expected_keys = {
        "Why This Matters",
        "Key Vocabulary",
        "How to Spot It",
        "Common Mistakes",
        "How to Fix It",
    }
    for lesson in get_all_lessons():
        actual_keys = set(lesson.body_sections.keys())
        assert actual_keys == expected_keys, (
            f"Lesson '{lesson.id}' has unexpected section keys: "
            f"missing={expected_keys - actual_keys}, extra={actual_keys - expected_keys}"
        )


def test_quiz_questions_valid() -> None:
    """Quiz questions should have valid correct_index."""
    for lesson in get_all_lessons():
        for q in lesson.quiz:
            assert 0 <= q.correct_index < len(q.options)
