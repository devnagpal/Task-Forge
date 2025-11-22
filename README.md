# TASK FORGE 
### A Smart To-Do List Revision Planner

Task Forge is a simple and smart Task And Revision Planning Sytem. It helps students plan their work, track progess and systematically revise their topics/tasks through reminders.

## Features:
• Tasks having categories : STUDY , IMPORTANT , NORMAL , DAILY
<br>
• Tasks can have Sub-Tasks
<br>
• Mark Tasks or Sub-Tasks as Complete or Incomplete
<br>
• Toggle Reminders ON or OFF for specific Tasks
<br>
• Automatic Reminder Scheduler based on Task Category
<br>
• Data/Storage Management using JSON files
<br>
• Simple Menu-Driven Project

## Technologies/Tools Used:
• Python
• JSON
• Git/GitHub

## Steps to Run The Project:
• Open your Terminal or VSCode Integrated Terminal and run:
• git clone https://github.com/devnagpal/Task-Forge.git
<br>
• then, run: cd Task-Forge
<br>
• Make sure Python-3 is installed
<br>
• run python main.py

## Instructions for Testing:

• You'll see a menu like this:
===== SMART REVISION PLANNER =====
1. View all tasks
2. Add task
3. Add subtask
4. Complete task
5. Uncomplete task
6. Toggle reminders
7. Delete task
8. View reminders
0. Exit

• The app saves and loads all data from the data folder:
data/tasks.json
data/reminders.json
data/settings.json
Your tasks and reminders stay even after closing the program.

• if "python main.py" doesn't work, try: python3 main.py
