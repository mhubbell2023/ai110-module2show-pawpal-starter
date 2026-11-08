from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta


def normalize_time_value(value: str) -> str:
    """Converts common labels like morning/afternoon/evening to HH:MM."""
    if value is None:
        return "unscheduled"

    text = str(value).strip().lower()
    if text == "unscheduled":
        return "unscheduled"

    time_map = {
        "morning": "09:00",
        "afternoon": "13:00",
        "evening": "18:00",
    }

    if text in time_map:
        return time_map[text]

    if ":" in text:
        hour, minute = text.split(":", 1)
        try:
            hour_value = int(hour)
            minute_value = int(minute)
            if 0 <= hour_value <= 23 and 0 <= minute_value <= 59:
                return f"{hour_value:02d}:{minute_value:02d}"
        except ValueError:
            return "unscheduled"

    return "unscheduled"


def time_to_minutes(value: str) -> int:
    """Converts HH:MM to minutes since midnight."""
    normalized = normalize_time_value(value)
    if normalized == "unscheduled":
        return 24 * 60

    hour, minute = map(int, normalized.split(":"))
    return hour * 60 + minute


def minutes_to_time(total_minutes: int) -> str:
    """Converts minutes since midnight to HH:MM."""
    hour = total_minutes // 60
    minute = total_minutes % 60
    return f"{hour:02d}:{minute:02d}"


@dataclass
class Owner:
    """Stores owner details and their pets."""

    owner_id: str
    name: str
    available_time: int
    preferences: list[str] = field(default_factory=list)
    pets: list["Pet"] = field(default_factory=list)

    def add_pet(self, pet: "Pet") -> None:
        """Adds a pet to the owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: "Pet") -> None:
        """Removes a pet from the owner."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pet(self, name: str) -> "Pet | None":
        """Finds a pet by name."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None

    def get_all_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list["Task"]:
        """Collects all tasks across the owner's pets. Optional filters keep this easy to reuse."""
        tasks: list[Task] = []
        for pet in self.pets:
            if pet_name is not None and pet.name.lower() != pet_name.lower():
                continue

            pet_tasks = pet.get_tasks()
            if completed is not None:
                pet_tasks = [task for task in pet_tasks if task.completed is completed]
            tasks.extend(pet_tasks)
        return tasks


@dataclass
class Pet:
    """Stores pet details and care tasks."""

    pet_id: str
    name: str
    age: int
    breed: str
    care_tasks: list["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Adds a task to the pet."""
        task.pet_name = self.name
        self.care_tasks.append(task)

    def remove_task(self, task: "Task") -> None:
        """Removes a task from the pet."""
        if task in self.care_tasks:
            self.care_tasks.remove(task)

    def get_tasks(self) -> list["Task"]:
        """Returns the pet's tasks."""
        return self.care_tasks


@dataclass
class Task:
    """Stores a pet care task."""

    task_id: str
    name: str
    duration: int
    priority: str
    completed: bool = False
    scheduled_time: str = "unscheduled"
    frequency: str = "daily"
    pet_name: str = ""
    next_occurrence: datetime | None = None

    def __post_init__(self) -> None:
        """Keeps scheduled times in a consistent HH:MM format."""
        self.scheduled_time = normalize_time_value(self.scheduled_time)

    def mark_complete(self) -> None:
        """Marks the task as complete and schedules the next recurring occurrence when needed."""
        self.completed = True

        if self.frequency.lower() not in {"daily", "weekly"}:
            return

        if self.scheduled_time == "unscheduled":
            current_datetime = datetime.now()
        else:
            current_time = time_to_minutes(self.scheduled_time)
            current_datetime = datetime.now().replace(
                hour=current_time // 60,
                minute=current_time % 60,
                second=0,
                microsecond=0,
            )

        delta = timedelta(days=1) if self.frequency.lower() == "daily" else timedelta(weeks=1)
        self.next_occurrence = current_datetime + delta
        self.scheduled_time = self.next_occurrence.strftime("%H:%M")

    def reset_status(self) -> None:
        """Resets the task to incomplete."""
        self.completed = False

    def create_next_occurrence(self) -> "Task | None":
        """Creates the next version of a repeating task. Returns a new task object."""
        if self.frequency.lower() not in {"daily", "weekly"}:
            return None

        base_time = self.next_occurrence or datetime.now()
        delta = timedelta(days=1) if self.frequency.lower() == "daily" else timedelta(weeks=1)
        next_date = base_time + delta

        return Task(
            task_id=f"{self.task_id}_next",
            name=self.name,
            duration=self.duration,
            priority=self.priority,
            completed=False,
            scheduled_time=next_date.strftime("%H:%M"),
            frequency=self.frequency,
            pet_name=self.pet_name,
            next_occurrence=next_date,
        )


class Scheduler:
    """Builds a simple daily schedule."""

    def generate_daily_schedule(self, owner: Owner) -> list[Task]:
        """Builds a daily plan by filtering, sorting, and keeping tasks that fit the owner's time."""
        tasks = self.filter_tasks(owner.get_all_tasks(), completed=False)
        priority_sorted = self.sort_by_priority(tasks)
        return self.fit_available_time(priority_sorted, owner.available_time)

    def filter_tasks(
        self,
        tasks: list[Task],
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[Task]:
        """Returns tasks matching a pet name and/or completion status."""
        filtered = list(tasks)

        if pet_name is not None:
            filtered = [task for task in filtered if task.pet_name.lower() == pet_name.lower()]

        if completed is not None:
            filtered = [task for task in filtered if task.completed is completed]

        return filtered

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sorts tasks by priority first, then by time so urgent items are scheduled first."""
        priority_order = {"high": 0, "medium": 1, "low": 2}

        return sorted(
            tasks,
            key=lambda task: (
                priority_order.get(task.priority.lower(), 99),
                time_to_minutes(task.scheduled_time),
                task.duration,
                task.name.lower(),
            ),
        )

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Puts tasks in chronological order by their start time."""
        return sorted(tasks, key=lambda task: (time_to_minutes(task.scheduled_time), task.name.lower()))

    def fit_available_time(self, tasks: list[Task], available_time: int) -> list[Task]:
        """Selects tasks that fit within the owner's total daily time budget."""
        selected: list[Task] = []
        total_duration = 0

        for task in tasks:
            if total_duration + task.duration <= available_time:
                selected.append(task)
                total_duration += task.duration

        return selected

    def detect_overlaps(self, tasks: list[Task]) -> list[str]:
        """Looks for task time ranges that cross each other and returns warning messages."""
        warnings: list[str] = []

        for index, first_task in enumerate(tasks):
            first_start = time_to_minutes(first_task.scheduled_time)
            first_end = first_start + first_task.duration

            for second_task in tasks[index + 1 :]:
                second_start = time_to_minutes(second_task.scheduled_time)
                second_end = second_start + second_task.duration

                if first_start < second_end and second_start < first_end:
                    warnings.append(
                        f"Warning: {first_task.name} ({minutes_to_time(first_start)}-{minutes_to_time(first_end)}) "
                        f"overlaps with {second_task.name} ({minutes_to_time(second_start)}-{minutes_to_time(second_end)})."
                    )

        return warnings

    def explain_schedule(self, schedule: list[Task]) -> str:
        """Summarizes the chosen plan in plain English."""
        if not schedule:
            return "No tasks fit within the available time for this day."

        task_names = ", ".join(task.name for task in schedule)
        return f"The schedule includes: {task_names}. Tasks are ordered by priority and time, then filtered to fit within the available time."
