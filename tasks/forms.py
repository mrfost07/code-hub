from django import forms
from .models import Task, STATUS_CHOICES
from django.utils import timezone
from projects.models import Project

class TaskForm(forms.ModelForm):
    # Explicitly define the status field to ensure it uses the correct choices
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=True)
    
    # Add default start date of today
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now().date()
    )
    
    # Add project field as required
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Task
        fields = ['name', 'description', 'project', 'status', 'priority', 'start_date', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Ensure status field shows the correct value when editing
        if self.instance and self.instance.pk:
            self.initial['status'] = self.instance.status
