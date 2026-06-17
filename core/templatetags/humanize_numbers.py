from django import template

register = template.Library()

@register.filter
def short_number(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if value >= 1_000_000_000:
        return f"{value/1_000_000_000:.1f}B".replace(".0", "")
    elif value >= 1_000_000:
        return f"{value/1_000_000:.1f}M".replace(".0", "")
    elif value >= 1_000:
        return f"{value/1_000:.1f}K".replace(".0", "")
    return str(value)