from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument."""
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError):
        return 0

@register.filter
def subtract(value, arg):
    """Subtract the argument from the value."""
    try:
        return Decimal(str(value)) - Decimal(str(arg))
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """Divide the value by the argument."""
    try:
        arg = Decimal(str(arg))
        if arg == 0:
            return 0
        return Decimal(str(value)) / arg
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage(value, arg):
    """Calculate percentage change."""
    try:
        value = Decimal(str(value))
        arg = Decimal(str(arg))
        if arg == 0:
            return 0
        return ((value - arg) / arg) * 100
    except (ValueError, TypeError):
        return 0