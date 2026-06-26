"""How Data Flows — Streamlit entry point.

Run with:
    streamlit run app/main.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import streamlit as st  # noqa: E402

from app.components.sidebar import render_sidebar  # noqa: E402
from app.pages.registry import LESSON_PAGES  # noqa: E402
from src.data.examples import get_all_lessons  # noqa: E402
from src.gamification.progress import UserProgress  # noqa: E402


def main() -> None:
    """Application entry point."""
    st.set_page_config(
        page_title="How Data Flows",
        page_icon="🔄",
        layout="wide",
    )

    _init_session_state()

    lessons = get_all_lessons()
    progress: UserProgress = st.session_state["progress"]

    selected_id = render_sidebar(lessons, progress)

    if selected_id and selected_id in LESSON_PAGES:
        LESSON_PAGES[selected_id](progress, len(lessons))
    else:
        _render_home(lessons, progress)


def _init_session_state() -> None:
    """Initialize session state on first load."""
    if "progress" not in st.session_state:
        st.session_state["progress"] = UserProgress()
    if "selected_lesson" not in st.session_state:
        st.session_state["selected_lesson"] = None


def _render_home(lessons: list, progress: UserProgress) -> None:
    """Render the home/welcome page."""
    st.title("How Data Flows Through Your Organization")

    st.markdown(
        "Every time you save an employee record, it starts a journey through multiple systems. "
        "Payroll reads it. Benefits reads it. Finance counts heads from it. "
        "This course shows you where your data goes — and why accuracy at the source matters."
    )

    st.info(
        "**The #1 Rule:** Bad Data → Bad Report → Bad Decisions\n\n"
        "Your one typo becomes everyone's problem downstream."
    )

    st.markdown("### Your Progress")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Lessons Completed", f"{len(progress.completed_lesson_ids)}/{len(lessons)}")
    with col2:
        st.metric("Total XP", progress.total_xp)
    with col3:
        st.metric("Badges Earned", len(progress.earned_badge_ids))

    st.markdown("### Lessons")
    st.markdown("Click a lesson in the sidebar to get started, or pick one below:")

    cols = st.columns(2)
    for i, lesson in enumerate(lessons):
        completed = lesson.id in progress.completed_lesson_ids
        status = " ✓" if completed else ""
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"#### {lesson.icon} {lesson.title}{status}")
                preview = (
                    lesson.concept[:120] + "..." if len(lesson.concept) > 120 else lesson.concept
                )
                st.caption(preview)
                if st.button("Start", key=f"home_{lesson.id}"):
                    st.session_state["selected_lesson"] = lesson.id
                    st.rerun()


if __name__ == "__main__":
    main()
