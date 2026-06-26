"""Sidebar component with navigation, progress, and badges."""

from __future__ import annotations

import streamlit as st

from src.gamification.badges import ALL_BADGES
from src.gamification.progress import UserProgress
from src.models.lesson_model import Lesson


def render_sidebar(
    lessons: list[Lesson],
    progress: UserProgress,
) -> str | None:
    """Render the sidebar and return the selected lesson ID."""
    with st.sidebar:
        st.title("How Data Flows")
        st.caption("Where does your data go after you hit Save?")

        _render_progress_bar(progress)
        st.markdown("---")
        selected = _render_lesson_nav(lessons, progress)
        st.markdown("---")
        _render_badges(progress)

    return selected


def _render_progress_bar(progress: UserProgress) -> None:
    """Show XP bar and level."""
    st.markdown(f"### {progress.level_icon()} {progress.level_title()}")
    st.progress(progress.progress_fraction())

    xp_remaining = progress.xp_to_next_level()
    if xp_remaining is not None:
        st.caption(f"{progress.total_xp} XP  |  {xp_remaining} XP to next level")
    else:
        st.caption(f"{progress.total_xp} XP  |  Max level reached!")


def _render_lesson_nav(lessons: list[Lesson], progress: UserProgress) -> str | None:
    """Render lesson navigation links. Returns selected lesson ID."""
    st.markdown("### Lessons")

    if st.button("Home", key="nav_home", use_container_width=True):
        st.session_state["selected_lesson"] = None

    st.markdown("---")

    for lesson in lessons:
        completed = lesson.id in progress.completed_lesson_ids
        check = " ✓" if completed else ""
        label = f"{lesson.icon} {lesson.title}{check}"

        if st.button(label, key=f"nav_{lesson.id}", use_container_width=True):
            st.session_state["selected_lesson"] = lesson.id

    return st.session_state.get("selected_lesson")


def _render_badges(progress: UserProgress) -> None:
    """Show earned and locked badges."""
    st.markdown("### Badges")

    if not progress.earned_badge_ids:
        st.caption("Complete lessons and quizzes to earn badges!")
        return

    for badge in ALL_BADGES:
        if badge.id in progress.earned_badge_ids:
            st.markdown(f"{badge.icon} **{badge.name}**")
        else:
            st.markdown(f"🔒 ~~{badge.name}~~")
