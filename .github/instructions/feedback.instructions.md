---
applyTo: app/components/feedback.py
---

# Feedback Component Instructions

## Purpose
Collects per-lesson star rating and optional comment from users.
Currently stores in `st.session_state` only. When Databricks is available,
wire up persistence to the table below.

## Databricks Table Schema

```sql
bu_hr.hr_academy.feedback (
    email           STRING NOT NULL,     -- SSO user (from Azure AD)
    course_id       STRING NOT NULL,     -- 'how_data_flows', 'data_governance', etc.
    lesson_id       STRING NOT NULL,     -- 'data_life', 'single_source', etc.
    rating          INT NOT NULL,        -- 1-5 star rating
    comment         STRING DEFAULT '',   -- free-text (optional)
    submitted_at    TIMESTAMP NOT NULL   -- UTC timestamp
)
```

## Wiring Up Databricks

When persistence is ready, replace the `# TODO` block in `render_feedback()` with
a call to a `save_to_databricks()` function that:

1. Gets the user email from the SSO session
2. Builds a row dict matching the schema above
3. Writes to `bu_hr.hr_academy.feedback` via the Databricks SQL connector
4. Handles errors gracefully (show `st.error`, don't crash the page)

## Rules
- `FEEDBACK_ENABLED` flag at top of file controls visibility
- One submission per lesson per session (tracked via session state)
- `st.feedback` returns 0-4; store as 1-5 in the database
