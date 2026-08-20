const taskApiUrl = "http://127.0.0.1:8000/tasks";
const taskList = document.getElementById("task-list");
const taskMessage = document.getElementById("task-message");

async function loadTasks() {
    taskMessage.textContent = "Loading tasks…";

    try {
        const response = await fetch(taskApiUrl);

        if (!response.ok) {
            throw new Error("Task request failed");
        }

        const tasks = await response.json();
        taskList.innerHTML = "";

        if (tasks.length === 0) {
            taskMessage.textContent = "No tasks yet.";
            return;
        }

        taskMessage.textContent = "";

        for (const task of tasks) {
            const taskItem = document.createElement("li");
            taskItem.dataset.uid = task.uid;
            taskItem.dataset.isComplete = task.is_complete;
            const title = document.createElement("h3");
            title.textContent = task.title;
            taskItem.append(title);
            const description = document.createElement("p");
            description.textContent = task.description;
            taskItem.append(description);
            const status = document.createElement("p");
            status.textContent = task.is_complete ? "Status: Complete" : "Status: Incomplete";
            status.classList.add("status");
            taskItem.append(status);
            taskList.append(taskItem);
        }
    } catch (error) {
        taskList.innerHTML = "";
        taskMessage.textContent = "Unable to load tasks. Please try again.";
        console.error(error);
    }
}

loadTasks();
