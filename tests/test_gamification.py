"""Tests for gamification logic."""

from src.gamification.badges import check_new_badges
from src.gamification.progress import UserProgress


def test_initial_progress() -> None:
    """New progress should start at zero."""
    p = UserProgress()
    assert p.total_xp == 0
    assert p.level_title() == "Newcomer"
    assert p.level_icon() == "🌱"
    assert len(p.completed_lesson_ids) == 0


def test_complete_lesson() -> None:
    """Completing a lesson should add XP."""
    p = UserProgress()
    p.complete_lesson("test_1", 25)
    assert p.total_xp == 25
    assert "test_1" in p.completed_lesson_ids


def test_no_double_xp() -> None:
    """Completing the same lesson twice should not double XP."""
    p = UserProgress()
    p.complete_lesson("test_1", 25)
    p.complete_lesson("test_1", 25)
    assert p.total_xp == 25


def test_level_progression() -> None:
    """XP should advance levels."""
    p = UserProgress()
    p.total_xp = 50
    assert p.level_title() == "Data Curious"
    p.total_xp = 200
    assert p.level_title() == "Data Navigator"


def test_xp_to_next_level() -> None:
    """Should return XP remaining to next level."""
    p = UserProgress()
    p.total_xp = 30
    assert p.xp_to_next_level() == 20  # Next threshold is 50


def test_max_level_returns_none() -> None:
    """Max level should return None for xp_to_next_level."""
    p = UserProgress()
    p.total_xp = 999
    assert p.xp_to_next_level() is None


def test_first_lesson_badge() -> None:
    """Completing first lesson should earn first_lesson badge."""
    badges = check_new_badges(
        completed_ids={"lesson_1"},
        quiz_scores={},
        current_badges=set(),
        total_lessons=8,
    )
    badge_ids = [b.id for b in badges]
    assert "first_lesson" in badge_ids


def test_perfect_quiz_badge() -> None:
    """Perfect quiz score should earn quiz_whiz badge."""
    badges = check_new_badges(
        completed_ids={"lesson_1"},
        quiz_scores={"lesson_1": 100},
        current_badges={"first_lesson"},
        total_lessons=8,
    )
    badge_ids = [b.id for b in badges]
    assert "perfect_quiz" in badge_ids


def test_no_duplicate_badges() -> None:
    """Already-earned badges should not be returned."""
    badges = check_new_badges(
        completed_ids={"lesson_1"},
        quiz_scores={},
        current_badges={"first_lesson"},
        total_lessons=8,
    )
    badge_ids = [b.id for b in badges]
    assert "first_lesson" not in badge_ids


def test_record_quiz_improves_score() -> None:
    """Recording a higher quiz score should award bonus XP."""
    p = UserProgress()
    p.record_quiz("test_1", 50, 5)
    assert p.quiz_scores["test_1"] == 50
    assert p.total_xp == 5

    p.record_quiz("test_1", 100, 15)
    assert p.quiz_scores["test_1"] == 100
    assert p.total_xp == 20


def test_record_quiz_no_downgrade() -> None:
    """Lower quiz score should not replace higher one."""
    p = UserProgress()
    p.record_quiz("test_1", 100, 15)
    p.record_quiz("test_1", 50, 5)
    assert p.quiz_scores["test_1"] == 100
    assert p.total_xp == 15


def test_pipeline_thinker_badge() -> None:
    """Perfect score on trace_problem quiz should earn pipeline_thinker badge."""
    badges = check_new_badges(
        completed_ids={"trace_problem"},
        quiz_scores={"trace_problem": 100},
        current_badges={"first_lesson", "perfect_quiz"},
        total_lessons=8,
    )
    badge_ids = [b.id for b in badges]
    assert "pipeline_thinker" in badge_ids


def test_source_of_truth_badge() -> None:
    """Completing lessons 5 and 8 should earn source_of_truth badge."""
    badges = check_new_badges(
        completed_ids={"single_source", "trace_problem"},
        quiz_scores={},
        current_badges={"first_lesson"},
        total_lessons=8,
    )
    badge_ids = [b.id for b in badges]
    assert "source_of_truth" in badge_ids
