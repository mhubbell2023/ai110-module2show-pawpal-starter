from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Owner:
    """Represents a pet owner and their available time and pet list."""

    owner_id: str
    name: str
    available_time: int
    preferences: list[str] = field(default_factory=list)
    pets: list["Pet"] = field(default_factory=list)

    def add_pet(self, pet: "Pet") -> None:
        """Add a pet to the owner's collection."""
        pass

    def remove_pet(self, pet: "Pet") -> None:
        """Remove a pet from the owner's collection."""
        pass

    def get_pet(self, name: str) -> "Pet":
        """Get a pet by name from the owner's collection."""
        pass


@dataclass
class Pet:
    """Represents a pet and its scheduled care tasks."""

    pet_id: str
    name: str
    age: int
    breed: str
    care_tasks: list["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Add a care task to the pet."""
        pass

    def remove_task(self, task: "Task") -> None:
        """Remove a care task from the pet."""
        pass

    def get_tasks(self) -> list["Task"]:
        """Return the list of tasks for this pet."""
        pass


@dataclass
class Task:
    """Represents a single pet care task."""

    task_id: str
    name: str
    duration: int
    priority: str
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        pass

    def reset_status(self) -> None:
        """Reset the task back to an incomplete status."""
        pass


class Scheduler:
    """Organizes pet care tasks into a daily schedule."""

    def generate_daily_schedule(self, owner: Owner) -> list[Task]:
        """Create a daily schedule for the owner based on their pets and tasks."""
        pass

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority so the most important tasks come first."""
        pass

    def fit_available_time(self, tasks: list[Task], available_time: int) -> list[Task]:
        """Select tasks that fit within the owner's available time."""
        pass

    def explain_schedule(self, schedule: list[Task]) -> str:
        """Return an explanation of the scheduling decisions."""
        pass
