# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design includes four classes: Owner, Pet, Task, and Scheduler. Owner manages pet ownership and preferences, Pet manages pet details and care tasks, Task stores individual job details and completion status, and Scheduler organizes tasks into a daily plan based on priority and available time. The relationships are simple: one owner has many pets, one pet has many tasks, and the scheduler uses those objects to build a schedule.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After reviewing my UML diagram and Python class skeletons with AI, I confirmed that the four classes matched and had clear responsibilities. One change I made was allowing an Owner to have zero or more Pets instead of requiring at least one. This allows users to create a profile before adding a pet. AI also suggested that the get_pet() method could eventually return None when a pet is not found, which I can address during implementation. Overall, I kept the design simple and modular so the scheduling logic can be added later.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My PawPal+ scheduler considers several constraints, including the owner's available time, task duration, priority level, and scheduled time. I decided that priority and available time were the most important because essential pet care tasks should be completed first without exceeding the owner's daily time limit. The scheduler sorts tasks by high, medium, and low priority, then selects tasks that fit within the available time. I also implemented time sorting and conflict detection to help organize tasks and identify overlapping activities. Although owners can enter preferences, they do not currently affect the scheduling algorithm.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff I made was choosing a simple conflict detection algorithm instead of a more advanced approach. My algorithm uses nested loops to compare the scheduled times and durations of tasks to identify overlaps. This has O(n²) time complexity, meaning it becomes less efficient as more tasks are added. My AI assistant suggested sorting tasks first to improve performance, but I decided to keep the original approach because it is easier to understand and debug. Since PawPal+ is designed for a small number of pets and tasks, I felt that simplicity and readability were more important than optimizing performance.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI throughout the project to help brainstorm the initial system design, generate Python code, implement scheduling algorithms, and debug errors. AI was especially helpful when connecting my backend classes to the Streamlit interface and implementing features like recurring tasks and conflict detection. The most useful prompts were specific instructions that explained what I wanted the code to accomplish while keeping the implementation simple. I also used separate AI chat sessions for different phases of the project, which helped keep the development process organized and focused.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One time I did not accept an AI suggestion as-is was when I asked how to improve my conflict detection algorithm. The AI suggested sorting tasks before checking for overlaps to improve efficiency. However, I decided to keep my original nested-loop approach because it was easier to understand and worked well for a small application. I evaluated the suggestion by comparing the readability and time complexity of both approaches. I also verified my implementation by running the CLI demonstration and automated tests to make sure the scheduling features worked correctly.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested several important behaviors of my PawPal+ system, including adding pets and tasks, marking tasks complete, sorting tasks chronologically, detecting scheduling conflicts, and generating recurring tasks. I also checked that the scheduler respected the owner's available time and handled situations where pets had no tasks. These tests were important because they helped verify that the different classes and scheduling algorithms worked together correctly. I used pytest for automated testing and ran the CLI program to see how the scheduling logic behaved with example tasks.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I would rate my confidence in the scheduler as 4 out of 5 stars. The main features worked during testing, and the automated tests helped confirm that the system behaved as expected. However, I recognize that passing tests does not guarantee that every possible situation is handled correctly. If I had more time, I would test more complicated scheduling conflicts involving multiple pets, tasks that overlap by only a few minutes, and recurring tasks scheduled across different weeks or months. These additional tests would help identify issues that might not appear during normal use.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The part of this project I am most satisfied with is successfully connecting the Python backend to a working Streamlit application. It was rewarding to see the classes and algorithms I developed become features that a user could actually interact with. I also liked implementing the smarter scheduling features because they made the application more useful than a basic task manager. Being able to add pets, create tasks, and generate schedules through a working interface showed me how different parts of a software system come together.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve the scheduling algorithm to consider more constraints and make better decisions when tasks overlap. Currently, the scheduler mainly prioritizes tasks based on importance and available time, while conflict detection identifies potential problems. I would like to make the system automatically suggest alternative times for conflicting tasks. I would also improve how owner preferences influence scheduling

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One important thing I learned from this project is that using AI effectively requires more than just asking it to generate code. AI can make the development process much faster by helping with design, implementation, and debugging, but it is still important to understand and evaluate its suggestions. I learned that my role is to guide the overall design, decide which solutions make sense, and verify that the final system meets the requirements. This project helped me understand how AI can be used as a development tool while keeping the human responsible for important engineering decisions.
