from django import template
from portal.models import treeSpeciesTbl


register = template.Library()



@register.filter
def eokremove(value):
	"""Removes all values of arg from the given string"""

	return value.replace('{', '').replace('}', '').replace("'", '')



@register.filter
def establish(value):
	"""
		Finds the differences between two value and compare with the last value
	"""
	return str(value).replace('_',' ').replace('[','').replace(']','').replace("'",'')


@register.filter
def treespecies(value):
	try:
		aa = treeSpeciesTbl.objects.get(name=value.title()).botanical
		return aa 
	except Exception as e:
		try:
			aa = treeSpeciesTbl.objects.get(name=value).botanical
			return aa 
		except Exception as e:
			return value
		



  