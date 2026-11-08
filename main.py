from pawpal_system import Owner, Pet, Task, Scheduler, time_to_minutes


def main() -> None:
    """Runs a simple PawPal+ scheduling demo."""
    owner = Owner(
        owner_id="owner_001",
        name="Alex",
        available_time=90,
        preferences=["balanced routine", "morning care"],
    )

    pet1 = Pet(pet_id="pet_001", name="Buddy", age=4, breed="Golden Retriever")
    pet2 = Pet(pet_id="pet_002", name="Milo", age=2, breed="Tabby Cat")

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = Task(
        task_id="task_001",
        name="Morning Walk",
        duration=30,
        priority="high",
        scheduled_time="morning",
        frequency="daily",
    )
    task2 = Task(
        task_id="task_002",
        name="Feed Dinner",
        duration=20,
        priority="high",
        scheduled_time="evening",
        frequency="daily",
    )
    task3 = Task(
        task_id="task_003",
        name="Brush Coat",
        duration=25,
        priority="medium",
        scheduled_time="afternoon",
        frequency="daily",
    )
    task4 = Task(
        task_id="task_004",
        name="Litter Cleanup",
        duration=15,
        priority="low",
        scheduled_time="afternoon",
        frequency="daily",
    )

    pet1.add_task(task1)
    pet1.add_task(task3)
    pet2.add_task(task2)
    pet2.add_task(task4)

    scheduler = Scheduler()
    schedule = scheduler.generate_daily_schedule(owner)

    print("\nToday's Schedule")
    print("-" * 50)
    for index, task in enumerate(schedule, start=1):
        print(
            f"{index}. {task.name:<18} | "
            f"Time: {task.scheduled_time:<9} | "
            f"Duration: {task.duration} min | "
            f"Priority: {task.priority}"
        )

    print("-" * 50)
    print(scheduler.explain_schedule(schedule))

    print("\nDemonstration 1: Chronological sorting using sort_by_time()")
    print("-" * 50)
    for index, task in enumerate(scheduler.sort_by_time(schedule), start=1):
        print(f"{index}. {task.name:<18} | Time: {task.scheduled_time:<9} | Duration: {task.duration} min")

    print("\nDemonstration 2: Filtering by pet and completion status")
    print("-" * 50)
    filtered_tasks = scheduler.filter_tasks(owner.get_all_tasks(), pet_name="Buddy", completed=False)
    if filtered_tasks:
        for index, task in enumerate(filtered_tasks, start=1):
            print(f"{index}. {task.name:<18} | Pet: {task.pet_name:<8} | Complete: {task.completed}")
    else:
        print("No tasks matched the selected pet and status filter.")

    print("\nDemonstration 3: Generating a new recurring task after completion")
    print("-" * 50)
    recurring_task = Task(
        task_id="task_005",
        name="Evening Meal Prep",
        duration=25,
        priority="medium",
        scheduled_time="18:00",
        frequency="daily",
    )
    recurring_task.mark_complete()
    next_task = recurring_task.create_next_occurrence()
    print(f"Completed task: {recurring_task.name} -> completed={recurring_task.completed}")
    if next_task is not None:
        print(
            f"Next occurrence created: {next_task.name} | "
            f"Time: {next_task.scheduled_time} | "
            f"Next occurrence: {next_task.next_occurrence}"
        )
    else:
        print("No recurring task was generated.")

    print("\nDemonstration 4: Detecting overlapping tasks")
    print("-" * 50)
    overlap_tasks = [
        Task(
            task_id="overlap_001",
            name="Morning Grooming",
            duration=45,
            priority="high",
            scheduled_time="09:00",
            frequency="daily",
        ),
        Task(
            task_id="overlap_002",
            name="Quick Vet Check",
            duration=30,
            priority="high",
            scheduled_time="09:30",
            frequency="daily",
        ),
    ]
    warnings = scheduler.detect_overlaps(overlap_tasks)
    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print("No overlapping tasks detected.")


if __name__ == "__main__":
    main()
