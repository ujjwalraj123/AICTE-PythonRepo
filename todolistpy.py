!pip install colorama
!pip install gradio
import gradio as gr

# Initialize the task list
tasks = []

# Function to add a task
def add_task(task):
    if task.strip() != "":
        tasks.append({"task": task, "completed": False})
        return update_task_list(), f"Task '{task}' added successfully!"
    return update_task_list(), "Task cannot be empty!"

# Function to delete a task
def delete_task(task_index):
    if 0 <= task_index < len(tasks):
        removed_task = tasks.pop(task_index)
        return update_task_list(), f"Task '{removed_task['task']}' deleted successfully!"
    return update_task_list(), "Invalid task number."

# Function to mark a task as complete
def mark_task_complete(task_index):
    if 0 <= task_index < len(tasks):
        tasks[task_index]['completed'] = True
        return update_task_list(), f"Task '{tasks[task_index]['task']}' marked as complete!"
    return update_task_list(), "Invalid task number."

# Function to display the task list
def update_task_list():
    if not tasks:
        return "No tasks available."
    task_display = ""
    for i, task in enumerate(tasks):
        status = "✔ Completed" if task['completed'] else "❌ Incomplete"
        task_display += f"{i + 1}. {task['task']} - {status}\n"
    return task_display.strip()

# Gradio Interface
def app(action, task="", task_index=0):
    if action == "Add Task":
        return add_task(task)
    elif action == "Delete Task":
        return delete_task(task_index - 1)
    elif action == "Mark Complete":
        return mark_task_complete(task_index - 1)
    return update_task_list(), ""

with gr.Blocks() as todo_app:
    gr.Markdown("# 📝 To-Do List App")
    with gr.Row():
        action = gr.Radio(["Add Task", "Delete Task", "Mark Complete"], label="Action", value="Add Task")
    task_input = gr.Textbox(label="Task (for Add Task)", placeholder="Enter your task here")
    task_index_input = gr.Number(label="Task Number (for Delete/Complete)", value=0)
    output = gr.Textbox(label="To-Do List", lines=10, interactive=False)
    message = gr.Textbox(label="Message", lines=2, interactive=False)
    submit = gr.Button("Submit")

    submit.click(app, [action, task_input, task_index_input], [output, message])

todo_app.launch()
