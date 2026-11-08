from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion():
    task = Task(
        task_id="task_001",
        name="Walk the dog",
        duration=20,
        priority="high",
        completed=False,
    )

    task.mark_complete()

    assert task.completed is True


def test_task_addition():
    pet = Pet(
        pet_id="pet_001",
        name="Buddy",
        age=4,
        breed="Golden Retriever",
    )

    task = Task(
        task_id="task_002",
        name="Feed dinner",
        duration=15,
        priority="medium",
    )

    assert len(pet.care_tasks) == 0

    pet.add_task(task)

    assert len(pet.care_tasks) == 1


def test_scheduler_sort_by_time_orders_tasks_chronologically():
    scheduler = Scheduler()
    tasks = [
        Task(
            task_id="task_003",
            name="Feed dinner",
            duration=20,
            priority="medium",
            scheduled_time="evening",
        ),
        Task(
            task_id="task_004",
            name="Morning walk",
            duration=30,
            priority="high",
            scheduled_time="morning",
        ),
        Task(
            task_id="task_005",
            name="Brush coat",
            duration=15,
            priority="low",
            scheduled_time="afternoon",
        ),
    ]

    ordered = scheduler.sort_by_time(tasks)

    assert [task.name for task in ordered] == ["Morning walk", "Brush coat", "Feed dinner"]


def test_daily_recurring_task_creates_next_day_occurrence():
    task = Task(
        task_id="task_006",
        name="Morning walk",
        duration=30,
        priority="high",
        scheduled_time="09:00",
        frequency="daily",
        next_occurrence=datetime(2026, 11, 8, 9, 0),
    )

    next_task = task.create_next_occurrence()

    assert next_task is not None
    assert next_task.completed is False
    assert next_task.next_occurrence == datetime(2026, 11, 9, 9, 0)
    assert next_task.scheduled_time == "09:00"
    assert next_task.frequency == "daily"


def test_detect_overlaps_returns_warning_for_conflicting_tasks():
    scheduler = Scheduler()
    tasks = [
        Task(
            task_id="task_007",
            name="Morning Grooming",
            duration=45,
            priority="high",
            scheduled_time="09:00",
            frequency="daily",
        ),
        Task(
            task_id="task_008",
            name="Quick Vet Check",
            duration=30,
            priority="high",
            scheduled_time="09:30",
            frequency="daily",
        ),
    ]

    warnings = scheduler.detect_overlaps(tasks)

    assert len(warnings) == 1
    assert "Morning Grooming" in warnings[0]
    assert "Quick Vet Check" in warnings[0]

    non_overlapping = [
        Task(
            task_id="task_009",
            name="Feeding",
            duration=20,
            priority="medium",
            scheduled_time="09:00",
        ),
        Task(
            task_id="task_010",
            name="Cleaning",
            duration=20,
            priority="low",
            scheduled_time="09:45",
        ),
    ]

    assert scheduler.detect_overlaps(non_overlapping) == []


def test_generate_daily_schedule_respects_owner_available_time():
    owner = Owner(
        owner_id="owner_001",
        name="Alex",
        available_time=90,
    )
    pet = Pet(
        pet_id="pet_001",
        name="Buddy",
        age=4,
        breed="Golden Retriever",
    )
    owner.add_pet(pet)

    morning_walk = Task(
        task_id="task_011",
        name="Morning Walk",
        duration=50,
        priority="high",
        scheduled_time="09:00",
        frequency="daily",
    )
    feed_dinner = Task(
        task_id="task_012",
        name="Feed Dinner",
        duration=30,
        priority="medium",
        scheduled_time="18:00",
        frequency="daily",
    )
    brush_coat = Task(
        task_id="task_013",
        name="Brush Coat",
        duration=25,
        priority="low",
        scheduled_time="13:00",
        frequency="daily",
    )

    pet.add_task(morning_walk)
    pet.add_task(feed_dinner)
    pet.add_task(brush_coat)

    schedule = Scheduler().generate_daily_schedule(owner)

    assert [task.name for task in schedule] == ["Morning Walk", "Feed Dinner"]


def test_pet_with_no_tasks_has_empty_schedule():
    owner = Owner(
        owner_id="owner_002",
        name="Sam",
        available_time=120,
    )
    pet = Pet(
        pet_id="pet_002",
        name="Milo",
        age=2,
        breed="Tabby Cat",
    )
    owner.add_pet(pet)
    scheduler = Scheduler()

    assert owner.get_all_tasks() == []
    assert scheduler.filter_tasks(owner.get_all_tasks(), pet_name="Milo") == []
    assert scheduler.generate_daily_schedule(owner) == []
    assert scheduler.explain_schedule([]) == "No tasks fit within the available time for this day."
