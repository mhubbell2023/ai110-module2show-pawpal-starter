from pawpal_system import Task, Pet


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
