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


def _load_theme() -> None:
    """Load corporate CSS and render the logo bar."""
    import base64

    css = (Path(__file__).parent / "static" / "theme.css").read_text()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    logo_path = Path(__file__).parent / "static" / "logo.png"
    if logo_path.exists():
        b64 = base64.b64encode(logo_path.read_bytes()).decode()
        st.markdown(
            f'<div class="corp-topbar">'
            f'<img src="data:image/png;base64,{b64}" alt="Logo" /></div>',
            unsafe_allow_html=True,
        )
    st.markdown('<div class="corp-divider"></div>', unsafe_allow_html=True)


def main() -> None:
    """Application entry point."""
    st.set_page_config(
        page_title="How Data Flows",
        page_icon="🔄",
        layout="wide",
    )

    _load_theme()
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
    st.markdown(
        """
        <div class="corp-header">
            <h1>How Data Flows Through Your Organization</h1>
            <p>Every time you save an employee record, it starts a journey
            through multiple systems. Payroll reads it. Benefits reads it.
            Finance counts heads from it. This course shows you where your
            data goes — and why accuracy at the source matters.</p>
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
        <div class="kpi-row">
            <div class="kpi-card kpi-card--blue">
                <div class="kpi-label">Lessons Completed</div>
                <div class="kpi-value">{completed_count}/{total_count}</div>
            </div>
            <div class="kpi-card kpi-card--green">
                <div class="kpi-label">Total XP</div>
                <div class="kpi-value">{progress.total_xp}</div>
            </div>
            <div class="kpi-card kpi-card--purple">
                <div class="kpi-label">Badges Earned</div>
                <div class="kpi-value">{badge_count}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -- Lesson cards ----------------------------------------------------------
    st.markdown(
        '<h3 class="section-heading">Lessons</h3>',
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for i, lesson in enumerate(lessons):
        completed = lesson.id in progress.completed_lesson_ids
        chip_cls = "chip--complete" if completed else "chip--not-started"
        chip_text = "Complete" if completed else "Not Started"
        preview = (
            lesson.concept[:120] + "..." if len(lesson.concept) > 120 else lesson.concept
        )
        with cols[i % 2]:
            st.markdown(
                f"""
                <div class="lesson-card">
                    <div class="lesson-card__header">
                        <span class="lesson-card__title">
                            {lesson.icon} {lesson.title}</span>
                        <span class="chip {chip_cls}">{chip_text}</span>
                    </div>
                    <p class="lesson-card__preview">{preview}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Start", key=f"home_{lesson.id}"):
                st.session_state["selected_lesson"] = lesson.id
                st.rerun()


if __name__ == "__main__":
    main()
