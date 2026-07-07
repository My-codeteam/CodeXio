from django import template

register = template.Library()


@register.filter(name='short_number')
def short_number(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value

    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}".rstrip("0").rstrip(".") + "B"

    elif value >= 1_000_000:
        return f"{value / 1_000_000:.1f}".rstrip("0").rstrip(".") + "M"

    elif value >= 1_000:
        return f"{value / 1_000:.1f}".rstrip("0").rstrip(".") + "K"

    return int(value)