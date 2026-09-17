from django import template

register = template.Library()

@register.filter
def duration_format(value):
    if not value:
        return "0m"

    total_seconds = int(value.total_seconds())

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    if hours > 0 and minutes > 0:
        return f"{hours}h {minutes}m"

    if hours > 0:
        return f"{hours}h"

    return f"{minutes}m"