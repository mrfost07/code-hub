from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task, STATUS_CHOICES, PRIORITY_CHOICES
from .forms import TaskForm
from projects.models import Project  # Assuming the Project model is in projects app
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from notifications.utils import notify_task_action
from django.db.models import Q

@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)
    
    # Get filter parameters from request
    search_query = request.GET.get('search', '')
    priority_filter = request.GET.get('priority', '')
    status_filter = request.GET.get('status', '')
    
    # Apply filters if provided
    if search_query:
        tasks = tasks.filter(name__icontains=search_query)
    
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
        
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    # Get choices for dropdowns
    priority_choices = PRIORITY_CHOICES
    status_choices = STATUS_CHOICES
    
    context = {
        'tasks': tasks,
        'priority_choices': priority_choices,
        'status_choices': status_choices,
        'search_query': search_query,
        'priority_filter': priority_filter,
        'status_filter': status_filter,
    }
    
    return render(request, 'tasks/task_list.html', context)

@login_required
def task_detail(request, task_id):
    try:
        task = get_object_or_404(Task, id=task_id)
        return render(request, 'tasks/task_detail.html', {'task': task})
    except:
        # If task doesn't exist, redirect to task list with a message
        messages.warning(request, 'The task you are looking for does not exist or has been deleted.')
        return redirect('tasks:task_list')

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            
            # Explicitly set status from form data to ensure it's preserved
            task.status = form.cleaned_data['status']
            
            # Ensure the task is active
            task.active = True
            task.save()
            
            # Create notification
            if task.project:
                notify_task_action(task, request.user, f"created a new task '{task.name}' in project '{task.project.name}'")
            
            messages.success(request, 'Task created successfully!')
            # If task is created within a project, redirect to that project's kanban board
            if task.project:
                return redirect('projects:kanban_board', project_id=task.project.id)
            return redirect('tasks:task_detail', task_id=task.id)
    else:
        # Set a default status of TODO for new tasks
        form = TaskForm(initial={'status': 'TODO'})
        
        # Limit projects to ones the user has access to (owned by user or in teams user belongs to)
        user_projects = Project.objects.filter(
            Q(owner=request.user) | 
            Q(team__members=request.user)
        ).distinct()
        form.fields['project'].queryset = user_projects
        
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create Task'})

@login_required 
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Store original values for comparison
    original_status = task.status
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            # Explicitly set status from form data before saving
            task.status = form.cleaned_data['status']
            updated_task = form.save()
            
            # Create notification about the update
            notifications_message = f"updated task '{updated_task.name}'"
            
            # Add status change specific notification if status changed
            if original_status != updated_task.status:
                status_display = dict(STATUS_CHOICES)
                notifications_message += f" - status changed from '{status_display[original_status]}' to '{status_display[updated_task.status]}'"
            
            # Make sure to pass the current user as the actor
            notify_task_action(updated_task, request.user, notifications_message)
            
            messages.success(request, 'Task updated successfully!')
            return redirect('tasks:task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)
        
        # Limit projects to ones the user has access to
        user_projects = Project.objects.filter(
            Q(owner=request.user) | 
            Q(team__members=request.user)
        ).distinct()
        form.fields['project'].queryset = user_projects
        
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Update Task'})

@login_required
def create_project_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.owner = request.user
            
            # Explicitly set status from form data to ensure it's preserved
            task.status = form.cleaned_data['status']
            
            # Ensure the task is active
            task.active = True
            task.save()
            
            # Create notification
            notify_task_action(task, request.user, f"created a new task '{task.name}' in project '{project.name}'")
            
            messages.success(request, 'Task created successfully!')
            # Redirect to kanban board instead of project detail
            return redirect('projects:kanban_board', project_id=project.id)
    else:
        # Set a default status of TODO for new tasks
        form = TaskForm(initial={'project': project, 'status': 'TODO'})
        # Only allow selecting the current project
        form.fields['project'].queryset = Project.objects.filter(id=project.id)
        form.fields['project'].initial = project
        form.fields['project'].widget.attrs['readonly'] = True
    
    return render(request, 'tasks/task_form.html', {
        'form': form, 
        'title': f'Create Task for {project.name}',
        'project': project
    })

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    
    def test_func(self):
        task = self.get_object()
        return (self.request.user == task.owner or 
                self.request.user == task.project.owner or
                self.request.user in task.project.team.members.all())

    def get_success_url(self):
        return reverse_lazy('tasks:task_detail', kwargs={'task_id': self.object.id})
        
    def form_valid(self, form):
        # Store original task for notification purposes
        original_task = self.get_object()
        original_status = original_task.status
        
        # Save the form
        response = super().form_valid(form)
        
        # Create notification if status changed
        if original_status != self.object.status:
            status_display = dict(STATUS_CHOICES)
            # Make sure to pass the current user as the actor
            notify_task_action(
                self.object, 
                self.request.user,  # Explicitly use the current user
                f"updated task '{self.object.name}' - status changed from '{status_display[original_status]}' to '{status_display[self.object.status]}'"
            )
        
        return response

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task_list')
    
    def test_func(self):
        task = self.get_object()
        return (self.request.user == task.owner or 
                self.request.user == task.project.owner or
                self.request.user in task.project.team.members.all())

@login_required
@require_http_methods(["POST"])
def update_task_status(request, task_id):
    try:
        task = get_object_or_404(Task, id=task_id)
        
        # Allow project owner, task owner, or any team member to update task status
        is_team_member = request.user in task.project.team.members.all()
        if not (request.user == task.owner or request.user == task.project.owner or is_team_member):
            return JsonResponse({
                'success': False,
                'error': 'Permission denied: You must be the task owner, project owner, or a team member'
            }, status=403)

        data = json.loads(request.body)
        new_status = data.get('status')
        
        # Import STATUS_CHOICES from models at the top of the file if not already imported
        from .models import STATUS_CHOICES
        valid_statuses = [choice[0] for choice in STATUS_CHOICES]
        status_display = dict(STATUS_CHOICES)
        
        if new_status not in valid_statuses:
            return JsonResponse({
                'success': False,
                'error': f'Invalid status value. Must be one of: {valid_statuses}'
            }, status=400)

        # Store original status for notification
        original_status = task.status

        # Update task status
        task.status = new_status
        task.save()
        
        # Create notification about status change with more kanban-oriented messaging
        if original_status != new_status:
            # Determine movement direction in Kanban flow
            progression_map = {
                'BACKLOG': 0,
                'TODO': 1,
                'IN_PROGRESS': 2,
                'REVIEW': 3,
                'DONE': 4
            }
            
            # Enhanced notification based on progress direction
            if progression_map.get(new_status, 0) > progression_map.get(original_status, 0):
                action_verb = f"moved task '{task.name}' forward on the Kanban board from '{status_display[original_status]}' to '{status_display[new_status]}'"
            elif progression_map.get(new_status, 0) < progression_map.get(original_status, 0):
                action_verb = f"moved task '{task.name}' backward on the Kanban board from '{status_display[original_status]}' to '{status_display[new_status]}'"
            else:
                action_verb = f"updated task '{task.name}' status from '{status_display[original_status]}' to '{status_display[new_status]}'"
            
            # Always explicitly set the actor to be the current user making the request
            notify_task_action(
                task, 
                request.user,  # Explicitly use the current user who made the request
                f"{action_verb} (Progress: {task.progress}%)"
            )
        
        # Update project progress
        task.project.update_progress()
        
        # Reload the project to get the latest status after the update
        project = task.project
            
        return JsonResponse({
            'success': True,
            'task_progress': task.progress,
            'project_progress': project.progress,
            'project_status': project.status
        })
        
    except Task.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Task not found'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': str(e)
        }, status=500)
