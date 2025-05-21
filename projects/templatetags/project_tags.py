from django import template

register = template.Library()

@register.filter
def get_status_color(status):
    colors = {
        'BACKLOG': 'secondary',
        'TODO': 'info',
        'IN_PROGRESS': 'primary',
        'REVIEW': 'warning',
        'DONE': 'success'
    }
    return colors.get(status, 'secondary')

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
