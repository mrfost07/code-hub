from .models import Notification
from django.db.models import Q

def notifications(request):
    if request.user.is_authenticated:
        # Get all notifications for the user
        all_notifications = Notification.objects.filter(receipient=request.user).order_by('-created_at')
        unread_count = all_notifications.filter(read=False).count()
        
        # Get the latest notifications (limit to 10)
        latest_notifications = all_notifications[:10]
        
        # Organize notifications by type
        categorized_notifications = {
            'progress': [],      # Task/project progress updates
            'member': [],        # Team member additions
            'creation': [],      # New task/project creations
            'updates': [],       # Updates to projects and tasks
            'profile': []        # Profile related notifications
        }
        
        # Categorize notifications
        for notif in latest_notifications:
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
        
        return {
            'latest_notifications': latest_notifications,
            'categorized_notifications': categorized_notifications,
            'notification_count': unread_count
        }
    return {'latest_notifications': [], 'categorized_notifications': {}, 'notification_count': 0}
