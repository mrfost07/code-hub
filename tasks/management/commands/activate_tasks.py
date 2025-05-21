from django.core.management.base import BaseCommand
from tasks.models import Task

class Command(BaseCommand):
    help = 'Sets all tasks to active status to ensure visibility in kanban board'

    def add_arguments(self, parser):
        parser.add_argument(
            '--project',
            type=str,
            help='Specific project ID to fix tasks for (optional)',
        )

    def handle(self, *args, **options):
        project_id = options.get('project')
        
        if project_id:
            # Fix tasks for a specific project
            inactive_tasks = Task.objects.filter(active=False, project_id=project_id)
            self.stdout.write(f"Setting {inactive_tasks.count()} inactive tasks to active for project {project_id}")
        else:
            # Fix all inactive tasks
            inactive_tasks = Task.objects.filter(active=False)
            self.stdout.write(f"Setting {inactive_tasks.count()} inactive tasks to active across all projects")
        
        # Update the tasks
        update_count = inactive_tasks.update(active=True)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully activated {update_count} tasks')) 