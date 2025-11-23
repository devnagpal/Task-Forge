import uuid
from datetime import datetime

class Task:
    def __init__(self,title,category,due_date,reminders_enabled:bool=True):
        self.id = str(uuid.uuid4())
        self.title = title
        self.category = category
        self.due_date = None
        if due_date:
            try:
                self.due_date=datetime.strptime(due_date,"%Y-%m-%d")
            except ValueError:
                self.due_date=None
        self.reminders_enabled = reminders_enabled
        self.completed=False
        self.subtasks=[]
    def add_subtask(self,subtask):
        self.subtasks.append(subtask)
    def dic(self):
        return {"id":self.id,"title":self.title,"category":self.category,"due_date":self.due_date.strftime("%Y-%m-%d") if self.due_date else None,"reminders_enabled":self.reminders_enabled,"completed":self.completed,"subtasks":[subtask.dic() for subtask in self.subtasks]}
    @staticmethod
    def dictionary(d):
        task=Task(d["title"],d["category"],d["due_date"],d.get("reminders_enabled",True))
        task.id=d["id"]
        task.completed=d.get("completed",False)
        task.subtasks=[Task.dictionary(subtask) for subtask in d.get("subtasks",[])]
        return task
    
class Reminder:
    def __init__(self,taskid,title,due_on):
        self.id=str(uuid.uuid4())
        self.taskid=taskid
        self.title=title
        self.due_on=due_on
        self.done=False
    def dic(self):
        return {"id":self.id,"taskid":self.taskid,"title":self.title,"due_on":self.due_on.strftime("%Y-%m-%d"),"done":self.done}
    @staticmethod
    def dictionary(d):
        reminder=Reminder(d["taskid"],d["title"],datetime.strptime(d["due_on"],"%Y-%m-%d"))
        reminder.id=d["id"]
        reminder.done=d.get("done",False)
        return reminder
