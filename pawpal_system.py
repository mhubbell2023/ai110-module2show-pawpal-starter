from __future__ import annotations

from dataclasses import dataclass, field


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

    def get_all_tasks(self) -> list["Task"]:
        """Collects all tasks across the owner's pets."""
        tasks: list[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
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

    def mark_complete(self) -> None:
        """Marks the task as complete."""
        self.completed = True

    def reset_status(self) -> None:
        """Resets the task to incomplete."""
        self.completed = False


class Scheduler:
    """Builds a simple daily schedule."""

    def generate_daily_schedule(self, owner: Owner) -> list[Task]:
        """Creates a daily schedule for an owner."""
        tasks = owner.get_all_tasks()
        incomplete_tasks = [task for task in tasks if not task.completed]
        priority_sorted = self.sort_by_priority(incomplete_tasks)
        return self.fit_available_time(priority_sorted, owner.available_time)

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sorts tasks by priority and scheduled time."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        time_order = {"morning": 0, "afternoon": 1, "evening": 2, "unscheduled": 3}

        return sorted(
            tasks,
            key=lambda task: (
                priority_order.get(task.priority.lower(), 99),
                time_order.get(task.scheduled_time.lower(), 99),
                task.duration,
            ),
        )

    def fit_available_time(self, tasks: list[Task], available_time: int) -> list[Task]:
        """Keeps tasks that fit within the owner's time."""
        selected: list[Task] = []
        total_duration = 0

        for task in tasks:
            if total_duration + task.duration <= available_time:
                selected.append(task)
                total_duration += task.duration

        return selected

    def explain_schedule(self, schedule: list[Task]) -> str:
        """Explains the selected schedule."""
        if not schedule:
            return "No tasks fit within the available time for this day."

        task_names = ", ".join(task.name for task in schedule)
        return f"The schedule includes: {task_names}. Tasks are ordered by priority and fit within the available time."
