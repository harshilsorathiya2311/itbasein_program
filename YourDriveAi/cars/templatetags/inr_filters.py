from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


def format_inr(amount):
    if amount is None:
        return '0'
    try:
        amount = int(round(float(amount)))
    except (ValueError, TypeError):
        return '0'
    if amount < 0:
        prefix = '-'
        amount = abs(amount)
    else:
        prefix = ''
    s = str(amount)
    if len(s) <= 3:
        return prefix + s
    last3 = s[-3:]
    rest = s[:-3]
    groups = []
    while len(rest) > 2:
        groups.append(rest[-2:])
        rest = rest[:-2]
    if rest:
        groups.append(rest)
    result = ','.join(reversed(groups)) + ',' + last3
    return prefix + result


@register.filter(is_safe=True)
def inr(amount):
    return '\u20b9' + format_inr(amount)


@register.filter(is_safe=True)
def inr_value(amount):
    return format_inr(amount)
