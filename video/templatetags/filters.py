from django.template import Library
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
register = Library()
 
@register.filter()
def currency(value):
    return locale.currency(value, grouping=True)


