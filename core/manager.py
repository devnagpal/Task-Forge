from datetime import datetime,timedelta
from .base import Task,Reminder
from .storage import load_tasks,load_reminders,save_tasks,save_reminders

class TaskManager:
    def __init__(self,settings,engine):
        self.settings=settings
        self.engine=engine
        self.tasks=[]
        raw=load_tasks()
        for td in raw.get("Tasks",[]):
            self.tasks.append(Task.dictionary(td))
    def _save(self):
        save_tasks({"Tasks":[task.dic() for task in self.tasks]})
    def add_task(self,title: str,category:str="General",due_date:str=None,reminders_enabled:bool=True):
        task=Task(title, category,due_date,reminders_enabled=reminders_enabled)
        self.tasks.append(task)
        self._save()
        return task
    def add_subtask(self,parent_id:str,title:str,category:str="General",due_date:str=None,reminders_enabled:bool=True):
        parent=self.find_task(parent_id)
        if not parent:
            return None
        st=Task(title,category,due_date,reminders_enabled=reminders_enabled)
        parent.add_subtask(st)
        self._save()
        return st
    def find_task(self,taskid:str):
        for t in self.tasks:
            if t.id==taskid:
                return t
            hit=self.find_subtasks(t.subtasks,taskid)
            if hit:
                return hit
        return None
    def find_subtasks(self,subtasks,taskid):
        for st in subtasks:
            if st.id==taskid:
                return st
            found=self.find_subtasks(st.subtasks,taskid)
            if found:
                return found
        return None
    def delete_task(self,taskid:str):
        for i, t in enumerate(self.tasks):
            if t.id==taskid:
                self.tasks.pop(i)
                self._save()
                self.engine.remove_reminders(taskid)
                return True
            if self.delete_subtasks(t,taskid):
                self._save()
                self.engine.remove_reminders(taskid)
                return True
        return False
    def delete_subtasks(self,task:Task,taskid:str):
        for i, st in enumerate(task.subtasks):
            if st.id==taskid:
                task.subtasks.pop(i)
                return True
            if self.delete_subtasks(st, taskid):
                return True
        return False
    def complete_task(self,taskid:str):
        task=self.find_task(taskid)
        if not task:
            return None
        task.completed=True
        self._save()
        created=self.engine.schedule_for_task_completion(task,datetime.now())
        return created
    def incomplete_task(self,taskid:str):
        task=self.find_task(taskid)
        if not task:
            return None
        task.completed=False
        self._save()
        return task
    def toggle_reminders(self,taskid:str):
        task=self.find_task(taskid)
        if not task:
            return None
        current=getattr(task,"reminders_enabled",True)
        new_state=not current
        task.reminders_enabled=new_state
        self._save()
        if new_state is False:
            self.engine.remove_reminders(taskid)
        else:
            self.engine.schedule_for_task_completion(task,datetime.now())
        return new_state
    
class ReminderManager:
    def __init__(self,settings):
        self.settings=settings
        self.reminders=[]
        raw=load_reminders()
        for rd in raw.get("Reminders",[]):
            self.reminders.append(Reminder.dictionary(rd))
    def _save(self):
        save_reminders({"Reminders":[rm.dic() for rm in self.reminders]})
    def schedule_for_task_completion(self,task:Task,completion_date:datetime):
        if not getattr(task,"reminders_enabled",True):
            return []
        intervals=self.settings.get_intervals(task.category)
        created=[]
        for days in intervals:
            due_on=completion_date+timedelta(days=int(days))
            if task.category.upper()=="STUDY":
                title=f"Revise: {task.title}"
            else:
                title=task.title
            r=Reminder(task.id,title,due_on)
            self.reminders.append(r)
            created.append(r)
        self._save()
        return created
    def remove_reminders(self,taskid:str):
        before=len(self.reminders)
        self.reminders=[r for r in self.reminders if r.taskid!=taskid]
        after=len(self.reminders)
        if before!=after:
            self._save()
    def list_due(self):
        return sorted(self.reminders,key=lambda r: r.due_on)
    def save(self):
        self._save()