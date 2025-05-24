from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Value, CharField
from django.db.models.functions import Concat
from projects.models import Project
from tasks.models import Task
from teams.models import Team


@login_required
def search(request):
    """
    Global search view that searches across projects, tasks, and teams.
    Filters results based on user access permissions.
    """
    query = request.GET.get('q', '')
    user = request.user
    
    # Initialize empty querysets
    projects = []
    tasks = []
    teams = []
    total_results = 0
    
    if query:
        # Get user's teams
        user_teams = Team.objects.filter(members=user)
        
        # Search in Projects - filter to only show projects the user can access
        projects = Project.objects.filter(
            (Q(owner=user) | Q(team__in=user_teams)) &
            (Q(name__icontains=query) | 
             Q(description__icontains=query) |
             Q(status__icontains=query))
        ).distinct().select_related('owner', 'team')
        
        # Search in Tasks - filter to only show tasks the user can access
        # (owned by user or in a project the user has access to)
        tasks = Task.objects.filter(
            (Q(owner=user) | Q(project__owner=user) | Q(project__team__in=user_teams)) &
            (Q(title__icontains=query) | 
             Q(description__icontains=query) |
             Q(status__icontains=query))
        ).distinct().select_related('owner', 'project')
        
        # Search in Teams - filter to only show teams the user is a member of
        teams = Team.objects.filter(
            Q(members=user) &
            (Q(name__icontains=query) | 
            Q(description__icontains=query))
        ).distinct().prefetch_related('members')
        
        # Calculate total results
        total_results = projects.count() + tasks.count() + teams.count()
    
    context = {
        'query': query,
        'projects': projects,
        'tasks': tasks,
        'teams': teams,
        'total_results': total_results
    }
    
    return render(request, 'search_results.html', context) 