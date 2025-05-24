from django import forms
from django.contrib.auth.models import User
from .models import Task, STATUS_CHOICES
from django.utils import timezone
from projects.models import Project
from django.db.models import Q

class TaskForm(forms.ModelForm):
    # Explicitly define the status field to ensure it uses the correct choices
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=True)
    
    # Add default start date of today
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now().date()
    )
    
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),  # Will be filtered in __init__
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'project', 'status', 'priority', 
                 'start_date', 'due_date', 'assigned_to']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        
        # Handle project filtering
        if user:
            self.fields['project'].queryset = Project.objects.filter(
                Q(owner=user) | Q(team__members=user)
            ).distinct()
            
        # Handle assigned_to field population
        if project:
            # Pre-select project and setup assignees
            self.fields['project'].initial = project
            self.fields['project'].widget.attrs['disabled'] = True
            self.fields['project'].required = False
            
            # Get team members including project owner
            team_members = project.team.members.all()
            self.fields['assigned_to'].queryset = team_members | User.objects.filter(id=project.owner.id)
            
            # If user is not project owner, pre-select themselves
            if user and user != project.owner:
                self.fields['assigned_to'].initial = [user]
                self.fields['assigned_to'].widget.attrs['disabled'] = True
        
        # Add Bootstrap classes
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            
    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get('project')
        assigned_to = cleaned_data.get('assigned_to')
        
        if project and assigned_to:
            # Validate that assigned users are part of the project team or owner
            valid_users = set(project.team.members.all()) | {project.owner}
            invalid_users = set(assigned_to) - valid_users
            
            if invalid_users:
                invalid_usernames = ', '.join(user.username for user in invalid_users)
                raise forms.ValidationError(
                    f"The following users are not part of the project team: {invalid_usernames}"
                )
        
        return cleaned_data
