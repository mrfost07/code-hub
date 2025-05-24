from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Team
from .forms import TeamForm, TeamMemberForm
from notifications.utils import create_notification

# Create your views here.

@login_required
def team_list(request):
    teams = Team.objects.all()
    return render(request, 'teams/team_list.html', {'teams': teams})

@login_required
def team_detail(request, team_id):
    try:
        team = get_object_or_404(Team, id=team_id)
        member_form = TeamMemberForm()
        return render(request, 'teams/team_detail.html', {
            'team': team,
            'member_form': member_form
        })
    except:
        # If team doesn't exist, redirect to team list with a message
        messages.warning(request, 'The team you are looking for does not exist or has been deleted.')
        return redirect('teams:team_list')

@login_required
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.created_by = request.user
            team.team_lead = request.user
            team.save()
            team.members.add(request.user)
            messages.success(request, 'Team created successfully.')
            return redirect('teams:team_detail', team.id)
    else:
        form = TeamForm()
    return render(request, 'teams/team_form.html', {'form': form})

@login_required
def add_member(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            if user not in team.members.all():
                team.members.add(user)
                
                # Create notification for the added member
                create_notification(
                    recipient=user,
                    actor=request.user,
                    verb=f"added you as a member to team '{team.name}'",
                    content_object=team
                )
                
                # Notify team lead if they're not the one adding the member
                if team.team_lead != request.user:
                    create_notification(
                        recipient=team.team_lead,
                        actor=request.user,
                        verb=f"added {user.username} to team '{team.name}'",
                        content_object=team
                    )
                
                messages.success(request, f'{user.username} has been added to the team.')
            else:
                messages.warning(request, f'{user.username} is already a team member.')
            return redirect('teams:team_detail', team_id=team.id)
    else:
        form = TeamMemberForm()
    
    return render(request, 'teams/member_form.html', {
        'form': form,
        'team': team
    })

@login_required
def remove_member(request, team_id, user_id):
    try:
        team = get_object_or_404(Team, id=team_id)
        User = get_user_model()
        user = get_object_or_404(User, id=user_id)
        
        if user in team.members.all():
            if user != team.team_lead:
                team.members.remove(user)
                messages.success(request, f'{user.username} has been removed from the team.')
            else:
                messages.error(request, 'Cannot remove team lead from the team.')
        return redirect('teams:team_detail', team_id=team.id)
    except:
        messages.warning(request, 'The team you are looking for does not exist or has been deleted.')
        return redirect('teams:team_list')
