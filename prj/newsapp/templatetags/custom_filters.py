from django import template

register = template.Library()  # регистрируем  фильтры

CENSORED = ['fuck', 'shit', 'poo', 'fuckin', 'fuck!']
@register.filter(name='censor')
def censor(value):
    value2 = value.split()
    for word in value2:
        if word.lower() in CENSORED:
            value = value.replace(word, '****')
    return value