from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
from projects.models import Project

STATUS_CHOICES = [
    ('BACKLOG', 'Backlog'),
    ('TODO', 'To Do'), 
    ('IN_PROGRESS', 'In Progress'),
    ('REVIEW', 'Review'),
    ('DONE', 'Done'),
]


PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]


class TaskQueryset(models.QuerySet):
    def active(self):
        return self.filter(active=True)
    
    def upcoming(self):
        return self.filter(due_date__gte=timezone.now())
    

class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQueryset(self.model, using=self._db)
    
    def all(self):
        # Return all tasks by default, without filtering by active status
        return self.get_queryset()
    
    def active(self):
        # New method for active tasks only
        return self.get_queryset().active()
    
    def upcoming(self):
        # Method for upcoming tasks only
        return self.get_queryset().active().upcoming()
    
    # Add a method to get all tasks for a project regardless of status or due date
    def for_project(self, project_id):
        return self.get_queryset().filter(project_id=project_id)

class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="BACKLOG")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="Medium")
    start_date = models.DateField()
    due_date = models.DateField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TaskManager()


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

    
    def days_until_due(self):
        if self.due_date:
            #get current date
            current_date = timezone.now().date()
            return (self.due_date - current_date).days
        return None
    
    @property
    def progress(self):
        progress_dict = {
            'BACKLOG': 0,
            'TODO': 25,
            'IN_PROGRESS': 50,
            'REVIEW': 75,
            'DONE': 100,
        }
        return progress_dict.get(self.status, 0)
    

    @property
    def status_color(self):
        status_value = self.progress
        if status_value == 100:
            color = "success"
        elif status_value == 50:
            color = "primary"
        else:
            color = ""
        return color

           
    

    def priority_color(self):
        if self.priority == "Low":
            color = "success"
        elif self.priority == "Medium":
            color = "warning"
        else:
            color = "danger"
        return color

    def update_project_progress(self):
        """Update associated project progress"""
        if self.project:
            self.project.update_progress()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_project_progress()

class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class TaskDependency(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='dependencies')
    depends_on = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='dependent_tasks')




