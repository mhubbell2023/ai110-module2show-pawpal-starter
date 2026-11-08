# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

<img width="1572" height="464" alt="image" src="https://github.com/user-attachments/assets/4354e6a8-3869-4eb8-b119-6b4afebe7e50" />


## 🧪 Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

This project verifies the core scheduling behaviors, including:

- chronological ordering with `Scheduler.sort_by_time()`
- daily recurring tasks creating a next-day occurrence
- overlap/conflict detection when two tasks share the same time window
- scheduling only within the owner's available time
- safe handling of pets with no scheduled tasks

Successful pytest output:

```text
================================ 7 passed in 0.12s =================================
```

Confidence: ★★★★★ (5/5)

The passing test results show the main scheduling behaviors are working as expected, which gives strong confidence in the current project logic and scope.

## 📐 Smarter Scheduling

PawPal+ uses several scheduling helpers to turn a list of pet-care tasks into a realistic daily plan.

- `Scheduler.sort_by_time()` arranges tasks in chronological order based on each task’s scheduled start time. This makes the day easier to read and helps the planner work through the plan in time order.
- `Scheduler.filter_tasks()` narrows the task list by pet name and/or completion status. For example, you can view only the tasks for a specific pet, or hide tasks that are already complete.
- `Task.mark_complete()` updates a task to complete and, when the task repeats, creates the next scheduled occurrence. `Task.create_next_occurrence()` builds the next daily or weekly task object using the same details and the next time value.
- `Scheduler.detect_overlaps()` checks whether two task time ranges cross each other and returns a warning message when a conflict is found. This is useful for catching problems such as overlapping walks, feedings, or grooming sessions.
- `Scheduler.generate_daily_schedule()` combines filtering, sorting, and the owner’s available_time limit so the app picks the most appropriate tasks for the day.

These methods support the main scheduling ideas behind PawPal+:

- chronological sorting with `sort_by_time()`
- filtering by pet and completion status with `filter_tasks()`
- recurring daily and weekly tasks using `mark_complete()` and `create_next_occurrence()`
- conflict detection with `detect_overlaps()`

This helps the system stay organized while still being simple enough for a beginner Python project.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
