"""Lesson feedback component.

Collects star rating and optional comment per lesson.
Currently stores in session state only — Databricks persistence TBD.
"""

from __future__ import annotations

import streamlit as st

FEEDBACK_ENABLED = True


def render_feedback(course_id: str, lesson_id: str) -> None:
    """Render the feedback form inside a collapsible expander.

    Args:
        course_id: Course identifier (e.g. 'how_data_flows').
        lesson_id: Lesson identifier (e.g. 'data_life').
    """
    if not FEEDBACK_ENABLED:
        return

    feedback_key = f"feedback_{course_id}_{lesson_id}"
    already_submitted = st.session_state.get(f"{feedback_key}_submitted", False)

    with st.expander("Share your feedback"):
        if already_submitted:
            st.success("Thanks! Your feedback was submitted.")
            return

        rating = st.feedback(options="stars", key=f"{feedback_key}_rating")

        comment = st.text_area(
            "Anything else you'd like to share? (optional)",
            key=f"{feedback_key}_comment",
            max_chars=500,
        )

        if st.button("Submit Feedback", key=f"{feedback_key}_btn"):
            if rating is None:
                st.warning("Please select a star rating before submitting.")
                return

            # Store in session state for now
            st.session_state[f"{feedback_key}_submitted"] = True
            st.session_state[f"{feedback_key}_data"] = {
                "course_id": course_id,
                "lesson_id": lesson_id,
                "rating": rating + 1,  # st.feedback returns 0-4, store as 1-5
                "comment": comment,
            }

            # TODO: Replace with save_to_databricks() when persistence is ready.
            # Target table: bu_hr.hr_academy.feedback
            # See .github/instructions/feedback.instructions.md for schema.

            st.success("Feedback submitted!")
            st.rerun()
