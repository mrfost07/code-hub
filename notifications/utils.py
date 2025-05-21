from django.contrib.contenttypes.models import ContentType
from .models import Notification
from django.contrib.auth.models import User

def create_notification(recipient, actor, verb, content_object):
    """
    Create a notification for a user about an object.
    
    Args:
        recipient: User who will receive the notification
        actor: User who performed the action
        verb: String describing the action
        content_object: The model instance that was acted upon
    
    Returns:
        The created Notification object
    """
    content_type = ContentType.objects.get_for_model(content_object)
    
    notification = Notification.objects.create(
        receipient=recipient,
        actor=actor,
        verb=verb,
        content_type=content_type,
        object_id=str(content_object.id)
    )
    
    return notification

def create_profile_notification(user, actor, verb):
    """
    Create a notification about a user's profile
    
    Args:
        user: User whose profile is being referenced
        actor: User who performed the action (can be same as user)
        verb: String describing the action (e.g., "updated your profile")
    
    Returns:
        The created Notification object
    """
    # The user receives notification about their own profile
    return create_notification(recipient=user, actor=actor, verb=verb, content_object=user)

def create_system_notification(user, verb, system_object):
    """
    Create a system notification for a user
    
    Args:
        user: User who will receive the notification
        verb: String describing what happened
        system_object: Object related to the notification
    
    Returns:
        The created Notification object
    """
    # For system notifications, we use the system as the actor (admin user)
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        # If no admin user exists, use the same user
        admin_user = user
        
    return create_notification(recipient=user, actor=admin_user, verb=verb, content_object=system_object)

def notify_project_action(project, actor, action_verb):
    """
    Create notifications for all team members when a project action occurs
    
    Args:
        project: The Project instance
        actor: User who performed the action
        action_verb: String describing the action (e.g., "created a project", "updated a project")
    """
    # Notify all team members except the actor
    for member in project.team.members.all():
        if member != actor:
            create_notification(
                recipient=member,
                actor=actor,
                verb=action_verb,
                content_object=project
            )
    
    # Also notify the project owner if different from actor
    if project.owner != actor and project.owner not in project.team.members.all():
        create_notification(
            recipient=project.owner,
            actor=actor,
            verb=action_verb,
            content_object=project
        )

def notify_task_action(task, actor, action_verb):
    """
    Create notifications for relevant users when a task action occurs
    
    Args:
        task: The Task instance
        actor: User who performed the action
        action_verb: String describing the action (e.g., "created a task", "updated a task status")
    """
    # Notify task owner if different from actor
    if task.owner != actor:
        create_notification(
            recipient=task.owner,
            actor=actor,
            verb=action_verb,
            content_object=task
        )
    
    # Notify project owner if different from actor and task owner
    if task.project.owner != actor and task.project.owner != task.owner:
        create_notification(
            recipient=task.project.owner,
            actor=actor,
            verb=action_verb,
            content_object=task
        )
    
    # Also notify all team members about the task update
    if hasattr(task.project, 'team') and task.project.team:
        for member in task.project.team.members.all():
            # Don't notify the actor or people already notified
            if member != actor and member != task.owner and member != task.project.owner:
                create_notification(
                    recipient=member,
                    actor=actor,
                    verb=action_verb,
                    content_object=task
                ) 