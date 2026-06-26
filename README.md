# How Data Flows Through Your Organization

**Part of the [HR Analytics Academy](https://github.com/chrisselig/hr_analytics_academy)**

*Where does your data go after you hit Save?*

An interactive Streamlit course that teaches non-technical HR users how employee data flows from source systems to downstream reports, dashboards, and board decks — and why accuracy at the source matters.

## Lessons

| # | Lesson | Description |
|---|--------|-------------|
| 1 | 🚀 Your Data Has a Life After You | A new hire record flows from HRIS to payroll, benefits, finance, and the board deck |
| 2 | 🏭 Source Systems vs Reporting Systems | Why the HRIS and your dashboard show different numbers |
| 3 | 🤔 Why Finance and HR Never Agree on Headcount | Different definitions produce different numbers — both are "right" |
| 4 | 📞 The Telephone Game | How one wrong start date cascades to payroll, benefits, tenure, and the board deck |
| 5 | 📌 Single Source of Truth | What happens when three teams maintain their own employee spreadsheets |
| 6 | ⏰ Batch vs Real-Time | Why a termination at 2 PM won't show in tomorrow's report until tomorrow |
| 7 | 👤 The People Between the Systems | How manual Excel handoffs corrupt data silently |
| 8 | 🔍 Trace a Data Problem | Follow a wrong number backward through the data chain to find the root cause |

## Features

- **Gamified learning** — XP, levels (Newcomer to Data Navigator), and 6 achievement badges
- **Interactive lessons** — Spot the problem in real HR data, then reveal what breaks downstream
- **Before & After** — See bad data vs fixed data side by side
- **Quizzes** — 2 questions per lesson with detailed explanations
- **Progress tracking** — Session-based progress with visual indicators

## Quick Start

```bash
# Clone and enter
git clone https://github.com/chrisselig/how_data_flows.git
cd how_data_flows

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install
pip install -e ".[dev]"

# Run the app
streamlit run app/main.py

# Run tests
pytest -v

# Lint
ruff check .
```

## Project Structure

```
how_data_flows/
├── app/                    # Streamlit UI
│   ├── main.py             # Entry point
│   ├── components/         # Reusable UI components
│   │   ├── lesson.py       # Lesson renderer
│   │   └── sidebar.py      # Navigation + progress + badges
│   └── pages/              # One file per lesson
│       ├── registry.py     # Lesson page registry
│       └── lesson_*.py     # Thin wrappers calling render_lesson()
├── src/                    # Business logic
│   ├── data/
│   │   └── examples.py     # All lesson content (DataFrames, quizzes, text)
│   ├── models/
│   │   └── lesson_model.py # Lesson and QuizQuestion dataclasses
│   └── gamification/
│       ├── progress.py     # XP, levels, session state
│       └── badges.py       # Badge definitions + triggers
├── tests/                  # pytest tests
├── pyproject.toml          # Project config
└── README.md
```

## Teaching Pattern

Every lesson follows:

1. **Concept** — Plain-language principle
2. **Body tabs** — Why This Matters, Key Vocabulary, How to Spot It, Common Mistakes, How to Fix It
3. **Spot the Problem** — Bad data table with realistic HR data
4. **Reveal** — What breaks downstream
5. **Before & After** — Bad vs fixed data comparison
6. **Quiz** — 2 multiple choice questions with explanations

Core principle: **Bad Data → Bad Report → Bad Decisions**
