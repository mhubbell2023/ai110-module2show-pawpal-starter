from pawpal_system import Owner, Pet, Task, Scheduler


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


if __name__ == "__main__":
    main()
