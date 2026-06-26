---
applyTo: src/data/examples.py
---

# Lesson Content Instructions

## File Purpose
All lesson content for the How Data Flows course lives in this single file. Each lesson is built by a builder function that returns a `Lesson` dataclass.

## Builder Function Pattern
- Name: `lesson_<id>()` matching the lesson ID
- Returns: `Lesson` instance with all fields populated
- Added to `get_all_lessons()` builder list

## Required Fields
Every lesson MUST have:
- `id`: unique snake_case identifier
- `title`: display title
- `icon`: single emoji
- `order`: integer for sort position
- `concept`: 1-2 sentence plain-language explanation
- `bad_data`: pandas DataFrame with 4-5 rows of realistic HR data showing the problem
- `downstream_impact`: starts with `"**What breaks:**\n\n"` followed by bullet points, then `"**Real-world example:**"`
- `good_data`: pandas DataFrame showing the corrected version
- `body`: markdown with exactly these ### headers: Why This Matters, Key Vocabulary, How to Spot It, Common Mistakes, How to Fix It
- `quiz`: list of exactly 2 `QuizQuestion` objects
- `tip`: practical advice string

## Data Quality
- Use realistic HR employee names (diverse)
- DataFrames should have 4-5 rows
- Bad data should contain a specific, identifiable problem
- Good data should show the same scenario corrected
- Quiz questions should be non-obvious with plausible distractors

## Language
- Simple, non-technical language
- Audience is HR professionals, not engineers
- Avoid jargon unless defining it in Key Vocabulary
