"""All lesson data for How Data Flows Through Your Organization.

Each builder function returns a Lesson with:
  - concept: plain-language principle
  - bad_data / good_data: DataFrames with realistic HR data
  - downstream_impact: what breaks when data is wrong
  - body: rich markdown with ### headers (auto-split into tabs)
  - quiz: 2 quiz questions per lesson
  - tip: practical advice
"""

from __future__ import annotations

import pandas as pd

from src.models.lesson_model import Lesson, QuizQuestion


def get_all_lessons() -> list[Lesson]:
    """Return all lessons sorted by order."""
    builders = [
        lesson_data_life,
        lesson_source_vs_reporting,
        lesson_headcount_disagreement,
        lesson_error_multiplication,
        lesson_single_source,
        lesson_batch_vs_realtime,
        lesson_human_handoffs,
        lesson_trace_problem,
    ]
    lessons = [b() for b in builders]
    return sorted(lessons, key=lambda lesson: lesson.order)


# ---------------------------------------------------------------------------
# Lesson 1: Your Data Has a Life After You
# ---------------------------------------------------------------------------


def lesson_data_life() -> Lesson:
    """Build the 'Your Data Has a Life After You' lesson."""
    bad_data = pd.DataFrame({
        "System": ["HRIS (Source)", "Payroll", "Benefits Portal", "Finance Headcount", "Board Deck"],
        "Employee": ["Maria Santos", "Maria Santos", "Maria Santos", "Maria Santos", "Maria Santos"],
        "Department": ["Marketing", "Marketing", "Marketing", "Marketing", "Marketing"],
        "Start Date": ["2024-01-15", "2024-01-15", "2024-01-15", "2024-01-15", "2024-01-15"],
        "Status": ["Active", "Active", "Active", "Active", "Active"],
        "Notes": ["Dept should be Sales", "Copied from HRIS", "Copied from HRIS", "Used for headcount", "Rolled up from Finance"],
    })

    good_data = pd.DataFrame({
        "System": ["HRIS (Source)", "Payroll", "Benefits Portal", "Finance Headcount", "Board Deck"],
        "Employee": ["Maria Santos", "Maria Santos", "Maria Santos", "Maria Santos", "Maria Santos"],
        "Department": ["Sales", "Sales", "Sales", "Sales", "Sales"],
        "Start Date": ["2024-01-15", "2024-01-15", "2024-01-15", "2024-01-15", "2024-01-15"],
        "Status": ["Active", "Active", "Active", "Active", "Active"],
        "Notes": ["Corrected at source", "Auto-synced", "Auto-synced", "Auto-synced", "Rolled up correctly"],
    })

    return Lesson(
        id="data_life",
        title="Your Data Has a Life After You",
        icon="🚀",
        order=1,
        concept="Every time you save an employee record, that data flows to payroll, benefits, finance, and even the board deck. One wrong entry at the source becomes everyone's wrong number downstream.",
        bad_data=bad_data,
        downstream_impact=(
            "**What breaks:**\n\n"
            "- Maria shows up in Marketing's headcount instead of Sales\n"
            "- Sales appears understaffed in the board deck\n"
            "- Marketing's budget includes someone who doesn't work there\n"
            "- Finance reports the wrong departmental cost allocation\n\n"
            "**Real-world example:** A VP of Sales sees a board deck showing they have 12 people when they actually have 13. They escalate. Three teams spend two days tracing the discrepancy to a single HRIS entry made on Day 1."
        ),
        good_data=good_data,
        body=(
            "### Why This Matters\n"
            "You might think you're just updating one field in one system. But your HRIS is the starting point for a chain of data that touches every corner of the organization. Payroll uses it to calculate pay. Benefits uses it to determine eligibility. Finance uses it to report headcount. The board uses those numbers to make strategic decisions.\n\n"
            "### Key Vocabulary\n"
            "- **Source system**: The system where data is first entered (e.g., your HRIS)\n"
            "- **Downstream system**: Any system that receives data from the source\n"
            "- **Data propagation**: How data copies itself from one system to another\n"
            "- **Cascade effect**: When one error spreads to many places\n\n"
            "### How to Spot It\n"
            "- A manager says \"the numbers in my report don't match what I see in the HRIS\"\n"
            "- Two departments report different headcounts for the same team\n"
            "- Someone asks \"where did this number come from?\" and nobody can answer quickly\n\n"
            "### Common Mistakes\n"
            "- Thinking \"it's just one field, I'll fix it later\"\n"
            "- Not realizing how many systems read from the HRIS\n"
            "- Assuming downstream systems will catch the error\n"
            "- Entering placeholder data and forgetting to update it\n\n"
            "### How to Fix It\n"
            "- Always double-check department, cost center, and manager fields before saving\n"
            "- If you spot an error, fix it at the source (the HRIS) — not in the downstream report\n"
            "- Ask your HRIS admin: \"what systems does this field feed into?\"\n"
            "- When onboarding a new hire, verify all fields with the hiring manager before saving"
        ),
        quiz=[
            QuizQuestion(
                question="Maria was entered into the HRIS with 'Marketing' instead of 'Sales'. Who is most likely to notice the error first?",
                options=[
                    "The payroll team",
                    "Maria's manager in Sales",
                    "The benefits administrator",
                    "The CEO reading the board deck",
                ],
                correct_index=1,
                explanation="Maria's direct manager in Sales would notice when reviewing their team roster or headcount reports. Payroll and benefits process the data but may not validate department assignments.",
            ),
            QuizQuestion(
                question="If you discover a department error in a finance report, where should you fix it?",
                options=[
                    "In the finance report directly",
                    "In the payroll system",
                    "In the HRIS (the source system)",
                    "Ask IT to update all systems at once",
                ],
                correct_index=2,
                explanation="Always fix errors at the source system (the HRIS). Fixing it in a downstream report only patches one copy — the error remains everywhere else and will reappear next time data syncs.",
            ),
        ],
        tip="Before you hit Save on any new hire or change, ask yourself: 'Would I be comfortable if this exact data appeared on the CEO's board deck?' Because eventually, it will.",
    )


# ---------------------------------------------------------------------------
# Lesson 2: Source Systems vs Reporting Systems
# ---------------------------------------------------------------------------


def lesson_source_vs_reporting() -> Lesson:
    """Build the 'Source Systems vs Reporting Systems' lesson."""
    bad_data = pd.DataFrame({
        "Employee": ["James Okafor", "Priya Patel", "Carlos Rivera", "Lisa Chen", "Tom Wilson"],
        "HRIS Status": ["Active", "Active", "Active", "Terminated", "Active"],
        "Report Status": ["Active", "Active", "Active", "Active", "Active"],
        "HRIS Dept": ["Engineering", "Engineering", "Sales", "Marketing", "Sales"],
        "Report Dept": ["Engineering", "IT", "Sales", "Marketing", "Sales"],
    })

    good_data = pd.DataFrame({
        "Employee": ["James Okafor", "Priya Patel", "Carlos Rivera", "Lisa Chen", "Tom Wilson"],
        "HRIS Status": ["Active", "Active", "Active", "Terminated", "Active"],
        "Report Status": ["Active", "Active", "Active", "Terminated", "Active"],
        "HRIS Dept": ["Engineering", "Engineering", "Sales", "Marketing", "Sales"],
        "Report Dept": ["Engineering", "Engineering", "Sales", "Marketing", "Sales"],
    })

    return Lesson(
        id="source_vs_reporting",
        title="Source Systems vs Reporting Systems",
        icon="🏭",
        order=2,
        concept="Source systems are where data is entered and maintained. Reporting systems are where data is read and analyzed. They can show different numbers — and understanding why is critical.",
        bad_data=bad_data,
        downstream_impact=(
            "**What breaks:**\n\n"
            "- Lisa Chen shows as Active in the report but Terminated in the HRIS — headcount is inflated by 1\n"
            "- Priya appears in IT on the report but Engineering in the HRIS — department totals are wrong\n"
            "- HR says 4 active employees, the report says 5\n"
            "- Leadership loses trust in all HR data because the numbers don't match\n\n"
            "**Real-world example:** An HR director presents headcount data at a leadership meeting. The CFO pulls up their own report showing a different number. The rest of the meeting is spent debating whose data is right instead of making decisions."
        ),
        good_data=good_data,
        body=(
            "### Why This Matters\n"
            "Your HRIS is a source system — it's where you type in data. But most leaders never look at the HRIS directly. They see dashboards, reports, and data warehouses. If the reporting system is out of sync with the source, people make decisions based on stale or wrong numbers.\n\n"
            "### Key Vocabulary\n"
            "- **Source system**: Where data is created and edited (HRIS, ATS, payroll)\n"
            "- **Reporting system**: Where data is read and analyzed (dashboards, data warehouse, Excel exports)\n"
            "- **ETL (Extract, Transform, Load)**: The process that moves data from source to reporting\n"
            "- **Data lag**: The delay between a change in the source and its appearance in a report\n\n"
            "### How to Spot It\n"
            "- Someone says \"my report shows X but the HRIS shows Y\"\n"
            "- A terminated employee still appears in active headcount reports\n"
            "- Department names in reports don't match what's in the HRIS\n\n"
            "### Common Mistakes\n"
            "- Assuming the report is always right (it might be stale)\n"
            "- Assuming the HRIS is always right (it might have a pending change not yet saved)\n"
            "- Not knowing when the report was last refreshed\n"
            "- Editing data in a report instead of the source system\n\n"
            "### How to Fix It\n"
            "- Always ask: \"When was this report last refreshed?\"\n"
            "- Know which system is the source for each data field\n"
            "- If numbers don't match, start by checking the source system\n"
            "- Never edit data in a reporting system — it will be overwritten on the next refresh"
        ),
        quiz=[
            QuizQuestion(
                question="A terminated employee still appears as 'Active' in a headcount dashboard. What is the most likely cause?",
                options=[
                    "The HRIS has a bug",
                    "The dashboard hasn't refreshed since the termination was processed",
                    "Someone hacked the dashboard",
                    "The employee was rehired",
                ],
                correct_index=1,
                explanation="Reporting systems often refresh on a schedule (daily, weekly). If a termination was processed after the last refresh, the dashboard will show stale data until the next sync.",
            ),
            QuizQuestion(
                question="Priya's department shows as 'Engineering' in the HRIS but 'IT' in the report. What should you do first?",
                options=[
                    "Change it to IT in the HRIS to match the report",
                    "Change it to Engineering in the report",
                    "Check which system is the source of truth for department data",
                    "Ignore it — small differences don't matter",
                ],
                correct_index=2,
                explanation="Before making any changes, you need to know which system is authoritative. The HRIS is usually the source for department data, but you should confirm before changing anything.",
            ),
        ],
        tip="Whenever someone shows you a number from a report, your first question should be: 'When was this data last refreshed?' The answer tells you how stale it might be.",
    )


# ---------------------------------------------------------------------------
# Lesson 3: Why Finance and HR Never Agree on Headcount
# ---------------------------------------------------------------------------


def lesson_headcount_disagreement() -> Lesson:
    """Build the 'Why Finance and HR Never Agree on Headcount' lesson."""
    bad_data = pd.DataFrame({
        "Employee": ["Ana Lopez", "David Kim", "Sarah Brown", "Raj Mehta", "Jenny Nguyen"],
        "HR Status": ["Full-Time", "Part-Time (0.5 FTE)", "Contractor", "On Leave", "Full-Time"],
        "HR Headcount": [1, 1, 1, 1, 1],
        "Finance Headcount": [1.0, 0.5, 0.0, 0.0, 1.0],
        "Cutoff Date HR": ["Jun 30", "Jun 30", "Jun 30", "Jun 30", "Jun 30"],
        "Cutoff Date Finance": ["Jun 28", "Jun 28", "Jun 28", "Jun 28", "Jun 28"],
    })

    good_data = pd.DataFrame({
        "Employee": ["Ana Lopez", "David Kim", "Sarah Brown", "Raj Mehta", "Jenny Nguyen"],
        "Status": ["Full-Time", "Part-Time (0.5 FTE)", "Contractor", "On Leave", "Full-Time"],
        "Bodies (HR def.)": [1, 1, 1, 1, 1],
        "FTE (Finance def.)": [1.0, 0.5, 0.0, 0.0, 1.0],
        "Shared Cutoff": ["Jun 30", "Jun 30", "Jun 30", "Jun 30", "Jun 30"],
    })

    return Lesson(
        id="headcount_disagreement",
        title="Why Finance and HR Never Agree on Headcount",
        icon="🤔",
        order=3,
        concept="HR and Finance often report different headcount numbers — not because someone is wrong, but because they define 'headcount' differently. HR counts bodies. Finance counts FTEs. Both exclude different groups.",
        bad_data=bad_data,
        downstream_impact=(
            "**What breaks:**\n\n"
            "- HR reports 5 employees. Finance reports 2.5 FTE. Leadership is confused.\n"
            "- A contractor is counted by HR but excluded by Finance — or vice versa.\n"
            "- An employee on leave is counted by HR but not by Finance — the gap looks like attrition.\n"
            "- Different cutoff dates mean the numbers can never match even with the same definitions.\n\n"
            "**Real-world example:** The CHRO tells the board 'We have 2,400 employees.' The CFO's slide says 2,150 FTE. A board member asks if 250 people quit. Nobody is wrong — they're just counting differently."
        ),
        good_data=good_data,
        body=(
            "### Why This Matters\n"
            "Headcount sounds simple, but it's one of the most argued-about numbers in any organization. HR typically counts every person who has an active employment record. Finance counts in FTEs (full-time equivalents) and may exclude contractors, interns, or people on long-term leave. When these two teams present different numbers, leadership loses confidence in both.\n\n"
            "### Key Vocabulary\n"
            "- **Headcount (bodies)**: Number of individual people with active records\n"
            "- **FTE (Full-Time Equivalent)**: Hours worked relative to a full-time schedule (a half-time employee = 0.5 FTE)\n"
            "- **Cutoff date**: The point-in-time snapshot used for the count\n"
            "- **Inclusion/exclusion rules**: Which worker types are counted (contractors, interns, leaves)\n\n"
            "### How to Spot It\n"
            "- HR and Finance present different headcount numbers at the same meeting\n"
            "- A leader asks \"did we hire or lose people?\" but the change is just definitional\n"
            "- Reports from different teams show different totals for the same period\n\n"
            "### Common Mistakes\n"
            "- Assuming \"headcount\" means the same thing to everyone\n"
            "- Not documenting inclusion/exclusion rules on reports\n"
            "- Using different cutoff dates for HR and Finance snapshots\n"
            "- Arguing about who is \"right\" instead of aligning on definitions\n\n"
            "### How to Fix It\n"
            "- Agree on shared definitions: publish a data dictionary that says exactly what \"headcount\" means\n"
            "- Always label reports: \"Headcount (bodies, incl. contractors)\" or \"Headcount (FTE, excl. leaves)\"\n"
            "- Use the same cutoff date across teams\n"
            "- When numbers differ, explain the definitional gap instead of debating accuracy"
        ),
        quiz=[
            QuizQuestion(
                question="HR reports 500 employees. Finance reports 420 FTE. What is the most likely explanation?",
                options=[
                    "Finance made a counting error",
                    "80 people were terminated between the two reports",
                    "The two teams use different definitions — FTE vs bodies, and likely different inclusion rules",
                    "HR's system has duplicate records",
                ],
                correct_index=2,
                explanation="The most common reason HR and Finance headcounts differ is definitional. Part-time employees count as less than 1 FTE, and Finance may exclude contractors, interns, or employees on leave.",
            ),
            QuizQuestion(
                question="What is the best way to prevent headcount disagreements between HR and Finance?",
                options=[
                    "Only let one team report headcount",
                    "Agree on shared definitions and cutoff dates, and label every report clearly",
                    "Always use HR's number since they own employee data",
                    "Round all numbers to avoid small differences",
                ],
                correct_index=1,
                explanation="The fix is alignment, not control. Both teams have legitimate reasons to count differently. The key is to agree on definitions, use the same cutoff dates, and clearly label what each number includes.",
            ),
        ],
        tip="Every headcount report you create should answer three questions in a footnote: (1) Who is included? (2) Who is excluded? (3) What date is this as-of? If you can't answer those, neither can your audience.",
    )


# ---------------------------------------------------------------------------
# Lesson 4: The Telephone Game: How Small Errors Multiply
# ---------------------------------------------------------------------------


def lesson_error_multiplication() -> Lesson:
    """Build the 'The Telephone Game: How Small Errors Multiply' lesson."""
    bad_data = pd.DataFrame({
        "System": ["HRIS (Source)", "Payroll", "Benefits", "Tenure Report", "Board Deck"],
        "Employee": ["Kevin Park", "Kevin Park", "Kevin Park", "Kevin Park", "Kevin Park"],
        "Start Date": ["2024-03-01", "2024-03-01", "2024-03-01", "2024-03-01", "—"],
        "What Went Wrong": ["Entered as Mar 1 (should be Jan 3)", "Paid from Mar 1 — missed 2 months pay", "Benefits eligibility delayed by 2 months", "Tenure shows 10 months instead of 12", "Avg tenure metric is off by 0.4 months"],
    })

    good_data = pd.DataFrame({
        "System": ["HRIS (Source)", "Payroll", "Benefits", "Tenure Report", "Board Deck"],
        "Employee": ["Kevin Park", "Kevin Park", "Kevin Park", "Kevin Park", "Kevin Park"],
        "Start Date": ["2024-01-03", "2024-01-03", "2024-01-03", "2024-01-03", "—"],
        "Result": ["Correct start date", "Paid correctly from Day 1", "Benefits eligible on time", "Tenure accurately reported", "Avg tenure metric is accurate"],
    })

    return Lesson(
        id="error_multiplication",
        title="The Telephone Game: How Small Errors Multiply",
        icon="📞",
        order=4,
        concept="A single wrong date in the HRIS doesn't stay in the HRIS. It cascades to payroll (wrong pay), benefits (wrong eligibility), tenure reports (wrong averages), and the board deck (wrong retention story).",
        bad_data=bad_data,
        downstream_impact=(
            "**What breaks:**\n\n"
            "- Kevin was underpaid for 2 months because payroll used the wrong start date\n"
            "- His benefits enrollment was delayed — he had no health coverage for 2 months\n"
            "- The tenure report shows him at 10 months instead of 12, pulling the team average down\n"
            "- The board deck shows lower average tenure, suggesting a retention problem that doesn't exist\n\n"
            "**Real-world example:** A VP sees declining average tenure on the board deck and proposes a $500K retention bonus program. The actual cause? Three start dates were entered in MM/DD format instead of DD/MM by a new HR coordinator. Total cost of investigating and correcting: 40+ hours across 5 teams."
        ),
        good_data=good_data,
        body=(
            "### Why This Matters\n"
            "Think of the children's game of Telephone — one person whispers a message, and by the time it reaches the last person, it's completely different. Data works the same way. A small error at the source gets used by system after system, and each system makes decisions based on that wrong data. The error doesn't just persist — it multiplies.\n\n"
            "### Key Vocabulary\n"
            "- **Error cascade**: When one mistake causes a chain of downstream errors\n"
            "- **Data lineage**: The path data takes from source to final report\n"
            "- **Root cause**: The original error that started the cascade\n"
            "- **Blast radius**: How many systems and reports are affected by a single error\n\n"
            "### How to Spot It\n"
            "- An employee reports a payroll discrepancy and the investigation reveals a wrong date in the HRIS\n"
            "- A metric on a dashboard shifts unexpectedly and nobody made a policy change\n"
            "- Multiple systems show slightly different but consistently wrong data for the same person\n\n"
            "### Common Mistakes\n"
            "- Entering dates in the wrong format (MM/DD vs DD/MM)\n"
            "- Copy-pasting from one record to another and forgetting to update a field\n"
            "- Assuming a small error is harmless because \"it's just one person\"\n"
            "- Fixing the error in a downstream system instead of at the source\n\n"
            "### How to Fix It\n"
            "- Double-check dates, especially start dates and termination dates — they feed everything\n"
            "- Use date pickers instead of free-text date fields when possible\n"
            "- When you find an error, trace it backward to the source and fix it there\n"
            "- Ask your HRIS team: \"If I get this field wrong, what else breaks?\""
        ),
        quiz=[
            QuizQuestion(
                question="Kevin's start date was entered as March 1 instead of January 3. Which downstream impact is LEAST likely?",
                options=[
                    "Payroll calculates the wrong pay amount",
                    "Benefits eligibility is delayed",
                    "Kevin's emergency contact information is wrong",
                    "The board deck shows inaccurate average tenure",
                ],
                correct_index=2,
                explanation="Emergency contact information is not derived from start date. Payroll, benefits eligibility, and tenure calculations all depend on start date, so they would all be affected.",
            ),
            QuizQuestion(
                question="You discover a wrong start date in the HRIS that has already propagated to payroll and benefits. What should you fix first?",
                options=[
                    "The payroll record, since that affects the employee's pay",
                    "The benefits record, since that affects coverage",
                    "The HRIS record (the source), then notify payroll and benefits to re-sync",
                    "The board deck, since that's what leadership sees",
                ],
                correct_index=2,
                explanation="Always fix at the source first. If you fix payroll but not the HRIS, the error will re-propagate on the next sync. Fix the root cause, then ensure downstream systems pick up the correction.",
            ),
        ],
        tip="Start dates and termination dates are the two most dangerous fields in HR data. They feed payroll calculations, benefits eligibility, tenure metrics, and turnover rates. Triple-check them.",
    )


# ---------------------------------------------------------------------------
# Lesson 5: What "Single Source of Truth" Actually Means
# ---------------------------------------------------------------------------


def lesson_single_source() -> Lesson:
    """Build the 'What Single Source of Truth Actually Means' lesson."""
    bad_data = pd.DataFrame({
        "Employee": ["Nina Williams", "Nina Williams", "Nina Williams", "Marco Rossi", "Marco Rossi"],
        "Maintained By": ["HR Team", "Compensation Team", "Recruiting Team", "HR Team", "Compensation Team"],
        "Department": ["Product", "Product", "Engineering", "Sales", "Sales"],
        "Title": ["Sr. Designer", "Sr. Designer", "Product Designer", "Account Exec", "Sales Rep"],
        "Salary": ["$95,000", "$98,000", "$95,000", "$72,000", "$72,000"],
        "Last Updated": ["Jun 15", "Jun 20", "May 1", "Jun 15", "Jun 10"],
    })

    good_data = pd.DataFrame({
        "Employee": ["Nina Williams", "Nina Williams", "Nina Williams", "Marco Rossi", "Marco Rossi"],
        "Source": ["HRIS (Source of Truth)", "Comp system (reads from HRIS)", "ATS (reads from HRIS)", "HRIS (Source of Truth)", "Comp system (reads from HRIS)"],
        "Department": ["Product", "Product", "Product", "Sales", "Sales"],
        "Title": ["Sr. Designer", "Sr. Designer", "Sr. Designer", "Account Exec", "Account Exec"],
        "Salary": ["$98,000", "$98,000", "$98,000", "$72,000", "$72,000"],
    })

    return Lesson(
        id="single_source",
        title="What 'Single Source of Truth' Actually Means",
        icon="📌",
        order=5,
        concept="When multiple teams maintain their own copies of employee data, those copies drift apart over time. A 'single source of truth' means one system is authoritative, and all others read from it.",
        bad_data=bad_data,
        downstream_impact=(
            "**What breaks:**\n\n"
            "- Nina's department is 'Engineering' in recruiting's spreadsheet but 'Product' in the HRIS — which is right?\n"
            "- Her title differs across systems — compensation decisions may be based on the wrong level\n"
            "- Her salary is $95K in two systems and $98K in another — a recent raise was only updated in one place\n"
            "- Marco's title differs — 'Account Exec' vs 'Sales Rep' — comp benchmarking will be inaccurate\n\n"
            "**Real-world example:** During an audit, a company discovers 340 employees have different job titles in HR vs Compensation systems. The remediation project takes 3 months and requires manager-by-manager validation."
        ),
        good_data=good_data,
        body=(
            "### Why This Matters\n"
            "Imagine three people each writing down your phone number. Over time, you change your number. You tell one person, but not the other two. Now two out of three people have the wrong number. This is exactly what happens when multiple teams maintain their own employee spreadsheets instead of reading from one authoritative source.\n\n"
            "### Key Vocabulary\n"
            "- **Single source of truth (SSOT)**: One authoritative system for a given data element\n"
            "- **Data drift**: When copies of data diverge over time because they're maintained independently\n"
            "- **Master data**: Core reference data (employee name, department, title) that should be consistent everywhere\n"
            "- **Golden record**: The one version of a record that is considered correct\n\n"
            "### How to Spot It\n"
            "- Two teams present conflicting information about the same employee\n"
            "- Someone says \"let me check my spreadsheet\" instead of looking in the HRIS\n"
            "- An employee's title or department is different depending on which system you check\n\n"
            "### Common Mistakes\n"
            "- Maintaining a \"shadow\" spreadsheet because the HRIS is \"too slow\" to update\n"
            "- Assuming all systems are in sync because they were in sync last month\n"
            "- Updating data in a downstream system and expecting it to flow back to the source\n"
            "- Not having a clear answer to: \"Which system is the source of truth for job titles?\"\n\n"
            "### How to Fix It\n"
            "- Designate one system as the source for each data element (HRIS for titles, comp system for salary bands, etc.)\n"
            "- Set up automated syncs so downstream systems pull from the source instead of being manually updated\n"
            "- Eliminate shadow spreadsheets — if the HRIS process is too slow, fix the process, don't create a workaround\n"
            "- Publish a simple reference guide: \"For X data, the source is Y system\""
        ),
        quiz=[
            QuizQuestion(
                question="Nina's title is 'Sr. Designer' in the HRIS and 'Product Designer' in the recruiting system. What is the root cause?",
                options=[
                    "The recruiting team made a typo",
                    "Nina was promoted but the recruiting system wasn't updated",
                    "Multiple systems are independently maintained without a single source of truth",
                    "The HRIS has a syncing bug",
                ],
                correct_index=2,
                explanation="The root cause is structural: multiple teams maintain their own copies of employee data. Even if the recruiting team's data was correct at one point, it drifted because there's no automated sync from a single authoritative source.",
            ),
            QuizQuestion(
                question="What does 'single source of truth' mean in practice?",
                options=[
                    "Only one person is allowed to enter data",
                    "Only one system exists in the entire company",
                    "One system is designated as authoritative for each data element, and others read from it",
                    "All data is stored in a single spreadsheet",
                ],
                correct_index=2,
                explanation="SSOT doesn't mean one system for everything. It means for each type of data (titles, salaries, org structure), there is one designated authoritative source, and other systems pull from it rather than maintaining independent copies.",
            ),
        ],
        tip="Ask yourself: 'If I needed to know an employee's current job title right now, which ONE system would I trust?' If you can't answer that instantly, your organization doesn't have a clear source of truth for that data.",
    )


# ---------------------------------------------------------------------------
# Lesson 6: Batch vs Real-Time
# ---------------------------------------------------------------------------


def lesson_batch_vs_realtime() -> Lesson:
    """Build the 'Batch vs Real-Time' lesson."""
    bad_data = pd.DataFrame({
        "Event": ["Termination processed", "Payroll notified", "Badge access revoked", "Headcount report updated", "Benefits terminated"],
        "Employee": ["Derek Foster", "Derek Foster", "Derek Foster", "Derek Foster", "Derek Foster"],
        "Time of Action": ["2:00 PM Tuesday", "Next payroll run (Friday)", "Next morning batch (Wed 6 AM)", "Next day report refresh (Wed 7 AM)", "End of month"],
        "Gap": ["—", "3 days", "16 hours", "17 hours", "Up to 30 days"],
        "Risk": ["—", "Low (overpayment clawed back)", "HIGH — security risk", "Medium — stale headcount", "Low (coverage continues)"],
    })

    good_data = pd.DataFrame({
        "Event": ["Termination processed", "Badge access revoked", "Payroll notified", "Headcount report updated", "Benefits terminated"],
        "Employee": ["Derek Foster", "Derek Foster", "Derek Foster", "Derek Foster", "Derek Foster"],
        "Timing": ["2:00 PM Tuesday", "2:01 PM Tuesday (real-time)", "2:05 PM Tuesday (real-time)", "Wed 7 AM (daily batch — acceptable)", "End of month (monthly batch — acceptable)"],
        "Sync Type": ["—", "Real-time (security-critical)", "Real-time (pay-critical)", "Batch (reporting — OK)", "Batch (admin — OK)"],
    })

    return Lesson(
        id="batch_vs_realtime",
        title="Batch vs Real-Time: When Timing Matters",
        icon="⏰",
        order=6,
        concept="Not all data moves instantly. Some systems sync in real-time (seconds), while others sync in batches (daily, weekly). Knowing the difference tells you when a gap is dangerous and when it's fine.",
        bad_data=bad_data,
        downstream_impact=(
            "**What breaks:**\n\n"
            "- Derek is terminated at 2 PM but his badge still works until 6 AM the next day — a 16-hour security gap\n"
            "- The headcount report still shows Derek as active until the next morning refresh\n"
            "- If anyone checks headcount Tuesday afternoon, they get a wrong number\n"
            "- Benefits continue for up to a month after termination, potentially costing the company\n\n"
            "**Real-world example:** An employee is terminated for cause at 3 PM. Because badge access runs on a nightly batch, the employee returns that evening, accesses their office, and removes company property. The security gap existed because the system wasn't configured for real-time revocation."
        ),
        good_data=good_data,
        body=(
            "### Why This Matters\n"
            "Think of it like mail vs text messaging. A text arrives instantly — that's real-time. Mail arrives the next day — that's batch processing. Both work, but you wouldn't send a text message by mail if it was urgent. Data works the same way: some things need to sync instantly (security access), while others are fine updating overnight (monthly headcount reports).\n\n"
            "### Key Vocabulary\n"
            "- **Real-time sync**: Data moves between systems within seconds or minutes\n"
            "- **Batch sync**: Data moves on a schedule (nightly, weekly, monthly)\n"
            "- **Data lag**: The time between when something changes in the source and when it appears downstream\n"
            "- **Point-in-time snapshot**: A report that captures data as of a specific moment\n\n"
            "### How to Spot It\n"
            "- A change you made today doesn't appear in a report until tomorrow\n"
            "- Someone asks about a new hire and the system says \"employee not found\"\n"
            "- A termination is processed but the person still has system access hours later\n\n"
            "### Common Mistakes\n"
            "- Assuming all systems update instantly when you hit Save\n"
            "- Treating all data lag the same — a 24-hour lag for security is very different from a 24-hour lag for a report\n"
            "- Not asking IT: \"How often does this system sync?\"\n"
            "- Panicking when a report doesn't reflect a change made 5 minutes ago\n\n"
            "### How to Fix It\n"
            "- Know which of your systems are real-time vs batch — ask your HRIS admin or IT team\n"
            "- For security-critical changes (terminations, role changes), ensure real-time sync or manual immediate action\n"
            "- Label reports with their refresh time: \"Data as of: June 25, 7:00 AM\"\n"
            "- Don't assume a report is wrong just because it doesn't reflect today's changes"
        ),
        quiz=[
            QuizQuestion(
                question="Derek is terminated at 2 PM. Which downstream action is MOST critical to handle in real-time rather than in a nightly batch?",
                options=[
                    "Updating the headcount report",
                    "Revoking building badge access",
                    "Terminating benefits coverage",
                    "Removing from the org chart",
                ],
                correct_index=1,
                explanation="Badge access is a security concern. A terminated employee with active badge access is a physical security risk. Headcount reports and benefits can safely wait for the next batch cycle.",
            ),
            QuizQuestion(
                question="You process a new hire at 3 PM and your manager asks why they don't appear in the headcount dashboard yet. What's the best response?",
                options=[
                    "Something went wrong — re-enter the new hire record",
                    "The dashboard refreshes overnight — they'll appear tomorrow morning",
                    "Headcount dashboards are unreliable",
                    "Call IT to force a manual refresh",
                ],
                correct_index=1,
                explanation="Most headcount dashboards refresh on a daily batch schedule. A new hire entered in the afternoon won't appear until the next refresh cycle. This is normal data lag, not an error.",
            ),
        ],
        tip="Make a simple list for your team: 'These systems update in real-time. These update nightly. These update weekly.' Post it where everyone can see it. It prevents a huge number of 'why doesn't my change show up?' questions.",
    )


# ---------------------------------------------------------------------------
# Lesson 7: The People Between the Systems
# ---------------------------------------------------------------------------


def lesson_human_handoffs() -> Lesson:
    """Build the 'The People Between the Systems' lesson."""
    bad_data = pd.DataFrame({
        "Employee ID": ["E1001", "E1002", "E1003", "E1004", "E1005"],
        "Name": ["Amy Chen", "Brian Davis", "Carlos Ruiz", "Diana Kim", "Eric Walsh"],
        "Department": ["Sales", "Engineering", "Marketing", "Finance", "Sales"],
        "Salary": ["$85,000", "$110,000", "$72,000", "$95,000", "$88,000"],
        "Manager": ["Diana Kim", "Amy Chen", "Eric Walsh", "Carlos Ruiz", "Brian Davis"],
    })

    good_data = pd.DataFrame({
        "Employee ID": ["E1001", "E1002", "E1003", "E1004", "E1005"],
        "Name": ["Amy Chen", "Brian Davis", "Carlos Ruiz", "Diana Kim", "Eric Walsh"],
        "Department": ["Engineering", "Engineering", "Marketing", "Finance", "Sales"],
        "Salary": ["$110,000", "$85,000", "$72,000", "$95,000", "$88,000"],
        "Manager": ["Tom Lee", "Tom Lee", "Sara Jones", "Pat Clark", "Sara Jones"],
    })

    return Lesson(
        id="human_handoffs",
        title="The People Between the Systems",
        icon="👤",
        order=7,
        concept="Data doesn't always flow through automated pipes. Sometimes a human copies data from one system to another using Excel. When someone sorts one column without selecting all columns, or pastes into the wrong row, the data becomes silently corrupted.",
        bad_data=bad_data,
        downstream_impact=(
            "**What breaks:**\n\n"
            "- Someone sorted the Name column alphabetically but forgot to select Salary and Manager — now salaries are attached to the wrong people\n"
            "- Amy Chen appears to earn $85K but her real salary is $110K — compensation analysis is wrong\n"
            "- Every manager field is now misaligned — the org chart makes no sense\n"
            "- If this spreadsheet is uploaded back into a system, it corrupts the source data\n\n"
            "**Real-world example:** An HR analyst exports a 2,000-row spreadsheet, sorts by last name to find someone, accidentally sorts only one column, saves, and emails it to Finance. Finance uses it for budget planning. Nobody notices until a manager questions why their direct report's salary is $40K less than expected."
        ),
        good_data=good_data,
        body=(
            "### Why This Matters\n"
            "Even in companies with modern HR systems, a surprising amount of data moves through Excel spreadsheets. Someone exports from one system, edits in Excel, and uploads to another system — or emails it to a colleague. Every manual step is a chance for human error. The most dangerous part? These errors are silent. The spreadsheet looks fine. Nobody gets an error message.\n\n"
            "### Key Vocabulary\n"
            "- **Manual handoff**: When data moves between systems via human action (copy-paste, email, upload)\n"
            "- **Column sort error**: Sorting one column without selecting all data, misaligning rows\n"
            "- **Silent corruption**: Data that looks correct but is actually wrong — no error message, no warning\n"
            "- **Data integrity**: The assurance that data is accurate and consistent throughout its lifecycle\n\n"
            "### How to Spot It\n"
            "- A manager says \"these numbers don't look right\" about a spreadsheet\n"
            "- Salary data seems randomly assigned — values don't match expected ranges for roles\n"
            "- The org chart has people reporting to managers in completely different departments\n\n"
            "### Common Mistakes\n"
            "- Sorting a single column in Excel instead of the entire table\n"
            "- Copy-pasting data without verifying row alignment\n"
            "- Not using 'Format as Table' in Excel (which prevents single-column sorts)\n"
            "- Sending spreadsheets via email instead of using shared system access\n\n"
            "### How to Fix It\n"
            "- Always select ALL columns before sorting in Excel (Ctrl+A then sort)\n"
            "- Use Excel Tables (Ctrl+T) — they automatically sort all columns together\n"
            "- Spot-check: after any manipulation, verify 3-4 rows match what you expect\n"
            "- Where possible, eliminate manual handoffs — use direct system integrations or APIs\n"
            "- If you must use spreadsheets, protect the sheet structure and add validation rules"
        ),
        quiz=[
            QuizQuestion(
                question="After the sort error, Amy Chen's salary shows as $85,000 instead of $110,000. What type of error is this?",
                options=[
                    "A calculation error",
                    "A silent corruption error — the data looks valid but is wrong",
                    "A formatting error",
                    "A system bug in Excel",
                ],
                correct_index=1,
                explanation="This is silent corruption. $85,000 is a perfectly valid salary, so no error message appears. The spreadsheet looks fine. But Amy's real salary is $110,000 — the sort error moved another person's salary into her row.",
            ),
            QuizQuestion(
                question="What is the simplest way to prevent single-column sort errors in Excel?",
                options=[
                    "Never sort any data",
                    "Use 'Format as Table' (Ctrl+T) which forces full-table sorts",
                    "Always sort in descending order",
                    "Lock the spreadsheet so nobody can edit it",
                ],
                correct_index=1,
                explanation="Excel Tables (Ctrl+T) are designed to keep data together. When you sort a Table, Excel automatically includes all columns. This one habit prevents the most common spreadsheet corruption error.",
            ),
        ],
        tip="Before you email any spreadsheet with employee data, spot-check 3 random rows. Pick an employee you know and verify their department, salary, and manager are correct. If even one is wrong, the data may be corrupted.",
    )


# ---------------------------------------------------------------------------
# Lesson 8: How to Trace a Data Problem Back to Its Source
# ---------------------------------------------------------------------------


def lesson_trace_problem() -> Lesson:
    """Build the 'How to Trace a Data Problem Back to Its Source' lesson."""
    bad_data = pd.DataFrame({
        "Step": ["1. Board Deck", "2. Finance Report", "3. Data Warehouse", "4. Payroll Export", "5. HRIS (Source)"],
        "What It Shows": ["Avg salary: $94,200", "Dept salary total: $471,000 for 5 people", "5 active employees in Engineering", "5 Engineering employees on payroll", "5 Engineering records — but one has wrong salary"],
        "Employee with Error": ["—", "—", "—", "Jun Park: $82,000", "Jun Park: $82,000 (should be $92,000)"],
        "Status": ["Wrong metric", "Wrong total", "Count is correct", "Wrong salary propagated", "ROOT CAUSE: typo in salary field"],
    })

    good_data = pd.DataFrame({
        "Step": ["1. Board Deck", "2. Finance Report", "3. Data Warehouse", "4. Payroll Export", "5. HRIS (Source)"],
        "What It Shows": ["Avg salary: $96,200", "Dept salary total: $481,000 for 5 people", "5 active employees in Engineering", "5 Engineering employees on payroll", "5 Engineering records — all correct"],
        "Employee Fixed": ["—", "—", "—", "Jun Park: $92,000", "Jun Park: $92,000 (corrected at source)"],
        "Status": ["Correct metric", "Correct total", "Count is correct", "Correct salary", "Source data is accurate"],
    })

    return Lesson(
        id="trace_problem",
        title="How to Trace a Data Problem Back to Its Source",
        icon="🔍",
        order=8,
        concept="When a number in a report looks wrong, don't just fix the report. Trace the data backward through each system until you find where the error was introduced. Fix it there — at the root — so it doesn't come back.",
        bad_data=bad_data,
        downstream_impact=(
            "**What breaks:**\n\n"
            "- The board deck shows average Engineering salary as $94,200 instead of $96,200 — a $2,000 gap per person\n"
            "- Finance's budget model underestimates Engineering compensation costs\n"
            "- Jun Park is underpaid by $10,000/year due to a typo nobody caught\n"
            "- If HR benchmarks salaries against this data, they'll set new hire offers too low\n\n"
            "**Real-world example:** A VP notices the average salary metric seems low compared to market data. Instead of dismissing it, she asks the analytics team to trace it. They follow the chain: board deck ← finance report ← data warehouse ← payroll ← HRIS. The root cause is a $10K typo in one employee's salary. It took 45 minutes to trace and 2 minutes to fix."
        ),
        good_data=good_data,
        body=(
            "### Why This Matters\n"
            "This lesson ties everything together. You've learned that data flows from source to downstream systems (Lesson 1), that source and reporting systems can disagree (Lesson 2), that definitions matter (Lesson 3), that errors multiply (Lesson 4), that you need a single source of truth (Lesson 5), that timing affects what you see (Lesson 6), and that human handoffs introduce risk (Lesson 7). Now you learn the skill that makes all of that actionable: tracing a problem back to its root.\n\n"
            "### Key Vocabulary\n"
            "- **Data lineage**: The documented path data takes from source to report\n"
            "- **Root cause analysis**: The process of tracing an error back to where it was first introduced\n"
            "- **Upstream**: Closer to the source system (where data is entered)\n"
            "- **Downstream**: Farther from the source (where data is consumed in reports)\n"
            "- **Trace-back**: Following a data value from report back to source, system by system\n\n"
            "### How to Spot It\n"
            "- A metric in a report seems \"off\" but nobody can explain why\n"
            "- A manager says \"this doesn't match what I expected\" about salary, headcount, or tenure data\n"
            "- Two reports that should agree show different numbers for the same metric\n\n"
            "### Common Mistakes\n"
            "- Fixing the number in the report or dashboard without investigating the source\n"
            "- Assuming the most recent system in the chain introduced the error\n"
            "- Giving up when the trace involves more than 2 systems\n"
            "- Not documenting the data lineage so future trace-backs are easier\n\n"
            "### How to Fix It\n"
            "- Start at the report where the wrong number appears\n"
            "- Ask: \"Where does this report get its data?\" Move one system upstream.\n"
            "- At each system, check: is the data correct here? If yes, the error is downstream. If no, keep going upstream.\n"
            "- When you find the system where the error first appears, you've found the root cause. Fix it there.\n"
            "- Document the path you followed — this becomes your data lineage documentation."
        ),
        quiz=[
            QuizQuestion(
                question="The board deck shows average Engineering salary as $94,200. You suspect it's wrong. What is the correct first step?",
                options=[
                    "Change the number in the board deck to what you think it should be",
                    "Ask Finance where their salary data comes from and check that system",
                    "Recalculate the average yourself using a separate spreadsheet",
                    "Assume it's rounding and ignore it",
                ],
                correct_index=1,
                explanation="The correct approach is to trace backward. The board deck gets data from Finance, Finance gets data from the data warehouse, and so on. Start by asking where the data comes from and check each system in the chain until you find where the error was introduced.",
            ),
            QuizQuestion(
                question="You're tracing a wrong salary back through the data chain. The data warehouse shows the wrong number, but the HRIS also shows the wrong number. What does this tell you?",
                options=[
                    "Both systems have independent bugs",
                    "The error originated in the HRIS (the source) and propagated to the data warehouse",
                    "The data warehouse corrupted the HRIS data",
                    "Someone manually changed both systems",
                ],
                correct_index=1,
                explanation="Since the HRIS is the source system, and it shows the wrong number, the error originated there. The data warehouse simply copied the already-wrong data. Fix it in the HRIS and the correction will flow downstream.",
            ),
        ],
        tip="When tracing a data problem, draw the chain on a piece of paper: Report ← Dashboard ← Data Warehouse ← Payroll ← HRIS. Then check each node. The first node that shows the wrong data is where the error lives. This takes minutes, not hours.",
    )
