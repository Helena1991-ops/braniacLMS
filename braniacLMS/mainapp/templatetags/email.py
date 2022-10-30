from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.filter
def email(email_string):
    result = f'<a href="mailto:{email_string}">{email_string}</a>'
    return mark_safe(result)



@register.filter
def myfilter(value):
    return value.upper()
