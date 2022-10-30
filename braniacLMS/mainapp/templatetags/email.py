from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.filter
def email(email_string):
    return mark_safe(f'<a href="mailto:{email_string}">{email_string}</a>')



