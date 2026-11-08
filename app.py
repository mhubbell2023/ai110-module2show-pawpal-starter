import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        owner_id="owner_001",
        name="Jordan",
        available_time=90,
        preferences=["balanced routine"],
    )

owner = st.session_state.owner

st.markdown(
    """
Welcome to the PawPal+ starter app.

This UI stores the owner, pets, and tasks in `st.session_state` so the data remains available
between Streamlit reruns while you work on the app.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

st.subheader("Owner Details")
with st.form("owner_form"):
    owner.name = st.text_input("Owner name", value=owner.name)
    owner.available_time = st.number_input(
        "Available time (minutes)", min_value=30, max_value=240, value=owner.available_time
    )
    submitted_owner = st.form_submit_button("Update owner")
    if submitted_owner:
        st.session_state.owner = owner

st.divider()

st.subheader("Add Pet")
with st.form("pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    age = st.number_input("Age", min_value=0, max_value=30, value=2)
    breed = st.text_input("Breed", value="Mixed breed")
    if st.form_submit_button("Add pet"):
        pet = Pet(
            pet_id=f"pet_{len(owner.pets) + 1}",
            name=pet_name,
            age=int(age),
            breed=breed,
        )
        owner.add_pet(pet)
        st.session_state.owner = owner
        st.success(f"Added {pet.name} to {owner.name}'s pets.")

st.divider()

st.subheader("Add Task")
if owner.pets:
    selected_pet_name = st.selectbox("Select pet", [pet.name for pet in owner.pets])
    with st.form("task_form"):
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        scheduled_time = st.selectbox("Scheduled time", ["morning", "afternoon", "evening"])

        if st.form_submit_button("Add task"):
            selected_pet = owner.get_pet(selected_pet_name)
            if selected_pet is not None:
                task = Task(
                    task_id=f"task_{len(selected_pet.care_tasks) + 1}",
                    name=task_title,
                    duration=int(duration),
                    priority=priority,
                    scheduled_time=scheduled_time,
                    frequency="daily",
                )
                selected_pet.add_task(task)
                st.session_state.owner = owner
                st.success(f"Added '{task.name}' to {selected_pet.name}.")
else:
    st.info("Add a pet before creating tasks.")

st.divider()

st.subheader("Pets and Tasks")
if owner.pets:
    for pet in owner.pets:
        st.markdown(f"### {pet.name} ({pet.breed})")
        if pet.get_tasks():
            for task in pet.get_tasks():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    status = "✅ Complete" if task.completed else "⏳ Incomplete"
                    st.write(f"{task.name} - {status}")
                with col2:
                    st.write(f"{task.scheduled_time} | {task.priority}")
                with col3:
                    if st.button(f"Mark complete", key=f"complete_{pet.pet_id}_{task.task_id}"):
                        task.mark_complete()
                        st.session_state.owner = owner
                        st.rerun()
        else:
            st.caption("No tasks yet.")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler()
    schedule = scheduler.generate_daily_schedule(owner)

    st.markdown("### Today's Schedule")
    if schedule:
        for index, task in enumerate(schedule, start=1):
            st.write(
                f"{index}. {task.name} | Time: {task.scheduled_time} | "
                f"Duration: {task.duration} min | Priority: {task.priority}"
            )
        st.success(scheduler.explain_schedule(schedule))
    else:
        st.info("No tasks fit within the available time for today.")

st.markdown(
    """
This app stores the `Owner` object in `st.session_state`, and then the Add Pet and Add Task
buttons call methods like `Owner.add_pet()` and `Pet.add_task()` directly. When the user clicks
"Generate schedule", the app calls `Scheduler.generate_daily_schedule(owner)` and shows the result.
"""
)
