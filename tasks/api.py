from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
import json
from .models import Task, STATUS_CHOICES
from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(["POST"])
def update_task_status(request, task_id):
    try:
        task = get_object_or_404(Task, id=task_id)
        data = json.loads(request.body)
        new_status = data.get('status')
        
        valid_statuses = [choice[0] for choice in STATUS_CHOICES]
        
        if new_status in valid_statuses:
            task.status = new_status
            task.save()  # This will trigger project progress update
            return JsonResponse({
                'success': True,
                'new_status': new_status,
                'task_progress': task.progress,
                'project_progress': task.project.progress
            })
        
        return JsonResponse({
            'success': False, 
            'error': f'Invalid status. Valid values are: {valid_statuses}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': str(e)
        }, status=500)
