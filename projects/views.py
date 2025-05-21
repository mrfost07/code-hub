from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, STATUS_CHOICES, PRIORITY_CHOICES
from .forms import ProjectForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from tasks.models import STATUS_CHOICES as TASK_STATUS_CHOICES
from tasks.models import Task
from notifications.utils import notify_project_action

@login_required
def project_list(request):
    projects = Project.objects.all()
    
    # Get filter parameters from request
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    
    # Apply filters if provided
    if search_query:
        projects = projects.filter(name__icontains=search_query)
    
    if status_filter:
        projects = projects.filter(status=status_filter)
    
    if priority_filter:
        projects = projects.filter(priority=priority_filter)
    
    # Get choices for dropdowns
    status_choices = STATUS_CHOICES
    priority_choices = PRIORITY_CHOICES
    
    context = {
        'projects': projects,
        'status_choices': status_choices,
        'priority_choices': priority_choices,
        'search_query': search_query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
    }
    
    return render(request, 'projects/project_list.html', context)

@login_required
def project_detail(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id)
        return render(request, 'projects/project_detail.html', {'project': project})
    except:
        # If project doesn't exist, redirect to project list with a message
        messages.warning(request, 'The project you are looking for does not exist or has been deleted.')
        return redirect('projects:project_list')

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()  # Save many-to-many relationships
            
            # Create notification for team members
            notify_project_action(project, request.user, f"created a new project: {project.name}")
            
            messages.success(request, 'Project created successfully!')
            return redirect('projects:project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})

@login_required 
def kanban_board(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Create a mapping of status values to display names
    status_display = dict(TASK_STATUS_CHOICES)
    
    # Get ALL tasks for this project without any filtering whatsoever
    # Using direct ORM query with model._base_manager to completely bypass the custom manager
    all_tasks = Task._base_manager.filter(project=project).select_related('owner')
    
    # For debugging - print the count of tasks found
    task_count = all_tasks.count()
    print(f"Found {task_count} tasks for project {project.id}")
    
    # Define columns with their display names and tasks
    columns = [
        {
            'status': 'BACKLOG',
            'title': status_display['BACKLOG'],
            'tasks': all_tasks.filter(status='BACKLOG'),
            'color': 'secondary'
        },
        {
            'status': 'TODO',
            'title': status_display['TODO'],
            'tasks': all_tasks.filter(status='TODO'),
            'color': 'info'
        },
        {
            'status': 'IN_PROGRESS',
            'title': status_display['IN_PROGRESS'],
            'tasks': all_tasks.filter(status='IN_PROGRESS'),
            'color': 'primary'
        },
        {
            'status': 'REVIEW',
            'title': status_display['REVIEW'],
            'tasks': all_tasks.filter(status='REVIEW'),
            'color': 'warning'
        },
        {
            'status': 'DONE',
            'title': status_display['DONE'],
            'tasks': all_tasks.filter(status='DONE'),
            'color': 'success'
        }
    ]
    
    context = {
        'project': project,
        'columns': columns,
        'total_task_count': task_count,
    }
    return render(request, 'projects/kanban_board.html', context)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    template_name = 'projects/project_form.html'
    fields = ['name', 'description', 'status', 'priority', 'due_date', 'team']
    
    def test_func(self):
        project = self.get_object()
        return self.request.user == project.owner or \
               self.request.user in project.team.team_lead.all()

    def get_success_url(self):
        return reverse_lazy('projects:project_detail', kwargs={'project_id': self.object.id})
    
    def form_valid(self, form):
        # Store original values for comparison
        original_obj = self.get_object()
        original_status = original_obj.status
        
        # Let the original form_valid method handle saving
        response = super().form_valid(form)
        
        # Create notification message
        notification_msg = f"updated project: {self.object.name}"
        
        # Add status change information if status has changed
        if original_status != self.object.status:
            status_display = dict(STATUS_CHOICES)
            notification_msg += f" - status changed from '{status_display[original_status]}' to '{status_display[self.object.status]}'"
        
        # Create notification
        notify_project_action(self.object, self.request.user, notification_msg)
        
        return response

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('projects:project_list')
    
    def test_func(self):
        project = self.get_object()
        return self.request.user == project.owner or \
               self.request.user in project.team.team_lead.all()
    
    def delete(self, request, *args, **kwargs):
        project = self.get_object()
        
        # Create notification before deleting
        notify_project_action(project, request.user, f"deleted project: {project.name}")
        
        # Proceed with deletion
        return super().delete(request, *args, **kwargs)
