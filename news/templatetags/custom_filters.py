from django import template
import re

register = template.Library()

bad_words = ['художник', 'время', 'слово', 'о',]


def replace(match):
    word = match.group()
    if word.lower() in bad_words:
        return word[0] + '*' * (len(word) - 1)
    else:
        return word


@register.filter()
def censor(value):
    return re.sub(r'\b\w*\b', replace, value, flags=re.I | re.U)
