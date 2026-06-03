from django import template

register = template.Library()


@register.filter
def zip_lists(a, b):
    """Permite iterar dos listas en paralelo dentro de un template Django.
    Uso: {% for item_a, item_b in lista_a|zip_lists:lista_b %}"""
    return zip(a, b)
