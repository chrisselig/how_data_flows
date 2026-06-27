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

from app._pages.registry import LESSON_PAGES  # noqa: E402
from app.components.sidebar import render_sidebar  # noqa: E402
from src.certificate import CertificateData, generate_certificate_pdf  # noqa: E402
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
    # -- Corporate header banner -----------------------------------------------
    st.markdown(
        """
        <div style="border-bottom: 3px solid #2980B9; padding-bottom: 1rem;
                    margin-bottom: 1.5rem;">
            <h1 style="color: #1B4F72; margin: 0 0 0.3rem 0;
                       font-size: 1.8rem;">
                How Data Flows Through Your Organization
            </h1>
            <p style="color: #5D6D7E; font-size: 1rem; margin: 0;">
                Every time you save an employee record, it starts a journey
                through multiple systems. Payroll reads it. Benefits reads it.
                Finance counts heads from it. This course shows you where your
                data goes — and why accuracy at the source matters.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "**The #1 Rule:** Bad Data → Bad Report → Bad Decisions\n\n"
        "Your one typo becomes everyone's problem downstream."
    )

    # -- Certificate section (when all lessons completed) ----------------------
    all_complete = len(progress.completed_lesson_ids) >= len(lessons)
    if all_complete:
        st.success("You've completed all lessons! Download your certificate below.")
        cert_name = st.text_input(
            "Your name (for the certificate)",
            value=st.session_state.get("cert_name", ""),
            key="cert_name_input",
        )
        if cert_name:
            st.session_state["cert_name"] = cert_name
            cert_data = CertificateData(
                display_name=cert_name,
                course_title="How Data Flows",
                course_id="how_data_flows",
                lessons_completed=len(progress.completed_lesson_ids),
                total_lessons=len(lessons),
                total_xp=progress.total_xp,
                level_title=progress.level_title(),
                level_icon=progress.level_icon(),
                body_text=(
                    f"has successfully completed all {len(lessons)} lessons in "
                    f"How Data Flows, demonstrating an understanding of how data "
                    f"moves through organizational systems and why accuracy at "
                    f"the source matters."
                ),
            )
            pdf_bytes = generate_certificate_pdf(cert_data)
            st.download_button(
                label="Download Certificate (PDF)",
                data=pdf_bytes,
                file_name="how_data_flows_certificate.pdf",
                mime="application/pdf",
            )

    # -- KPI progress metrics --------------------------------------------------
    completed_count = len(progress.completed_lesson_ids)
    total_count = len(lessons)
    badge_count = len(progress.earned_badge_ids)
    st.markdown(
        f"""
        <div style="display: flex; gap: 1rem; margin: 1.5rem 0;">
            <div style="flex: 1; background: #fff; border: 1px solid #DEE2E6;
                        border-left: 4px solid #2980B9; border-radius: 4px;
                        padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
                <div style="font-size: 0.7rem; text-transform: uppercase;
                            color: #5D6D7E; margin-bottom: 0.3rem;">
                    Lessons Completed</div>
                <div style="font-size: 1.5rem; font-weight: 700;
                            color: #1B4F72;">{completed_count}/{total_count}</div>
            </div>
            <div style="flex: 1; background: #fff; border: 1px solid #DEE2E6;
                        border-left: 4px solid #27AE60; border-radius: 4px;
                        padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
                <div style="font-size: 0.7rem; text-transform: uppercase;
                            color: #5D6D7E; margin-bottom: 0.3rem;">
                    Total XP</div>
                <div style="font-size: 1.5rem; font-weight: 700;
                            color: #1B4F72;">{progress.total_xp}</div>
            </div>
            <div style="flex: 1; background: #fff; border: 1px solid #DEE2E6;
                        border-left: 4px solid #8E44AD; border-radius: 4px;
                        padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
                <div style="font-size: 0.7rem; text-transform: uppercase;
                            color: #5D6D7E; margin-bottom: 0.3rem;">
                    Badges Earned</div>
                <div style="font-size: 1.5rem; font-weight: 700;
                            color: #1B4F72;">{badge_count}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -- Lesson cards ----------------------------------------------------------
    st.markdown(
        """<h3 style="color: #1B4F72; margin-bottom: 0.5rem;">Lessons</h3>""",
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for i, lesson in enumerate(lessons):
        completed = lesson.id in progress.completed_lesson_ids
        chip_bg = "#27AE60" if completed else "#95A5A6"
        chip_text = "Complete" if completed else "Not Started"
        preview = (
            lesson.concept[:120] + "..." if len(lesson.concept) > 120 else lesson.concept
        )
        with cols[i % 2]:
            st.markdown(
                f"""
                <div style="border: 1px solid #DEE2E6; border-left: 4px solid #2980B9;
                            border-radius: 4px; padding: 1rem; margin-bottom: 0.75rem;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
                    <div style="display: flex; justify-content: space-between;
                                align-items: center; margin-bottom: 0.5rem;">
                        <strong style="color: #1B4F72;">
                            {lesson.icon} {lesson.title}</strong>
                        <span style="background: {chip_bg}; color: #fff;
                                     font-size: 0.7rem; padding: 2px 8px;
                                     border-radius: 12px;">{chip_text}</span>
                    </div>
                    <p style="color: #5D6D7E; font-size: 0.85rem; margin: 0;">
                        {preview}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Start", key=f"home_{lesson.id}"):
                st.session_state["selected_lesson"] = lesson.id
                st.rerun()


if __name__ == "__main__":
    main()
