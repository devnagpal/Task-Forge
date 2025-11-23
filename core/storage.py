import os
import json
import tempfile

BASE=os.path.join(os.path.dirname(__file__), '..', 'data')
TASK_FILE=os.path.join(BASE, 'tasks.json')
REMINDERS_FILE=os.path.join(BASE, 'reminders.json')
SETTINGS_FILE=os.path.join(BASE, 'settings.json')

DEFAULT_TASKS={"Tasks":[]}
DEFAULT_REMINDERS={"Reminders":[]}
DEFAULT_SETTINGS={"ReminderIntervals":{"STUDY":[1,3,7,15,30],"IMPORTANT":[1,3],"NORMAL":[1,3],"DAILY":[1,2,3,4,5,6,7]}}
def ensure_files(path,default):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, 'w',encoding='utf-8') as f:
            json.dump(default, f, indent=2)
def safe_write(path,data):
    ensure_files(path,{})
    fd,temp=tempfile.mkstemp(dir=os.path.dirname(path))
    with os.fdopen(fd,'w',encoding='utf-8') as f:
        json.dump(data,f,indent=2)
    os.replace(temp,path)
def load_json(path,default):
    ensure_files(path,default)
    try:
        with open(path,'r',encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default.copy()
def save_json(path,data):
    safe_write(path,data)

def load_tasks():
    return load_json(TASK_FILE,DEFAULT_TASKS)
def load_reminders():
    return load_json(REMINDERS_FILE,DEFAULT_REMINDERS)
def load_settings():
    return load_json(SETTINGS_FILE,DEFAULT_SETTINGS)

def save_tasks(data):
    save_json(TASK_FILE,data)
def save_reminders(data):
    save_json(REMINDERS_FILE,data)
def save_settings(data):
    save_json(SETTINGS_FILE,data)