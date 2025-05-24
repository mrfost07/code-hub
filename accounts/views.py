from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from .forms import UserRegistrationForm, UserProfileForm
from projects.models import Project
from tasks.models import Task
from .models import Profile
from notifications.models import Notification  # Fixed typo in import
from notifications.utils import create_profile_notification, create_system_notification
from teams.models import Team
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.timezone import timezone


# class DashboardView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, "accounts/dashboard.html")

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
            
        # Get user's projects (either as team member or owner)
        latest_projects = Project.objects.filter(
            team__members=request.user
        ).distinct() | Project.objects.filter(
            owner=request.user
        ).distinct().order_by('-created_at')

        # Get user's tasks
        latest_tasks = Task.objects.filter(
            owner=request.user
        ).select_related('project').order_by('-created_at')

        # Get all team members from teams the user is part of
        User = get_user_model()
        user_teams = request.user.teams.all()
        
        team_members = []
        for team in user_teams:
            team_members.extend(team.members.all())
        
        # Convert to set to remove duplicates then back to list
        team_members = list(set(team_members))
        
        # Get profiles for all team members
        member_profiles = []
        for user in team_members:
            if hasattr(user, 'profile'):
                member_profiles.append(user.profile)
        
        # Sort by most recent join date
        latest_members = sorted(member_profiles, key=lambda x: x.user.date_joined, reverse=True)

        context = {}
        if request.user.is_authenticated:
            latest_notifications = Notification.objects.for_user(request.user).order_by('-created_at')
            context["latest_notifications"] = latest_notifications[:3]
            context["notification_count"] = latest_notifications.count()
            
        context["latest_projects"] = latest_projects[:5]
        context["latest_project_count"] = latest_projects.count()
        context["latest_tasks"] = latest_tasks[:5]
        context["latest_task_count"] = latest_tasks.count()
        context["latest_members"] = latest_members[:8]
        context["latest_member_count"] = len(latest_members)
        context["team_count"] = user_teams.count()
        
        return render(request, "accounts/dashboard.html", context)

@login_required
def dashboard(request):
    # Get projects where the user is a team member or owner
    user_projects = Project.objects.filter(team__members=request.user) | Project.objects.filter(owner=request.user)
    # Get tasks owned by the user
    user_tasks = Task.objects.filter(owner=request.user)
    context = {
        'projects': user_projects,
        'tasks': user_tasks
    }
    return render(request, 'accounts/dashboard.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('accounts:dashboard')
        messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create a notification instead of a message
            create_system_notification(
                user=user, 
                verb="Your account has been created successfully", 
                system_object=user
            )
            
            # Still show success message for login page
            messages.success(request, 'Your account has been created successfully! You can now log in with your username and password.')
            return redirect('accounts:login')
        else:
            # If there are form errors, render the form with errors
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def profile(request, user_id=None):
    # Check if we're viewing another user's profile
    User = get_user_model()
    
    if user_id:
        try:
            profile_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, "User doesn't exist")
            return redirect('accounts:dashboard')
    else:
        # Check for user_id in query params for backward compatibility
        query_user_id = request.GET.get('user_id')
        if query_user_id:
            try:
                profile_user = User.objects.get(id=query_user_id)
            except User.DoesNotExist:
                messages.error(request, "User doesn't exist")
                return redirect('accounts:dashboard')
        else:
            profile_user = request.user
    
    # Get user's projects (either as team member or owner)
    projects_as_member = [team.projects.all() for team in Team.objects.filter(members=profile_user)]
    flat_projects_as_member = [project for queryset in projects_as_member for project in queryset]
    projects_as_owner = Project.objects.filter(owner=profile_user)
    projects = list(projects_as_owner) + flat_projects_as_member
    
    # Get user's tasks (either assigned directly or as part of user's projects)
    tasks = Task.objects.filter(owner=profile_user)
    
    # Get user's notifications (most recent first) - only for own profile
    notifications = []
    if profile_user == request.user:
        notifications = Notification.objects.filter(receipient=profile_user).order_by('-created_at')[:10]
    
    # Calculate analytics data for projects by status
    project_status_counts = {
        'To Do': 0,
        'In Progress': 0,
        'Completed': 0
    }
    for project in projects:
        project_status_counts[project.status] = project_status_counts.get(project.status, 0) + 1
    
    # Calculate analytics data for tasks by status
    from tasks.models import STATUS_CHOICES
    task_status_dict = dict(STATUS_CHOICES)
    task_status_counts = {
        'BACKLOG': 0,
        'TODO': 0,
        'IN_PROGRESS': 0,
        'REVIEW': 0,
        'DONE': 0
    }
    for task in tasks:
        task_status_counts[task.status] = task_status_counts.get(task.status, 0) + 1
    
    context = {
        'user': profile_user,
        'is_own_profile': profile_user == request.user,
        'projects': projects,
        'tasks': tasks,
        'notifications': notifications,
        'project_status_counts': project_status_counts,
        'task_status_counts': task_status_counts,
        'task_status_labels': {k: task_status_dict.get(k, k) for k in task_status_counts.keys()}
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                file = request.FILES['profile_picture']
                # Create a safe filename
                ext = file.name.split('.')[-1]
                filename = f"{request.user.username}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
                profile.profile_picture.save(filename, file, save=False)
            
            profile.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'page_title': 'Edit Profile',
    })

def email_verification(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified. You can now login.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'The verification link was invalid or has expired.')
        return redirect('accounts:register')
