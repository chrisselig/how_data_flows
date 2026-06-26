"""Reusable lesson rendering component for Streamlit.

Renders the standard teaching pattern:
  Concept -> Body tabs -> Spot the Problem -> Reveal -> Before/After -> Quiz
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from app.components.feedback import render_feedback
from src.gamification.badges import check_new_badges
from src.gamification.progress import UserProgress
from src.models.lesson_model import Lesson, QuizQuestion

XP_PER_LESSON = 25
XP_PER_PERFECT_QUIZ = 15
XP_PER_QUIZ_QUESTION = 5


def render_lesson(lesson: Lesson, progress: UserProgress, total_lessons: int) -> None:
    """Render a full lesson page using the interactive teaching pattern."""
    already_completed = lesson.id in progress.completed_lesson_ids

    st.title(f"{lesson.icon} {lesson.title}")

    if already_completed:
        st.success("You've completed this lesson!")

    _render_concept(lesson.concept)

    if lesson.body_sections:
        _render_body_sections(lesson.body_sections)
    elif lesson.body:
        st.markdown(lesson.body)

    _render_spot_the_problem(lesson, already_completed)

    reveal_key = f"reveal_{lesson.id}_shown"
    revealed = already_completed or st.session_state.get(reveal_key, False)

    if revealed:
        _render_downstream_impact(lesson.downstream_impact)
        _render_data_comparison(lesson.bad_data, lesson.good_data)

        if lesson.tip:
            _render_tip(lesson.tip)

        if lesson.quiz:
            _render_quiz(lesson, progress, total_lessons)

        if not already_completed:
            _render_completion_button(lesson, progress, total_lessons)

    _render_feedback(lesson)


def _render_feedback(lesson: Lesson) -> None:
    """Render the feedback form at the bottom of every lesson."""
    st.markdown("---")
    render_feedback(course_id="how_data_flows", lesson_id=lesson.id)


def _render_concept(concept: str) -> None:
    """Render the concept explanation section."""
    st.header("The Concept")
    st.info(concept)


def _render_body_sections(sections: dict[str, str]) -> None:
    """Render body content as interactive tabs."""
    tabs = st.tabs(list(sections.keys()))
    for tab, content in zip(tabs, sections.values()):
        with tab:
            st.markdown(content)


def _render_spot_the_problem(lesson: Lesson, already_completed: bool) -> None:
    """Render bad data table with a reveal button for the answer."""
    st.header("Spot the Problem")
    st.markdown("Look at this data. **Can you spot what's wrong?**")
    st.dataframe(lesson.bad_data, use_container_width=True, hide_index=True)

    reveal_key = f"reveal_{lesson.id}_shown"
    if not already_completed and not st.session_state.get(reveal_key, False):
        if st.button("Reveal What's Wrong", key=f"reveal_{lesson.id}"):
            st.session_state[reveal_key] = True
            st.rerun()


def _render_downstream_impact(impact_text: str) -> None:
    """Render the downstream business impact section."""
    st.header("What Breaks Downstream")
    st.markdown("**Remember:** Bad Data → Bad Report → Bad Decisions")
    st.error(impact_text)


def _render_data_comparison(bad_df: pd.DataFrame, good_df: pd.DataFrame) -> None:
    """Render bad and good data as a before/after tab toggle."""
    st.header("Before & After")
    before_tab, after_tab = st.tabs(["Before (Bad Data)", "After (Fixed Data)"])
    with before_tab:
        st.dataframe(bad_df, use_container_width=True, hide_index=True)
    with after_tab:
        st.dataframe(good_df, use_container_width=True, hide_index=True)


def _render_tip(tip: str) -> None:
    """Render a practical tip callout."""
    st.markdown("---")
    st.markdown(f"**Practical Tip:** {tip}")


def _render_quiz(lesson: Lesson, progress: UserProgress, total_lessons: int) -> None:
    """Render the quiz section with scoring."""
    st.markdown("---")
    st.header("Quick Quiz")
    st.markdown("Test your understanding. Pick the best answer for each question.")

    quiz_key = f"quiz_{lesson.id}"
    correct_count = 0
    total_questions = len(lesson.quiz)
    all_answered = True

    for i, q in enumerate(lesson.quiz):
        _render_quiz_question(q, i, quiz_key)
        selected = st.session_state.get(f"{quiz_key}_{i}")
        if selected is None:
            all_answered = False
        elif selected == q.options[q.correct_index]:
            correct_count += 1

    if all_answered:
        submitted_key = f"{quiz_key}_submitted"
        if st.button("Check Answers", key=f"btn_{quiz_key}"):
            st.session_state[submitted_key] = True

        if st.session_state.get(submitted_key):
            _show_quiz_results(lesson, progress, total_lessons, correct_count, total_questions)


def _render_quiz_question(question: QuizQuestion, index: int, quiz_key: str) -> None:
    """Render a single quiz question."""
    st.radio(
        question.question,
        options=question.options,
        key=f"{quiz_key}_{index}",
        index=None,
    )


def _show_quiz_results(
    lesson: Lesson,
    progress: UserProgress,
    total_lessons: int,
    correct: int,
    total: int,
) -> None:
    """Show quiz results and award XP."""
    score_pct = int((correct / total) * 100) if total > 0 else 0
    st.markdown(f"**Score: {correct}/{total} ({score_pct}%)**")

    if score_pct == 100:
        st.balloons()
        st.success("Perfect score!")
    elif score_pct >= 50:
        st.warning("Good effort! Review the explanations below.")
    else:
        st.error("Keep learning! Review the lesson and try again.")

    for i, q in enumerate(lesson.quiz):
        with st.expander(f"Question {i + 1} — Explanation"):
            st.markdown(f"**Correct answer:** {q.options[q.correct_index]}")
            st.markdown(q.explanation)

    prev_score = progress.quiz_scores.get(lesson.id, 0)
    if score_pct > prev_score:
        bonus = XP_PER_PERFECT_QUIZ if score_pct == 100 else (correct * XP_PER_QUIZ_QUESTION)
        progress.record_quiz(lesson.id, score_pct, bonus)
        st.toast(f"+{bonus} XP for quiz!")

        new_badges = check_new_badges(
            progress.completed_lesson_ids,
            progress.quiz_scores,
            progress.earned_badge_ids,
            total_lessons,
        )
        for badge in new_badges:
            progress.earned_badge_ids.add(badge.id)
            st.toast(f"Badge earned: {badge.icon} {badge.name}")


def _render_completion_button(lesson: Lesson, progress: UserProgress, total_lessons: int) -> None:
    """Render the lesson completion button."""
    st.markdown("---")
    if st.button("Mark Lesson Complete", key=f"complete_{lesson.id}", type="primary"):
        progress.complete_lesson(lesson.id, XP_PER_LESSON)
        st.toast(f"+{XP_PER_LESSON} XP!")

        new_badges = check_new_badges(
            progress.completed_lesson_ids,
            progress.quiz_scores,
            progress.earned_badge_ids,
            total_lessons,
        )
        for badge in new_badges:
            progress.earned_badge_ids.add(badge.id)
            st.toast(f"Badge earned: {badge.icon} {badge.name}")

        st.rerun()
