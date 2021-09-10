from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def highlight_search(text, search):

	text = text.replace(search.lower(), f"<span style='background-color: yellow'>{search.lower()}</span>")
	text = text.replace(search.upper(), f"<span style='background-color: yellow'>{search.upper()}</span>")
	text = text.replace(search.capitalize(), f"<span style='background-color: yellow'>{search.capitalize()}</span>")

	return mark_safe(text)
