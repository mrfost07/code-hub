from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

@login_required
def notification_list(request):
    # Get all notifications for the user
    all_notifications = Notification.objects.filter(receipient=request.user).order_by('-created_at')
    
    # Create categorized notifications
    categorized_notifications = {
        'progress': [],      # Task/project progress updates
        'member': [],        # Team member additions
        'creation': [],      # New task/project creations
        'updates': [],       # Updates to projects and tasks
        'profile': []        # Profile related notifications
    }
    
    # Categorize notifications
    for notif in all_notifications:
        verb_lower = notif.verb.lower()
        content_type = str(notif.content_object).lower() if notif.content_object else ""
        
        # Task created by team members goes to creation
        if 'created' in verb_lower and 'task' in verb_lower:
            categorized_notifications['creation'].append(notif)
        
        # Team membership notifications
        elif ('added' in verb_lower and 'member' in verb_lower) or \
             ('added to' in verb_lower and 'team' in verb_lower):
            categorized_notifications['member'].append(notif)
            
        # Progress tracking notifications
        elif 'progress' in verb_lower or 'moved' in verb_lower or 'status' in verb_lower:
            categorized_notifications['progress'].append(notif)
            
        # Profile related notifications
        elif 'profile' in verb_lower or 'account' in verb_lower:
            categorized_notifications['profile'].append(notif)
            
        # Project and task updates (not creations or status changes)
        elif ('updated' in verb_lower or 'changed' in verb_lower or 'edited' in verb_lower) and \
             ('project' in verb_lower or 'task' in verb_lower or 'project' in content_type or 'task' in content_type):
            categorized_notifications['updates'].append(notif)
            
        # Default case - put in updates if it involves a project or task
        elif 'project' in verb_lower or 'task' in verb_lower:
            categorized_notifications['updates'].append(notif)
            
        # Remaining notifications
        else:
            # Find the best category based on content
            if 'task' in content_type:
                categorized_notifications['updates'].append(notif)
            elif 'team' in content_type:
                categorized_notifications['member'].append(notif)
            elif 'project' in content_type:
                categorized_notifications['updates'].append(notif)
            elif 'user' in content_type:
                categorized_notifications['profile'].append(notif)
            else:
                # If all else fails, put in updates
                categorized_notifications['updates'].append(notif)
    
    return render(request, 'notifications/notification_list.html', {
        'latest_notifications': all_notifications,
        'categorized_notifications': categorized_notifications
    })

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, receipient=request.user)
    notification.read = True
    notification.save()
    return redirect('notifications:notification_list')

@login_required
def mark_all_as_read(request):
    Notification.objects.filter(receipient=request.user, read=False).update(read=True)
    return redirect('notifications:notification_list')

@login_required
def cleanup_notifications(request):
    """Clean up notifications that reference non-existent objects"""
    deleted_count = 0
    
    # Get all notifications for the user
    notifications = Notification.objects.filter(receipient=request.user)
    
    # Check each notification
    for notif in notifications:
        try:
            # If content_object can't be retrieved, the referenced object doesn't exist
            if notif.content_object is None:
                notif.delete()
                deleted_count += 1
        except:
            # If there's an error accessing content_object, delete the notification
            notif.delete()
            deleted_count += 1
    
    messages.success(request, f'Cleaned up {deleted_count} notifications referencing deleted items.')
    return redirect('notifications:notification_list')
